import os 
import sys
import numpy as np
from IPython import embed
import pandas as pd
def summaryJ3(data):
    avg=data.mean()
    return 1-(avg['c1'])/(avg['c3']+avg['c2']-avg['c1'])

def summaryJ2(data):
    return ((data['c2']-data['c1'])/data['c2']).mean()
    avg=data.mean()
    return (avg['c2']-avg['c1'])/avg['c2']

def summaryDknown(data):
    return ((data['c3']-data['c1'])/data['c3']).mean()
    avg=data.mean()
    return (avg['c3']-avg['c1'])/avg['c3']

def summaryDknown2(data):
    avg=data.mean()
    return (avg['c2']-avg['c1'])/avg['c2']
def summaryD(data):
    return ((data['c3']-data['c1'])/data['c2']).mean()
    avg=data.mean()
    return (avg['c3']-avg['c1'])/avg['c2']

def summaryJ(data):
    fn=None
    if len(L)<6:
        fn=summaryJ2
    else:
        fn=summaryJ3
    return fn(data)

if __name__=="__main__":
    filename= sys.argv[1]
    mode =sys.argv[2]
    L=[]
    min_hash=10000000
    id=None
    sumj=0
    nj=0
    ncount=2
    if mode=="declass":
        summary=summaryD
        ncount=3
    elif mode=="known":
        ncount=3
        summary=summaryDknown
    else:
        summary=summaryJ
    data=pd.read_csv(filename,delimiter='\t',header=-1)
    c=[]
    for i in range(1,1+ncount):
        c.append("c%d"%i)
        c.append("h%d"%i)
    c=c+['na1','na2']
    data.columns=c
    data=data.query("c2>0")

    for i in range(1, 1+ncount):
        data['h%d'%i]=data['h%d'%i]*data['c%d'%i]/data['c%d'%i]
    hash=data.iloc[:,[i*2+1 for i in range(0,ncount)]]
    minhash=hash.min(axis=1)
    for i in range(1, 1+ncount):
        data['c%d'%i]=data['c%d'%i]*((data['h%d'%i]-minhash).rpow(2))
        data['c%d'%i] =data['c%d'%i].fillna(0)
        data['h%d'%i]=minhash
    
    print("invalid data =",data.query("c2<c1").shape)
    data=data.query("c2>=c1 ")
    #data=data[~data['na2'].str.contains("t")]

    j=summary(data)

    #print("avg:",data.mean())
    print(j)
