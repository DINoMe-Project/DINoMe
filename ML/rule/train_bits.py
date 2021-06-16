import argparse
from skrules import SkopeRules
from prepare_data import prepare_data
from IPython import embed
from sklearn.utils import class_weight,shuffle

def train(X,y,feature_names):
    clf = SkopeRules(max_depth_duplication=3,
                 max_depth=10,
                 n_estimators=30,
                 precision_min=0.3,
                 recall_min=0.1,
                 max_samples=0.8,
                 n_jobs=-1,
                 verbose=1,
                 max_features="auto",
                 feature_names=feature_names)
    X,y=shuffle(X,y)
    Xtrain=X[0:5000,:]
    ytrain=y[0:5000,:]
    embed()
    clf.fit(X, y==0)
    #clf.fit(X, y==0)
    embed()
def main(samedata_file,diffdata_file):
    x,y,feature_names,symbol_vars=prepare_data(samedata_file,diffdata_file)
    #embed()
    train(x,y,feature_names)
if __name__=="__main__":
    parser = argparse.ArgumentParser(description='match symbol')
    parser.add_argument('files',metavar='files',type=str,nargs="+",help='same file, diff file')
    args=parser.parse_args()
    if len(args.files)==1:
        main(args.files[0],None)
    else:
        main(args.files[0],args.files[1])
