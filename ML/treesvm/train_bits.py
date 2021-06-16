from sklearn.svm import LinearSVC, SVC
from IPython import embed
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn import metrics,tree
from sklearn.linear_model import SGDClassifier
import  sys
from sklearn.feature_selection import RFE, VarianceThreshold
import  pandas as pd
import textwrap
from sklearn.cluster import DBSCAN
from prepare_data import prepare_data
from sklearn.linear_model import ElasticNetCV
from sklearn.utils import class_weight,shuffle
import tensorflow as tf
import tensorflow.keras  as keras
class MyLayer(keras.layers.Layer):
    def __init__(self, **kwargs):
        self.output_dim = 1
        super(MyLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        # Create a trainable weight variable for this layer.
        self.kernel = self.add_weight(name='kernel',
                                      shape=(input_shape[1], self.output_dim),
                                      dtype=tf.float32,
                                      initializer='random_normal',
                                      trainable=True)
        self.bias = self.add_weight(name="bias",
                                    shape=(self.output_dim,),
                                    initializer='random_normal',
                                    dtype=tf.float32,
                                    trainable=True)
        super(MyLayer, self).build(input_shape)  # Be sure to call this at the end

    def call(self, x):
        return keras.backend.dot(x, self.kernel)+self.bias

    def compute_output_shape(self, input_shape):
        return (input_shape[0], self.output_dim)


class FlexLinear:
    def fit(self,X,y):
        X,y=shuffle(X,y)
        nfeature=X.shape[-1]
        inputs = keras.Input(shape=(nfeature,), name='bitvec')
        outputs=keras.layers.Dense(1, activation='sigmoid')(inputs)
        #keras.layers.Activation("sigmoid")(MyLayer()(inputs))
        y=np.reshape(y,(y.shape[0],))
        #self.model=keras.Model(inputs,outputs)
        self.model = keras.models.Sequential()
        cw=class_weight.compute_class_weight("balanced", np.unique(y), y)
        self.model.add(keras.layers.Dense(1, input_dim=nfeature, activation='sigmoid'))
        self.model.compile(optimizer=keras.optimizers.SGD(lr=0.03, decay=1e-6, momentum=0.9, nesterov=True),  # Optimizer
                  # Loss function to minimize
                  loss=keras.losses.hinge,
                  # List of metrics to monitor
                  loss_weights=[cw],
                  class_weight=cw,
                  metrics=[keras.metrics.binary_accuracy])
        history = self.model.fit(X, y,
                        batch_size=int(X.shape[0]/10),
                        epochs=30,
                        # We pass some validation for
                        # monitoring validation loss and metrics
                        # at the end of each epoch
                        validation_split=0.1,workers=4, use_multiprocessing=True)
        #embed()
    def predict(self,X):
        y= self.model.predict_classes(X,batch_size=100000)
        #return y
        return np.reshape(y,(y.shape[0],1))
    @property
    def coef_(self):
        return self.model.get_weight()[0]
    @property
    def intercept_(self):
        return self.model.get_weight()[1]

def myloss(Y,myY):
    print("myloss")
    if np.unique(Y).shape[0]==1:
        return 0
    try:
        ret= -metrics.log_loss(Y,myY)
    except Exception as e:
        embed()
    return ret
def myscore(Y,myY):
    if np.unique(Y).shape[0]==1:
        return 1.0
    return metrics.balanced_accuracy_score(Y,myY,pos_label=0)
#max_score=0
#min_score=-100000
score_fn=metrics.balanced_accuracy_score
max_score=1.0
min_score=0
def process():
    _OFFSET_SIZE=3
    N=111
    choice=np.arange(N)
    np.random.shuffle(choice)
    train_choice=choice[0:int(N*0.9)]
    test_choice=choice[int(N*0.9):N]
    same_data=np.genfromtxt('sample_declass/12.same.csv',filling_values=2,delimiter=",")
    diff_data=np.genfromtxt('sample_declass/12.diff.csv',filling_values=2,delimiter=",")

    split_index=np.unique(np.where(same_data==2)[1]);
    cs=range(0,split_index[0])
    I=range((split_index[0]+1),split_index[1])
    s=range((split_index[1]+1),split_index[2])
    sAlt=range((split_index[2]+1),split_index[3])
    X=np.concatenate((same_data,diff_data))
    Y=np.concatenate((np.zeros((same_data.shape[0],1)),np.ones((diff_data.shape[0],1))))
    N=X.shape[0]
    choice=np.arange(N)
    np.random.shuffle(choice)
    train_choice=choice[0:int(N*0.9)]
    test_choice=choice[int(N*0.9):N]
    symbol_valuess={"P":cs[:32],"COFF":cs[32:], "SOFF":I[:_OFFSET_SIZE],"SIZE":I[_OFFSET_SIZE:],"S":s,"S'":sAlt}
    pred_c=X[:,cs[:32]]
    coff=X[:,cs[32:]]
    coff=bits2value(X[:,cs[32:]])
    soff=bits2value(X[:,I[:_OFFSET_SIZE]])
    size=bits2value(X[:,I[_OFFSET_SIZE:]])
    s=X[:,s]
    s_alt=X[:,sAlt]
    X=np.concatenate((pred_c,coff,soff,size,s,s_alt),1)

def bits2value(bits):
    value=np.zeros((bits.shape[0],1));
    for i in range(bits.shape[1]):
        value=value*2+bits[:,i:i+1]
    return value


#data=np.array(X)
#data=np.append(data,np.array(Y).reshape([-1,1]),)
idcache=set()
class SVCTree:
    def getSV(i):
        if i>-1:
            return clf.support_vector_[:,i]
        else:
            return clf.coef0
    def getVarName(i):
        if i<0:
            return ''
        return 'X'+str(i)
    def poly_str(self,clf):
        feature_map={}
        nfeature=clf.support_vector_.shape[1]
        for i in range(-1,nfeature):
            feature_map[i]={}
            for j in range(i,nfeature):
                feature_map[i][j]=0
        if clf.degree==2:
            for index1 in range(-1,nfeature):
                for index2 in  range(-1,nfeature):
                    i=min(index1,index2)
                    j=max(index1,index2)
                    svi=self.getSV(i);
                    svj=self.getSV(j);
                    feature_map[i][j]=feature_map[i][j]+np.sum(svi*svj)
        for i in feature_map:
            for j in range(i,nfeature):
                if feature_map[i][j]<0:
                    s=s+'-'
                else:
                    s=s+'+'
            s=s+'{:.1f}'.format(abs(feature_map[i][j]))+self.getVarName(i)+'*'+self.getVarName(j)
        return s
    def __init__(self,nodeid,level,feature_combination,
            min_node_size=100,max_level=4,tol=0.01,model='linear',cols=None,position=""):
        self.left=None
        self.right=None
        self.clf=None
        self.count=0
        self.cols=cols
        self.position=position
        self.min_node_size=min_node_size
        self.true_sample=0
        self.false_sample=0
        while nodeid in idcache:
               nodeid=nodeid+1
        idcache.add(nodeid)
        self.nodeid=nodeid
        print("new node",nodeid,"\n");
        self.level=level;
        self.feature_combination=feature_combination
        self.feautre=self.feature_combination[0]
        self.score=-100000
        self.base_score=-10000
        self.tol=tol
        self.sampleSize=0
        self.model=model
    def predict(self,X):
        if self.clf.predict(X):
            if self.left:
                return self.left.predict(x)
            else:
                return 1
        else:
            if self.right:
                return self.right.predict(x)
            else:
                return 0

    def node2str(self):
        s=""
        if self.model=='poly':
            s=s+self.poly_str()
        elif self.clf!=None:
            if len(self.clf.coef_.shape)>1:
                coef=self.clf.coef_[0]
            else:
                coef=self.clf.coef_
            intercept=self.clf.intercept_[0]
            intercept=intercept
            avg=np.mean(np.abs(coef))
            #limit=max(avg,0.01*large)
            sorted_index=np.argsort(np.abs(coef))
            choice=np.where(np.abs(coef)>avg*0.1)[0]
            selected_coef=coef[choice]
            small=max(1.0,min(intercept,np.min(np.abs(selected_coef))))
            choice= sorted_index[-selected_coef.shape[-1]:]
            coef=coef/small
            for offset in choice:
                w=coef[offset]
                i=self.feature[offset]
                if w<0:
                    s=s+'-'+"{:.3f}".format(-w)+self.cols[i]
                elif w>0:
                    s=s+'+'+"{:.3f}".format(w)+self.cols[i]
            if intercept<0:
                s=s+'-'+"{:.3f}".format(-intercept)
            if intercept>0:
                s=s+'+'+"{:.3f}".format(intercept)

        if len(s):
            s="%s>0"%(s)
        s="\n".join(textwrap.wrap(s,50))
        s=s+ '\nbase='+"{:.3f}".format(self.base_score)+'\nscore='+"{:.3f}".format(self.score)+"\nsample="+str(self.sampleSize)
        s="%s\nTrue: %d, False:%d" %(s, self.true_sample,self.false_sample)
        return s

    def build_svc(self,X,Y,level,base_acc=0):
        self.true_sample= len(Y[Y==1])
        self.false_sample=len(Y[Y==0])
        best_clf=None
        self.X=X
        print("build svc")
        self.base_score=best_score=base_acc
        best_pY=np.array([])
        self.score=base_acc
        self.sampleSize=X.shape[0]
        self.feature=self.feature_combination[0]
        if self.true_sample<self.min_node_size/2 or self.false_sample<self.min_node_size/2:
            #embed()
            print("return1")
            return 1;
        if base_acc>max_score-self.tol:
            print("return2")
            return 1;
        print ("before com")
        for comb in self.feature_combination:
            if self.model == "flexlinear":
                clf=FlexLinear()
            elif self.model == 'linear':
                clf=SGDClassifier(max_iter=10000,
                                    class_weight="balanced",
                                    early_stopping=True,
                                    random_state=0,
                                    penalty="l1",
                                    )
                #clf = LinearSVC(tol=1e-4,penalty='l2',class_weight='balanced',dual=False)
            elif self.model !='sgd':
                clf = SVC(tol=1e-4,kernel=self.model,gamma='auto',probability=True)
            else:
                clf = SGDClassifier(loss='hinge',learning_rate='adaptive',eta0=0.02,epsilon=0.0001,tol=0.0000001)
            clf.fit(X[:,comb], Y)
            pY=clf.predict(X[:,comb])
            score=score_fn(Y, pY)
            if score>best_score+self.tol or (abs(score-best_score)<self.tol and len(comb)<len(self.feature)):
                best_score=score
                best_clf=clf
                best_pY=pY
                self.feature=comb
            print(self.position,X[:,comb].shape,comb,score,base_acc)
        print(self.position,X[:,self.feature].shape,self.feature,best_score,base_acc)
        self.clf=best_clf

        if self.clf==None:
            return 1

        self.count=self.count+1
        pY=best_pY
        #print(pY)
        print("Improve accuracy by ",best_score-base_acc)
        if (best_score-base_acc)<0.1:
            return self.count
		
        self.score=best_score

        if level==0:
            return self.count
        if len(Y[np.where(pY==1)])>0:
            left_acc=score_fn(Y[np.where(pY==1)[0],:],pY[np.where(pY==1)])
            self.left= SVCTree(self.nodeid+1,self.level-1,self.feature_combination,cols=self.cols,position=self.position+"l")
            #embed()
            subcount=self.left.build_svc(X[np.where(pY==1)[0],:],Y[np.where(pY==1)],level-1,left_acc)
        if len(Y[np.where(pY==0)])>0:
            right_acc=score_fn(Y[np.where(pY==0)[0],:],pY[np.where(pY==0)])
            self.right=SVCTree(self.nodeid+self.count,self.level-1,self.feature_combination,cols=self.cols,position=self.position+"r")
            subcount=self.right.build_svc(X[np.where(pY==0)[0],:],Y[np.where(pY==0)],level-1,right_acc)
            self.count=self.count+subcount
        return self.count

    def _export_to_dot(self,f):
        node_id=0
        #if self.clf==None:
        #    return
        stack=[[tree,0]]
        exp= self.node2str()
        f.write('%d [label="%s"];\n'
                               % (self.nodeid,exp))
        if self.left!=None:
            f.write("%d -> %d\n [label=True]" % (self.nodeid,self.left.nodeid))
            self.left._export_to_dot(f)
        if self.right!=None:
            f.write("%d -> %d\n [label=False]" % (self.nodeid,self.right.nodeid))
            self.right._export_to_dot(f)


    def export_to_dot(self,filename):
        f=open(filename,'w+')
        f.write("digraph g {\nnode [shape=box] ;\n")
        self._export_to_dot(f)
        f.write("}")
        f.close()

def main(samedata_file,diffdata_file):
    x,y,cols,symbol_vars=prepare_data(samedata_file,diffdata_file)
    #embed()
    #embed()
    train(x,np.reshape(y,(-1,1)),cols,symbol_vars)

    #trainDT(x,y,cols,count,symbol_vars)
def interpretable(out_filename,cols):
    contents=""
    with open(out_filename,"r") as f:
        contents=f.read()
    for i in range(len(cols)):
        contents=contents.replace("X[%d]"%(i),cols[i])
    with open(out_filename.replace(".dot","_symbol.dot"),"w+") as ff:
        ff.write(contents)

def trainDT(X,Y,cols,symbol_vars):
    clftree = tree.DecisionTreeClassifier(criterion='entropy',max_depth=8,class_weight="balanced",min_impurity_split=0.1)
    """model=clftree
    rfe = RFE(model, X.shape[1])
    X_rfe = rfe.fit_transform(X[train_choice,:],Y[train_choice,:])
    print(rfe.support_)
    print(rfe.ranking_)
    clftree = clftree.fit(X_rfe,Y[train_choice,:])"""
    clftree = clftree.fit(X,Y)
    import graphviz
    out_filename='train-1.dot'
    tree.export_graphviz(clftree, out_file=out_filename)
    print("score",clftree.score(X,Y))
    interpretable('train-1.dot',cols)
    embed()

def train(X,Y,cols,symbol_vars):
    d=X.shape[-1]
    feature_combination=[]
    for sym in symbol_vars:
        print(sym)
        if len(symbol_vars[sym])>0:
            feature_combination.append(symbol_vars[sym])
    #feature_combination.append([d-1])
    feature_combination.append(symbol_vars["s"]+symbol_vars["salt"])
    feature_combination.append(symbol_vars["I"]+symbol_vars['Ialt'])
    feature_combination.append(symbol_vars["s"]+symbol_vars["c"])
    feature_combination.append(symbol_vars["salt"]+symbol_vars["c"])
    feature_combination.append(symbol_vars["I"]+symbol_vars["c"])
    feature_combination.append(symbol_vars["Ialt"]+symbol_vars["c"])
    #feature_combination.append(range(d)) #np.arange(d).reshape([d,1]).tolist()+[range(d)] #[0],[1],[2],[0,1],[0,2],[1,2],
    #[symbols["P"],symbols["COFF"],symbols["SOFF"],symbols["SIZE"],symbols["COFF"]+symbols["SOFF"]+symbols["SIZE"],symbols["S"]+symbols["S'"]] #[0],[1],[2],[0,1],[0,2],[1,2],
    tree= SVCTree(0,4,feature_combination,model='linear',cols=cols) #SGDClassifier
    #embed()
    print("start")
    tree.build_svc(X,Y,level=6,base_acc=min_score)
    print ("end")
    tree.export_to_dot("%s.dot"%args.outname)
    interpretable("%s.dot"%args.outname,cols)
    embed()

#main("cache-8.numpy.npz",None)
import argparse
if __name__=="__main__":
    parser = argparse.ArgumentParser(description='match symbol')
    parser.add_argument('files',metavar='files',type=str,nargs="+",help='same file, diff file')
    parser.add_argument('--outname',metavar='outname',type=str,default="out_train",help='outname')
    args=parser.parse_args()
    if len(args.files)==1:
        main(args.files[0],None)
    else:
        main(args.files[0],args.files[1])
