from skrules.xgboost_rules import simplify_rules,tosymrule, xgbtree_rule_perf
import argparse
from IPython import embed
from sympy import simplify, And
import networkx as nx
from networkx.drawing.nx_pydot import write_dot
from prepare_data import prepare_data
import pandas as pd
from sklearn.utils import class_weight
import os
import math
class DAG:
  def __init2__(self,rulef, outf,args):
    self.rules = []
    self.nodenames = []
    self.rule_perf = []
    self.args=args
    self.outf=outf
    self.name=os.path.splitext(rulef)[0]
    self.graph = nx.DiGraph()
    with open(rulef) as f:
      lines= f.read().split("\n")
    for line in lines[1:-2]:
      line=line.replace("\\wedge","and")
      line=line.replace("\\ge"," >=")
      line=line.replace("\\","").replace("$\\","").replace("$","")
      line=line.replace("text{`","").replace("}","").replace("{(","_").replace("(","").replace(")","").replace("Var","").replace("{[","_").replace("]","")
      line=line.replace("")
      print(line)
      rule_perf = line.split("&")[1:]
      r=tosymrule(rule_perf[0])[1]
      self.rules.append(r)
      self.rule_perf.append((r,float(rule_perf[1]),float(rule_perf[2])))
      embed()
      p = f"precision: {rule_perf[1]}\nrecall: {rule_perf[2]}"
      nodename=f"{r}\n{p}"
      self.nodenames.append(nodename)
      self.graph.add_node(nodename,label = r)
    print(self.rules)
  def __init__(self,rulef, outf, args):
    self.sortby={"precision": (lambda x: (-x[1],-x[2], len(str(x[0])))), "recall": (lambda x: (-x[2],-x[1],len(str(x[0])))), "f1": (lambda x: (-x[1]*x[2]/(x[1]+x[2]),len(str(x[0])))) }
    self.rules = []
    self.redudant=set()
    self.args=args
    self.nodenames = []
    self.rule_perf = []
    self.outf=outf
    self.rulef=rulef
    self.name=os.path.splitext(rulef)[0]
    self.graph = nx.DiGraph()
    with open(rulef) as f:
      lines= f.read().split("\n")
    
    for line in lines[1:-2]:
      rule_perf = line.split(",")
      cr=tosymrule(rule_perf[0])[0]
      r=tosymrule(rule_perf[0])[1]
      self.rules.append(r)
      self.rule_perf.append((cr,float(rule_perf[1]),float(rule_perf[2])))
      p = f"precision: {rule_perf[1]}\nrecall: {rule_perf[2]}"
      nodename=f"{r}\n{p}"
      self.nodenames.append(nodename)
      self.graph.add_node(nodename,label = r)
    print(self.rules)

  
  def accumulated(self):
    print("accumulated")
    self.alldata=pd.read_csv(self.args.data)
    self.pddata=self.alldata.sample(frac=0.3, replace=True)
    self.pddata=self.pddata.reset_index(drop=1)
    #embed()
    sample_weight=class_weight.compute_sample_weight("balanced",self.pddata['Y'])
    acculated_r = False
    acculated_p = 0
    acculated_recall = 0
    prev_p=0
    prev_recall = 0
    out=""
    self.rule_perf=sorted(self.rule_perf,key = self.sortby[self.args.sort])
    #self.rule_perf=sorted(self.rule_perf,key = lambda x: -x[1]*x[2]/(x[1]+x[2]))
    index_set = set(range(len(self.rule_perf)))-self.redudant
    print(index_set)
    count = 0
    while index_set:
      pick_index=0
      candidates=[]
      for index in list(index_set)[:4]:
        r, _, _ = self.rule_perf[index]
        tmp_r = acculated_r | r
        precision, recall = xgbtree_rule_perf(str(tmp_r),self.pddata,self.pddata['Y'],sample_weight)
        candidates.append((index,precision,recall,tmp_r))
      candidates = sorted(candidates, key = self.sortby[self.args.sort])
      print("candidates",candidates)
      i,acculated_p,acculated_recall, tmp_r  = candidates[0]
      index_set.remove(i)
      r,precision,recall = self.rule_perf[i]
      if acculated_recall <= prev_recall*self.args.dev_ratio:
        continue
      acculated_r = acculated_r|r
      prev_p=acculated_p
      prev_recall = acculated_recall
      out =out + f"{i}:{r}, {acculated_p}, {acculated_recall},{precision},{recall}\n"
    """
    for r, precision, recall in self.rule_perf:
      if not acculated_r:
        acculated_r= r
      else:
        acculated_r = acculated_r | r
      acculated_p, acculated_recall = xgbtree_rule_perf(str(acculated_r),self.pddata,self.pddata['Y'],sample_weight)
      out =out + f"{r}, {acculated_p}, {acculated_recall},{precision},{recall}\n"
    """
    print(out)
    with open(os.path.join(os.path.dirname(self.rulef),os.path.splitext(os.path.basename(self.rulef))[0]+f"-{self.args.sort}-{self.args.dev_ratio}-accumulated.txt"),"w") as f:
      f.write(out)
      
  def ind_accumulated(self):
    print("accumulated")
    self.alldata=pd.read_csv(self.args.data)
    self.pddata=self.alldata.sample(frac=0.25, replace=True)
    self.pddata=self.pddata.reset_index(drop=1)
    #embed()
    sample_weight=class_weight.compute_sample_weight("balanced",self.pddata['Y'])
    acculated_r = False
    acculated_p = 0
    acculated_recall = 0
    prev_p=0
    prev_recall = 0
    out=""
    self.rule_perf=sorted(self.rule_perf,key = self.sortby[self.args.sort])
    #self.rule_perf=sorted(self.rule_perf,key = lambda x: -x[1]*x[2]/(x[1]+x[2]))
    index_set = set(range(len(self.rule_perf)))-self.redudant
    print(index_set)
    count = 0
    for i in range(len(self.rule_perf)):
      r, precision, recall = self.rule_perf[i]
      acculated_r = acculated_r | r
      acculated_p, acculated_recall = xgbtree_rule_perf(str(acculated_r),self.pddata,self.pddata['Y'],sample_weight)
      if acculated_recall <= prev_recall*self.args.dev_ratio:
        continue
      prev_p=acculated_p
      prev_recall = acculated_recall
      out =out + f"{i}:{r}, {acculated_p}, {acculated_recall},{precision},{recall}\n"
    print(out)
    with open(os.path.join(os.path.dirname(self.rulef),os.path.splitext(os.path.basename(self.rulef))[0]+f"-ind-{self.args.sort}-{self.args.dev_ratio}-accumulated.txt"),"w") as f:
      f.write(out)

  def dedup(self):
    n = min(50,len(self.rules))
    for i in range(n):
      for j in range(n):
        if i == j:
          continue
        r1 = self.rules[i]
        r2 = self.rules[j]
        r12 = simplify((~r1)&r2)
        print(f"{r1},{r2},{r12}")
        if str(r12) == "False":
          self.redudant.add(j)
    for i in range(n):
      if i not in self.redudant:
        out = out + f"{self.rule_perf[i][0]},{self.rule_perf[i][1]},{self.rule_perf[i][2]}\n"
    with open(os.path.join(os.path.dirname(self.rulef),os.path.splitext(os.path.basename(self.rulef))[0]+"-noredudant.txt"),"w") as f:
      f.write(out)

  def to_dag(self):
    n = len(self.rules) 
    for i in range(n):
      for j in range(n):
        if i == j:
          continue
        r1 = self.rules[i]
        r2 = self.rules[j]
        r12 = simplify((~r1)&r2)
        print(f"{r1},{r2},{r12}")
        if str(r12) == "False":
          self.graph.add_edge(self.nodenames[i],self.nodenames[j],style = "solid")
    pos = nx.nx_agraph.graphviz_layout(self.graph)
    nx.draw(self.graph, pos=pos)
    write_dot(self.graph, self.name+".dot")
    
  def to_ruledag(self):
    cnfG = nx.DiGraph()
    n = len(self.rules)
    basic = {}
    for rule in self.rules:
      if not isinstance(rule, And):
        continue
      conds = rule.args
      m=len(conds)
      for i in range(m):
        cond1=conds[i]
        a = cond1.atoms() 
        assert(len(a)==1)
        a=list(a)[0]
        if a not in basic:
          basic[a]= set()
        basic[a].add(cond1)
        for j in range(i+1,m):
          cond2=conds[j]
          cnfG.add_edge(cond1,cond2)
          print(cond1,cond2)
    for a in basic:
      if len(basic[a])==2:
        b = list(basic[a])
        cnfG.add_edge(*b,style="dashed")
        
    pos = nx.nx_agraph.graphviz_layout(cnfG)
    nx.draw(cnfG, pos=pos)
    write_dot(cnfG, self.name+".cnf.dot")

if __name__=="__main__":
  parser = argparse.ArgumentParser(description='match symbol')
  parser.add_argument('rulefile',metavar='files',type=str,help='.rule.txt files')
  parser.add_argument('--outname',type=str,default="out.dag",help='outname')
  parser.add_argument('--dev_ratio',type=float,default=1,help='outname')
  parser.add_argument('--data',type=str,default="data.csv",help='data csv')
  parser.add_argument('--mode',type=str,default="acc",help='data csv')
  parser.add_argument('--sort',type=str,default="precision",help='sort by')
  args=parser.parse_args()
  dag = DAG(args.rulefile, args.outname, args)
  if args.mode == "acc":
    dag.accumulated()
  if args.mode == "indacc":
    dag.ind_accumulated()
  if args.mode == "dedup":
    dag.dedup()