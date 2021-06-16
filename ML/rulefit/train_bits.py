from sklearn.svm import LinearSVC
from IPython import embed
import numpy as np
import pandas as pd
from rulefit import RuleFit
from sklearn.cluster import DBSCAN
from sklearn.ensemble import GradientBoostingRegressor,GradientBoostingClassifier
from prepare_data import prepare_data

def test():
    X = []
    Y = []
    for i in np.linspace(1, 100,20):
        for j in np.linspace(-100.0+i,100.0+i,20):
            for k in np.linspace(-100.0+i,100.0+i,20):
                x1=i
                x2=x1+j
                x3=x1+k
                if (x1<=x2 and x1>x3) or (x1>x2 and x1<=x3):
                    y=1
                else:
                    y=0
                X=X+[[x1,x2,x3]]
                Y=Y+[y]
def main(samedata_file,diffdata_file):

    x,y,feature_names,symbol_vars=prepare_data(samedata_file,diffdata_file)
    #['x1','x2','x3','x1-x2','x1-x3','x2-x3']
    embed()
    
    gb = GradientBoostingClassifier(
                        n_estimators=10,
                        max_depth=4,
                        learning_rate=0.1,
                        min_samples_leaf=10,
                        max_features="sqrt",
                        n_iter_no_change=5)
    rf = RuleFit(tree_generator=gb,rfmode="classify")
    print("fit")
    rf.fit(x, y, feature_names=feature_names)
    embed()
    rules = rf.get_rules()
    rules = rules[rules.coef != 0].sort_values("support", ascending=False)
    embed()

import argparse
if __name__=="__main__":
    parser = argparse.ArgumentParser(description='match symbol')
    parser.add_argument('files',metavar='files',type=str,nargs="+",help='same file, diff file')
    args=parser.parse_args()
    if len(args.files)==1:
        main(args.files[0],None)
    else:
        main(args.files[0],args.files[1])
