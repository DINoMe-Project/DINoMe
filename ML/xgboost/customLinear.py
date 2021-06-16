import numpy as np
from scipy.optimize import minimize, basinhopping
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import VarianceThreshold
from IPython import embed
import matplotlib.pyplot as plt
from sklearn.cluster import SpectralClustering
#import tensorflow as tf
import functools
from sklearn.svm import LinearSVC
from sklearn import preprocessing
from sklearn.utils.class_weight import *

import pandas as pd
def mean_absolute_percentage_error(y_pred, y_true, sample_weights=None):
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    assert len(y_true) == len(y_pred)
    if np.any(y_true==0):
        print("Found zeroes in y_true. MAPE undefined. Removing from set...")
        idx = np.where(y_true==0)
        y_true = np.delete(y_true, idx)
        y_pred = np.delete(y_pred, idx)
        if type(sample_weights) != type(None):
            sample_weights = np.array(sample_weights)
            sample_weights = np.delete(sample_weights, idx)

    if type(sample_weights) == type(None):
        return(np.mean(((y_pred - y_true +1)*0.5 / y_pred)) * 100)
    else:
        sample_weights = np.array(sample_weights)
        assert len(sample_weights) == len(y_true)
        return(100/sum(sample_weights)*np.dot(
                sample_weights, (((y_pred - y_true +1)*0.5 / y_pred))
        ))
def normalize_numeric_data(data, mean, std):
  # Center the data
  return (data-mean)/std
def localloss(data,y_pred):
	y_true=data[:,0]


class CustomLinearModel:
    """
    Linear model: Y = XB, fit by minimizing the provided loss_function
    with L2 regularization
    """
    def __init__(self, loss_function=mean_absolute_percentage_error,
                 X=None, Y=None, sample_weights=None, beta_init=None,
                 regularization=0.00012):
        self.regularization = regularization
        self.beta = None
        self.loss_function = loss_function
        self.sample_weights = sample_weights
        self.beta_init = beta_init

        self.X = X
        self.Y = Y


    def predict(self, X):
        prediction = np.matmul(X, self.beta)
        return(prediction)

    def model_error(self):
        error = self.loss_function(
            self.predict(self.X), self.Y, sample_weights=self.sample_weights
        )
        return(error)

    def l2_regularized_loss(self, beta):
        self.beta = beta
        return(self.model_error() + \
               sum(self.regularization*np.array(self.beta)**2))

    def fit(self, maxiter=250):
        # Initialize beta estimates (you may need to normalize
        # your data and choose smarter initialization values
        # depending on the shape of your loss function)
        if type(self.beta_init)==type(None):
            # set beta_init = 1 for every feature
            self.beta_init = np.array([1]*self.X.shape[1])
        else:
            # Use provided initial values
            pass

        if self.beta!=None and all(self.beta_init == self.beta):
            print("Model already fit once; continuing fit with more itrations.")
        #res = basinhopping(self.l2_regularize_loss)
        res = minimize(self.l2_regularized_loss, self.beta_init,
                       method='BFGS', options={'maxiter': maxiter})
        self.beta = res.x
        self.beta_init = self.beta

"""l2_mape_model = CustomLinearModel(
    loss_function=mean_absolute_percentage_error,
    X=X, Y=Y, regularization=0.00012
)
l2_mape_model.fit()
l2_mape_model.beta"""

class LinearFeature:
	def __init__(self):
		self.clf=None
	def show(self):
		plt.scatter(self.X, self.Y, color = "red")
		plt.plot(x_train, lr.predict(x_train), color = "green")
	def data2midpoints(self,data,xdata):
		min_max_scaler = preprocessing.MinMaxScaler()
		#data_scaled = min_max_scaler.fit_transform(data)
		data_scaled=(data*1.0-data.min()).div(data.max()-data.min())
		midpoints=pd.DataFrame(columns=xdata.columns)
		for attribute in xdata.columns:
			data_scaled=data_scaled.sort_values([attribute])
			z=data_scaled.iloc[1:,:]
			z.index=z.index-1
			candidates=(z.to_numpy()+data_scaled.iloc[0:-1,].to_numpy())/2
			candidates=candidates[candidates[:,0]==0.5][:,1:]
			midpoints=midpoints.append(pd.DataFrame(candidates,columns=xdata.columns),ignore_index=True,sort=False)
		return midpoints
	def fit(self,pddata,NStep=100,thresDis=0.2):
            selector = VarianceThreshold()
            selector.fit(pddata)
            drop=pddata.columns[selector.get_support()==False]
            pddata.drop(columns=drop)
            Xdata=pddata.iloc[:,1:]
            Ydata=pddata.iloc[:,0:1]
            X=self.X=Xdata.to_numpy()
            y=self.y=Ydata.to_numpy()
            nSample=y.shape[0]
            #clf = LogisticRegression(random_state=0,penalty='l1',multi_class='ovr',class_weight="balanced",solver='liblinear')
            #clf.fit(self.X, self.y)
            #minc=np.min(np.abs(clf.coef_))
            #maxc=np.max(np.abs(clf.coef_))
            #idx=np.where(abs(clf.coef_)>(maxc-minc)*0.2+minc)[1]
            trueIdx=np.where(y==1)[0]
            falseIdx=np.where(y==0)[0]
            data_scaled=(pddata-pddata.min()).div(pddata.max()-pddata.min())
            midpoints=self.data2midpoints(pddata,Xdata)
            anchors=midpoints.sample(NStep)
            sample_weight=compute_sample_weight('balanced',y)
            regs=[]
            self.anchors=anchors
            for point in anchors.to_numpy():
                dis=(data_scaled.iloc[:,1:]-point)
                dis=(dis*dis).sum(axis=1)
                #idx=np.argsort(dis)
                #subsample_weight=np.copy(sample_weight)
                #subsample_weight=subsample_weight/dis.to_numpy()
                #nSubSample=int(0.2*nSample)
                #subsample_weight[idx[:nSubSample]]=0
                #dis<0.2,1,0
                #subsample_weight=subsample_weight*np.where(dis<thresDis,1,0)
                local_index=np.where(dis<thresDis)
                local_x=X[local_index]
                local_y=y[local_index]
                local_sample_weight=compute_sample_weight('balanced',local_y)
                #reg=LogisticRegression()
                #LinearSVC()
                reg=LinearSVC(penalty='l1',loss='squared_hinge',dual=False,C=4,max_iter=400,tol=0.001)
                try:
                    reg.fit(local_x,local_y,sample_weight=local_sample_weight)
                except Exception:
                    continue
                score=reg.score(local_x,local_y,sample_weight=local_sample_weight)
                globalscore=reg.score(X,y,sample_weight=sample_weight)
                regs.append([reg,score,globalscore,reg.coef_,reg.intercept_,local_sample_weight,local_y.shape,point])
            self.regs=regs
            """
            clf2 = LogisticRegression(random_state=0,penalty='elasticnet',l1_ratio=0.5,multi_class='ovr',class_weight="balanced",solver='saga' )
            #clf2=CustomLinearModel()
            clf2.fit(X[:,idx],y)
            pY=clf2.predict(X[:,idx])
            leftIdx=np.where(pY==1)[0]
            rightIdx=np.where(pY==0)[0]
            self.left_data=pddata.iloc[leftIdx]
            self.right_data=pddata.iloc[rightIdx]
            self.clf=clf
            self.clf2=clf2
            """
            #self.idx=idx
            self.feature_name=pddata.columns[1:]
	def fitNext(self):
		lf=None
		rf=None
		if self.left_data.Y.unique().shape[0]==2:
			lf=LinearFeature()
			lf.fit(self.left_data)
		if self.right_data.Y.unique().shape[0]==2:
			rf=LinearFeature()
			rf.fit(self.right_data)
		return lf,rf
	def features(self,threshold=0.7):
		features={}
		added={}
		nfeature=0
		toremove=set()
		def distance(coef1,coef2):
			return np.sum((coef1-coef2)*(coef1-coef2))
		for reg,score,globalscore,coef,intercept,weight,nsample,point in self.regs:
			#coef=self.clf2.coef_[0]
			if score<threshold:
				continue
			coef=coef[0]
			print(coef)
			#intercept=self.clf2.intercept_
			feature=""
			csum=np.sum(np.abs(coef))
			coef=coef/(csum)
			coef=-coef if coef[0]<0 else coef
			for i in range(coef.shape[0]):
				if i>0 and coef[i]>0:
					feature=feature+"+%2f*%s"%(coef[i],self.feature_name[i])
				else:
					feature=feature+"%2f*%s"%(coef[i],self.feature_name[i])
			featurename="L_%d"%nfeature
			nfeature=nfeature+1
			added[featurename]=np.sum(self.X*coef,axis=1);
			features[featurename]=(score,globalscore,nsample,feature,point,coef)
		for name in features:
			if name in toremove:
				continue
			coef=features[name][-1]
			score=features[name][0]
			for name2 in features:
				if name<=name2:
					continue
				if name2 in toremove:
					continue
				coef2=features[name2][-1]
				score2=features[name2][0]
				d=distance(coef,coef2)
				print("distance",name,name2,d)
				if d>0.04:
					continue
				best=features[name] if score>score2 else features[name2]
				features[name]=best
				features[name2]=best
				toremove.add(name)
		for name in toremove:
			print("remove",features[name])
			del features[name]
			del added[name]
		return features,added

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='match symbol')
    parser.add_argument('files',metavar='files',type=str,nargs="+",help='same file, diff file')
    parser.add_argument('--debug',type=bool,default=False,help='decision rule depth')
    parser.add_argument('--depth',type=int,default=10,help='decision rule depth')
    parser.add_argument('--outname',type=str,default="xgboost_1",help='outname')
    parser.add_argument('--label',type=int,default=0,help='label value')
    args=parser.parse_args()
    if len(args.files)==1:
        x,y,feature_names,symbol_vars=prepare_data(args.files[0])
    else:
        x,y,feature_names,symbol_vars=prepare_data(samedata_file,diffdata_file)
