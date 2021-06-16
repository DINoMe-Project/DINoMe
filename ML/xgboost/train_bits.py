import argparse
from skrules import SkopeRules
from prepare_data import prepare_data
from IPython import embed
from sklearn.utils import class_weight,shuffle
import xgboost
import pandas as pd
import numpy as np
import re
import os
from sklearn.model_selection import GridSearchCV
import datetime

from skrules.xgboost_rules import xgbtree_rule_perf,xgbtree_to_rules,tocnffile,simplify_rules,tosymrule
from sympy import simplify
from customLinear import LinearFeature
"""
data: pandas.dataframe
"""

def toLatex(rule_scores,filename,symbolmap={}):
  typename={'s':r"\\SecFn{}",'salt':r"\\SecFnAlt{}",'I':r"\\AIIFn{}",'c':r"\\ACIFn{}"}
  def ruleToLatex(rule):
    rule=re.sub("diff_s_([0-9]*) ",r"\\diffFeature{\1}",rule)
    for fullname in symbolmap:
      name=fullname.split("_")
      param,offset=symbolmap[fullname]
      name=name[0]
      type=typename[name]
      param=re.sub("([av])([a-z]*)Map_([0-9]*)_([0-9]*)",r"{\1}map[\3][\4]",param)
      rule=re.sub("%s "%fullname,"%s(\\\\text{`%s'})[%d]"%(type,param,offset),rule)
    rule=re.sub("L_([0-9]*) ",r"\\linearFeature{\1}",rule)
    rule=re.sub("s_([0-9]*) ",r"\\SecFn{}[\1]",rule)
    rule=re.sub("c_([0-9]*) ",r"\\ACIFn{}[\1]",rule)
    rule=re.sub("I_([0-9]*) ",r"\\AIIFn{}[\1]",rule)
    rule=re.sub("salt_([0-9]*)",r"\\SecFnAlt{}[\1]",rule)
    rule=re.sub("([av])([a-z]*)Map_([0-9]*)_([0-9]*)",r"\\AIIFn{}(\\text{`{\1}map[\3][\4]}')",rule)
    rule=re.sub("(secret )",r"\\SecFn{}(\\text{`secret'})",rule)
    rule=re.sub("(secretalt )",r"\\SecFnAlt{}(\\text{`secret})",rule)
    rule=re.sub(">=",r"\\ge",rule)
    rule=re.sub(r"text{`secret'}",r"secretVar",rule)
    rule=re.sub(r"text{`secretalt'}",r"secretVar",rule)
    conds=rule.split(" and ")
    conds.sort(key=lambda x: x,reverse=True)
    rule=" \\wedge ".join(conds)
    #rule=re.sub("and",r"\\wedge",rule)
    return rule
  i=0
  ret=[]
  for rule_score in rule_scores:
    rule=rule_score[0]
    score=rule_score[1]
    display="$\\interferenceRule_{%d}$&$%s$&%.2f&%.2f\\\\"%(i,ruleToLatex(rule),score[0],score[1])
    print(display)
    ret.append(display)
    i=i+1
  with open(filename,'w') as f:
    f.write("\n".join(ret))
  return ret
#r=toLatex(rulelist,self.rule_latex,self.symbolmap)

def trim_rule(rule_score,pddata,sample_weight,thres=0.01):
  rule=rule_score[0]
  conds=rule.split(" and ")
  score=rule_score[1]
  newcond=set(conds)
  for cond in conds:
    newcond.remove(cond)
    newrule=" and ".join(list(newcond))
    new_score=xgbtree_rule_perf(str(newrule),pddata,pddata['Y'],sample_weight)
    if new_score[0]<score[0]*(1-thres):
      newcond.add(cond)
  print("trim ", rule, " to ", newrule)
  newcondlist=list(newcond)
  newcondlist.sort()
  newrule=" and ".join(newcondlist)
  newscore=xgbtree_rule_perf(str(newrule),pddata,pddata['Y'],sample_weight)
  return [newrule,newscore]

class LeakageLearner:
  def __init__(self,args):
    self.args=args
    self.outname = os.path.basename(self.args.outname)
    self.outdir = os.path.dirname(self.args.outname)
    self.cnffile="%s.cnf"%self.args.outname
    self.modelfile="%s.model.txt"%self.args.outname
    self.rulefile="%s.rule.txt"%self.args.outname
    self.attacker_cnffile="%s_attacker.cnf"%self.args.outname
    self.attacker_modelfile="%s_attacker.model.txt"%self.args.outname
    self.attacker_rulefile="%s_attacker.rule.txt"%self.args.outname
    self.rule_latex="%s_rule.tex"%self.args.outname
    self.in_param_file=self.args.param
    self.param_file="%s_param.pkl"%(self.args.outname)


  def saverules(self,rules,allrstat,filename):
    allscores=allrstat[1]
    with open(filename,'w') as f:
      f.write("rule,precision,recall,ntree\n")
      for r,scores in rules:
          f.write("%s,%.2f,%.2f,%d\n"%(r,scores[0],scores[1],scores[2]))
      r=allrstat[0]
      f.write("%s,%.2f,%.2f,--\n"%(r,allscores[0],allscores[1]))
    with open(filename+".tex",'w') as f:
      f.write("rule&precision&recall&ntree\\\\\n")
      for r,scores in rules:
        r=r.replace("and","\\wedge")
        r=r.replace(">= 1","= 1")
        r=r.replace("< 1","= 0")
        r=re.sub(r'([a-zA-Z]*)_([0-9]*)',r'\1_{\2}',r)
        f.write("$%s$&%.5f&%.5f&%d\\\\\n"%(r,scores[0],scores[1],scores[2]))

      f.write("$%s$&%.5f&%.5f&--\\\\\n"%(str(allrstat[0]),allscores[0],allscores[1]))
  def loadrules(self,filename):
    pdrules=pd.read_csv(filename)
    return pdrules

  def tune(self):
    xgb_model = xgboost.XGBClassifier()
    params = {'nthread':[8], #when use hyperthread, xgboost may become slower
      'objective':['binary:logistic'],
      'learning_rate': [0.1,0.2, 0.4], #so called `eta` value
      'max_depth': [6,8,10],
      'min_child_weight': [11],
      'silent': [1],
      'subsample': [1.0],
      'n_estimators': [16,32,64], #number of trees, change it to 1000 for better results
      'sample_type':['weighted']}
    clf = GridSearchCV(xgb_model, params, n_jobs=4,
           scoring='roc_auc',cv=2,
           verbose=2, refit=True)
    sample = self.pddata
    clf.fit(sample[self.feature_names], sample["Y"])
    best_parameters=clf.best_params_
    return clf
        
  def train(self,feature_names,symbol_vars):
  #model = xgboost.XGBClassifier(max_depth=7, n_estimators=10)
      #class_w=class_weight.compute_class_weight("balanced",np.unique(y),y)
    self.pddata['Y']=(self.pddata['Y']==self.args.label)
    self.pddata.to_csv(os.path.join(self.outdir,self.outname+datetime.datetime.now().strftime("%Y_%m_%d_%H_%M.csv")))
    traindata=self.pddata.sample(frac=0.8, replace=True)
    traindata=traindata.reset_index(drop=1)
    sample_weight=class_weight.compute_sample_weight("balanced",traindata['Y'])
    X=traindata.iloc[:,1:].to_numpy()
    y=traindata['Y']
    self.sample_weight=sample_weight
    data=xgboost.DMatrix(data=X,
              label=y,
              feature_names=feature_names,
              feature_types=['int']*X.shape[-1],
              weight=sample_weight)
    self.feature_names=feature_names
    d=X.shape[-1]
    feature_combination=[]
    for sym in symbol_vars:
        print(sym)
        if len(symbol_vars[sym])>0:
            feature_combination.append(symbol_vars[sym])
    import pickle
    if self.in_param_file:
      with open(self.in_param_file) as f:
        params=pickle.load(f)
        model=xgboost.train(params = params,
              dtrain=data,
              num_boost_round=self.args.ntrees,
            )

    else:
      t_clf=self.tune()
      model = t_clf.best_estimator_._Booster
      params=t_clf.best_params_
      #params['rate_drop']=0.1
      #params['skip_drop']=0.5
      #params['normalize_type']='tree'
    with open(self.param_file,'wb') as f:
      pickle.dump(params,f)
    print(self.linear)
    if self.args.debug:
      embed()
    model.dump_model(self.modelfile, with_stats=True)
    clf = SkopeRules(max_depth_duplication=self.args.depth,
                 precision_min=0.6,
                 recall_min=0.005,
                 verbose=1,
                 feature_names=feature_names)
    evaldata=self.pddata.sample(frac=0.3, replace=True)
    evaldata=evaldata.reset_index(drop=1)
    eval_sample_weight=class_weight.compute_sample_weight("balanced",evaldata['Y'])
    clf.fit_xgbmodel(evaldata, model, eval_sample_weight)
    print("end fit_xgbmodel")
    clf.rules_.sort(key=lambda x: x[1],reverse=True)
    rules={}
    for i in range(len(clf.rules_)):
      r=trim_rule(clf.rules_[i],evaldata,eval_sample_weight)
      rules[r[0]]=r[1]
    rulelist=[]
    for r in rules:
      rulelist.append([r,rules[r]])
    rulelist.sort(key=lambda x: x[1],reverse=True)
    usedLinear={}
    toLatex(rulelist,self.rule_latex)
    for lname in self.linear:
      if any(lname in r[0] for r in rulelist ):
        usedLinear[lname]=self.linear[lname]
        print("%s=%s"%(lname,usedLinear[lname][0]))

    sym_vars=symbol_vars
    var_sizes=[len(sym_vars['c']), len(sym_vars['I']), len(sym_vars['Ialt']), len(sym_vars['s']), len(sym_vars['salt'])]
    allr1,allr=simplify_rules(clf.rules_)
    #cnf=tocnffile(var_sizes,allr1,self.cnffile)
    allrscore=xgbtree_rule_perf(str(allr1),evaldata,evaldata['Y'],eval_sample_weight)
    print("all r=",simplify(~allr),allrscore)
    self.saverules(clf.rules_,[simplify(allr),allrscore],self.rulefile)
    if self.args.debug:
      embed()

  def localLearner(self,pddata,symbol_vars):
    continuous={}
    #continuous['s']=[(0,8,"secret")]
    #continuous['salt']=[(0,8,"secret'")]
    #continuous['c']=[(0,8,"offset")]
    #continuous['I']=[(0,8,"arr1_size")]
    intCols=['Y']
    with open(self.args.symbol) as symbolfile:
      for line in symbolfile:
        line.replace("\n","")
        w=line.split()
        if w[0] not in continuous:
          continuous[w[0]]=[]
        continuous[w[0]].append((int(w[1]),int(w[2]),w[3]))
    ncols=pddata.shape[1]
    self.symbolmap={}
    for xtype in continuous:
      for x_range in continuous[xtype]:
        x_name=x_range[2]
        x_val=0
        base=1;
        start=x_range[0]
        size=x_range[1]
        valid=True
        for offset in range(size):
          i=start+offset
          name="%s_%d"%(xtype,i)
          self.symbolmap[name]=[x_name,offset]
          if name not in pddata.columns:
            x_val=0
            valid=False
            break
          x_val=x_val+pddata[name]*base
          base=base*2
        symbol_vars[xtype].append(x_name)
        if (x_name not in pddata.columns) and valid:
          print("add",x_name)
          pddata.insert(ncols,x_name, x_val)
          intCols.append(x_name)
    intData=pddata[intCols]
    lf=LinearFeature()
    lf.fit(intData,NStep=self.args.nlinear,thresDis=self.args.disThres)
    self.lf=lf
    feature,addeddata=lf.features(0.8)
    return feature,pd.DataFrame(data=addeddata)

  def main(self,samedata_file,diffdata_file):
    X,y,feature_names,symbol_vars=prepare_data(samedata_file,diffdata_file,self.args.outname)
    #embed()
    pddata=pd.DataFrame(X,columns=feature_names)
    pddata.insert(0, 'Y',  y)
    linear,addeddata=self.localLearner(pddata,symbol_vars)
    self.linear=linear
    for name in feature_names:
      if "s_" in name:
        name2=name.replace('s_',"salt_")
        val=abs(pddata[name]-pddata[name2])
        addeddata["diff_%s"%name]=val.to_numpy()
    pddata=pddata.join(pd.DataFrame(data=addeddata))
    dirname=os.path.dirname(samedata_file)
    self.pddata=pddata
    feature_names=pddata.columns[1:]
    self.train(feature_names,symbol_vars)
    

  def run(self):
    if len(args.files)==1:
      self.main(args.files[0],None)
    else:
      self.main(args.files[0],args.files[1])

if __name__=="__main__":
  parser = argparse.ArgumentParser(description='match symbol')
  parser.add_argument('files',metavar='files',type=str,nargs="+",help='same file, diff file')
  parser.add_argument('--debug',type=bool,default=False,help='decision rule depth')
  parser.add_argument('--depth',type=int,default=6,help='decision rule depth')
  parser.add_argument('--ntrees',type=int,default=10,help='decision trees')
  parser.add_argument('--outname',type=str,default="xgboost_1",help='outname')
  parser.add_argument('--symbol',type=str,default="symbol.txt",help='outname')
  parser.add_argument('--param',type=str,default="",help='outname')
  parser.add_argument('--label',type=int,default=1,help='label value')
  parser.add_argument('--nlinear',type=int,default=100,help='number of linear model ')

  parser.add_argument('--disThres',type=float,default=0.2,help='local threshold')
  args=parser.parse_args()
  learner=LeakageLearner(args)
  learner.run()
