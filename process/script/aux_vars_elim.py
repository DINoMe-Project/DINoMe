from pysat.formula import CNF
from IPython import embed
import argparse
import logging
logging.basicConfig(filename='elimination.log',level=logging.DEBUG)
"""
Motivated by B+E simplification, this script will try to remove auxilary variables as much as possible.
"""
class Simp:
    def comment2varmap(self,comments):
        varmap={}
        for comment in comments:
            if "-->" in comment:
                name=comment.split()[1]
                variables=[int(v) for v in comment.split('[')[-1].split(']')[0].split()]
                varmap[name]=variables
        return varmap
    def varmap2comments(self,varmap):
        comments=[]
        for name in varmap:
            variables=' '.join([str(i) for i in varmap[name]])
            comments.append("c %s --> [ %s ]"%(name,variables))
        return comments

    def __init__(self,args):
        self.args=args
        cnf=CNF(from_file=args.file)
        varmap={}
        self.clause_per_vars={}
        self.outputLits=set()
        self.inputLits=set()
        varmap=self.varmap=self.comment2varmap(cnf.comments)
        for name in varmap:
            if name == 's%d'%(args.nstate):
                self.outputLits.update( varmap[name])
            else:
                self.inputLits.update(varmap[name])
        i=-1
        maxv=1
        self.clause_per_lit={}
        self.unit_clauses={}
        self.clsize_per_vars={}
        for clause in cnf.clauses:
            i=i+1
            noutput=0
            if len(clause)==1:
                self.unit_clauses[abs(clause[0])]=i
                continue
            for lit in clause:
                v=abs(lit)
                maxv=max(v,maxv)
                if v in self.outputLits or -v in self.outputLits:
                    noutput=noutput+1
                if v not in self.clause_per_vars:
                    self.clause_per_vars[v]=set()
                    self.clsize_per_vars[v]=0
                if lit not in self.clause_per_lit:
                    self.clause_per_lit[lit]=set()
                self.clause_per_vars[v].add(i)
                self.clause_per_lit[lit].add(i)
                self.clsize_per_vars[v]=self.clsize_per_vars[v]+len(clause)
        self.cnf=cnf
        self.nvar=maxv
        self.connections=[]
        self.symbolLits=set()
        self.symbolLits.update(self.inputLits)
        self.symbolLits.update(self.outputLits)
    def renumberCNF(self,removedVars):
        """Renumber clauses after remove removedVars"""
        count=1
        renumber={}
        print(removedVars)
        for v in range(1,self.nvar+1):
            if v in removedVars:
                continue
            renumber[v]=count
            count=count+1
        for name in self.varmap:
            self.varmap[name]= [renumber[abs(lit)] if lit>0 else -renumber[abs(lit)]for lit in self.varmap[name]]
        i=0
        for clause in self.cnf.clauses:
            for v in clause:
                if abs(v) in removedVars:
                    embed()
            self.cnf.clauses[i]=[renumber[abs(lit)] if lit>0 else -renumber[abs(lit)]for lit in clause]
            i=i+1
        self.cnf.comments=self.varmap2comments(self.varmap)

    def eliminate(self,outfile):
        newclauses=[]
        ncheck=0
        nclauses=len(self.cnf.clauses)
        removeIdx=set()
        removedVars=set()
        tocheck=[]
        donotcheck=set([abs(lit)for lit in self.symbolLits])
        for v in self.unit_clauses:
            donotcheck.add(v)
        for v in self.clause_per_vars:
            tocheck.append([v,self.clsize_per_vars[v]-len(self.clause_per_vars[v])])
        tocheck=sorted(tocheck,key=lambda x: -x[1])
        tocheck=[i for i,j in tocheck]
        npossible=self.nvar-len(donotcheck)
        while len(tocheck)>0 and ncheck<self.args.maxcheck:
            v=tocheck[-1]
            tocheck.pop()
            if v in donotcheck:
                continue
            if v not in self.clause_per_vars:
                continue
            if (v not in self.clause_per_lit) or (-v not in self.clause_per_lit):
                removedVars.add(v)
                for i in self.clause_per_vars[v]:
                    removeIdx.add(i)
                continue
            if len(self.clause_per_lit[v])>0 and len(self.clause_per_lit[-v])>0:
                if len(self.clause_per_lit[v])* len(self.clause_per_lit[-v])>self.args.maxres:
                    donotcheck.add(v)
                    logging.debug('Do not remove %d due to %d*%d '%(v,len(self.clause_per_lit[v]),len(self.clause_per_lit[-v])))
                    continue
                ncheck=ncheck+1
                print("try,v=",v)
                removedVars.add(v)
                for i in self.clause_per_lit[v]:
                    if i in removeIdx:
                        continue
                    clause1=self.cnf.clauses[i][:]
                    for j in self.clause_per_lit[-v]:
                        if j in removeIdx:
                            continue
                        clause2=self.cnf.clauses[j][:]
                        newcl=set(clause1 + clause2)
                        newcl.remove(v)
                        if -v not in newcl:
                            embed()
                        newcl.remove(-v)
                        newcl=sorted(list(newcl))
                        for v2 in newcl:
                            if -v2 in newcl:
                                newcl=[]
                        if len(newcl)>0:
                            self.cnf.append(newcl)
                            for lit in newcl:
                                if abs(lit) not in donotcheck:
                                    if abs(lit) not in tocheck:
                                        logging.debug('add %d to check queue'%(abs(lit)))
                                        tocheck.append((abs(lit),self.clause_per_vars[abs(lit)]))
                                self.clause_per_vars[abs(lit)].add(nclauses)
                                self.clause_per_lit[lit].add(nclauses)
                            nclauses=nclauses+1
            for i in self.clause_per_vars[abs(v)]:
                removeIdx.add(i)
                #self.cnf.comments.append("c removed var %d"%v)
        for i in sorted(removeIdx, reverse=True):
            del self.cnf.clauses[i]
        #self.renumberCNF(removedVars)
        print("Eliminsated %d/%d"%(len(removedVars),npossible))
        logging.info("Eliminsated %d/%d"%(len(removedVars),npossible))
        self.cnf.to_file(outfile)

    def connect(self,outputv,inputv,checked=[]):
        if outputv in checked:
            return False;
        print("checking %d %d"%(outputv,inputv))
        checked.append(abs(outputv))
        if (outputv,inputv) in self.connections:
            return True
        if len(self.clause_per_vars[outputv].intersection(self.clause_per_vars[inputv]))>0:
            self.connections.append((outputv,inputv))
            return True
        for i in self.clause_per_vars[outputv]:
            for lit in self.cnf.clauses[i]:
                if lit not in self.outputLits and lit not in self.inputLits:
                    if self.connect(abs(lit),inputv,checked):
                        return True
        return False

    def build(self):
        for output_lit in self.outputLits:
            for input_lit in self.inputLits:
                if self.connect(abs(output_lit),abs(input_lit),[]):
                    print("%d %d is connected"%(abs(output_lit),abs(input_lit)))
        embed()
if __name__=="__main__":
    parser = argparse.ArgumentParser(description='match symbol')
    parser.add_argument('file',metavar='files',type=str,
            help='smt file generated from yosys tool')
    parser.add_argument('--nstate',type=int,default=10,
            help='smt file generated from yosys tool')
    parser.add_argument('--maxres',type=int,default=500,
            help='smt file generated from yosys tool')
    parser.add_argument('--maxcheck',type=int,default=10000,
            help='smt file generated from yosys tool')
    args=parser.parse_args()
    simp=Simp(args)
    simp.eliminate(args.file+".e")
    



