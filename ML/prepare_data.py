import numpy as np
from sklearn.feature_selection import RFE, VarianceThreshold,SelectKBest, chi2
from sklearn.svm import SVR
from IPython import embed
import pandas as pd
import datetime
def getSymVar(columns):
    symbol_vars={"c":[],"I":[],"Ialt":[],"s":[],"salt":[]}
    for offset,sym_name in enumerate(columns):
        all=sym_name.split("_")
        label=all[0]
        index=all[1]
        symbol_vars[label].append(offset)
    return symbol_vars
def prepare_data(samedata_file,diffdata_file):
    if diffdata_file==None:
        data=pd.read_csv(samedata_file)
        return (data[data.columns[2:]].to_numpy(),data["Y"].to_numpy(),data.columns[2:],getSymVar(data.columns[2:]))
    same_data=pd.read_csv(samedata_file,header=None)
    same_data.insert(0, 'Y', [0]*len(same_data))
    diff_data=pd.read_csv(diffdata_file,header=None)
    diff_data.insert(0, 'Y', [1]*len(diff_data))
    #same_data=np.genfromtxt(samedata_file,filling_values=2,delimiter=",")
    #diff_data=np.genfromtxt(diffdata_file,filling_values=2,delimiter=",")
    data=pd.concat([same_data,diff_data])
    onerow=data[0:1].to_numpy();
    d=onerow.shape[-1]
    split_index=np.unique(np.where(onerow==' ')[1])
    assert(split_index.shape[0]>2)
    widths=split_index[0:5]-np.concatenate((np.array([0]),split_index[:-1]))[0:5]
    widths=widths-1
    cols=["Y"]
    colnames=["c","I","Ialt","s","salt"]
    for i,w in enumerate(widths):
        cols=cols+["%s_%d"%(colnames[i],j) for j in range(w)]
        cols.append("none")
    while len(cols)<d:
        cols.append("none")
    data.columns=cols
    del data["none"]
    select=VarianceThreshold(0.00001)
    #np.random.shuffle(x)
    #np.random.shuffle(y)
    select.fit(data)
    #select=RFE(chi2, k=20)
    index=np.where(select.get_support())[0]
    now = datetime.datetime.now()
    index=list(set(index)-set([0]))
    x=data.ix[:,index]
    to_del_index=list(set(range(data.shape[-1]))-set([0])-set(index))
    data.drop(data.columns[to_del_index],axis=1,inplace=True)
    #del data.ix[:,to_del_index]

    data.to_csv(now.strftime("%Y_%m_%d_%H_%M_%S.csv"))
    return (x.to_numpy(),data["Y"].to_numpy(),x.columns,getSymVar(x.columns))
