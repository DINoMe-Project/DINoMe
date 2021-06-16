from __future__ import division
import pandas as pd
from sympy import *
from sklearn.utils import class_weight,shuffle
from sklearn.metrics import balanced_accuracy_score,recall_score,precision_score
import numpy as np
def tocnffile(var_sizes,rule,filename):
    rule=to_cnf(rule)
    names=['control','other_0','other_1','secret_0','secret_1']
    offset=1
    sym_index={'c':0,'I':1,'Ialt':2,'s':3,'salt':4}
    declares=[]
    offsets=[]
    atoms=rule.atoms()
    cnf=str(rule)
    for i,size in enumerate(var_sizes):
        offsets.append(offset)
        if(size==0):
            continue
        vars=' '.join([str(i) for i in range(offset,offset+size)])
        declare="c %s --> [%s]"%(names[i],vars)
        offset=offset+size
        declares.append(declare)
    for atom in atoms:
        atom=str(atom)
        if '_' in atom:
            l=atom.split("_")
            sym=l[0]
            sym_offset=int(l[1])
            print("%s >= 1"%atom,"%d"%(offsets[sym_index[sym]]+sym_offset))
            cnf=cnf.replace("%s >= 1"%atom,"%d"%(offsets[sym_index[sym]]+sym_offset))
            cnf=cnf.replace("%s < 1"%atom,"-%d"%(offsets[sym_index[sym]]+sym_offset))
    cnf=cnf.replace("(","").replace(")","")
    cnf=[sorted(cl.split(' | '),key=lambda x: abs(int(x))) for cl in cnf.split(' & ')]
    cnf.sort(key=lambda x: [abs(int(xx)) for xx in x])
    ret='p cnf %d %d'%(sum(var_sizes),len(cnf))+"\n"+'\n'.join(declares)+"\n"+"\n".join(["%s 0"%(" ".join(cls)) for cls in cnf])
    with open(filename,'w') as f:
        f.write(ret)
    return ret

def tosymrule(rule):
    conds=rule.split(' and ')
    conds=[cond.split(' ') for cond in conds]
    conds.sort(key=lambda x: x[0],reverse=True)
    sym_rule=True
    for cond in conds:
        assert(len(cond)==3)
        var=symbols(cond[0])
        op=cond[1]
        try:
            var2=int(float(cond[2]))
        except Exception:
            var2=symbols(cond[2])
        if(op=='<='):
            sym_rule= sym_rule * (var<=var2)
        elif(op=='<'):
            sym_rule= sym_rule & (var<var2)
        elif(op=='>'):
            sym_rule= sym_rule & (var>var2)
        elif(op=='>='):
            sym_rule= sym_rule & (var>=var2)
        else:
            #==
            sym_rule= sym_rule & (var==var2)
    print(conds,sym_rule)
    #simplified_sym_rule=simplify_logic(sym_rule)
    return sym_rule


def simplify_rules(rules,min_precision=0.9):
    #all_rule=False
    all_rule=False
    for rule, score in rules:
        if score[0]<min_precision:
            continue
        sym_rule=tosymrule(rule)
        all_rule=all_rule|(sym_rule)
    #print(all_rule)
    return all_rule
"""
data: pandas.dataframe
"""
def xgbtree_rule_perf(rule,data,y):
    detected_index=data.query(rule).index
    if len(detected_index) <= 1:
        return (0, 0)
    pred_y=np.zeros(y.shape)
    pred_y[detected_index]=1
    sample_weight=class_weight.compute_sample_weight("balanced",y)
    return(precision_score(y,pred_y,
                        sample_weight=sample_weight),
                        recall_score(y,pred_y,sample_weight=sample_weight))

"""
allpaths: = xgbmodel.trees_to_dataframe()
index: tree index
"""
def xgbtree_to_rules(allpaths,index):
    paths=allpaths[allpaths['Tree']==index];
    rules=[]
    print(index)
    def recurse(node,prevcond):
        one=paths[paths['ID']==node]
        assert(len(one)==1)
        #print(one)
        threshold=one['Split'].to_numpy()[0]
        name=one['Feature'].to_numpy()[0]
        #print(name,threshold)
        if name=="Leaf":
            leaf_gain=one['Gain'].to_numpy()[0]
            if(leaf_gain<0):
                return
            prevcond.sort(key=lambda r: r.split(" ")[0])
            rule = str.join(' and ', prevcond)
            rule = (rule if rule != '' else "c_0 == c_0")
            rules.append(rule)
            return
        yes_symbol="<"
        yes_node=one["Yes"].to_numpy()[0]
        no_node=one["No"].to_numpy()[0]
        no_symbol=">="
        yes_cond = prevcond + ["%s %s %d"%(name, yes_symbol, threshold)]
        no_cond = prevcond + ["%s %s %d"%(name, no_symbol, threshold)]
        recurse(yes_node, yes_cond)
        recurse(no_node, no_cond)
    recurse("%d-0"%(index),[])
    return rules if len(rules) > 0 else 'True'
