

class tbl():
    
    def __init__(self):
        123
        

    def window2(self): 
        345                                            # <===
        


import cv2, re
import numpy as np
from sklearn.linear_model import SGDClassifier
from joblib import dump, load
from time import sleep
from pandas import DataFrame
from functions import scrn, getscore, getld
import os
import mss

try:
    from PIL import Image
except ImportError:
    import Image


class tbl():
    
    def fit(self,flist):
        ar=[]
        Y=[]
        for fl in flist:
            temp=cv2.imread(fl,0).reshape(-1,)
            ar.append(temp)
            Y.append(re.search( '/.*/(.*)/', fl).group(1) )
        ar=np.array(ar)
            
        sgd_clf = SGDClassifier(max_iter=500)
        self.sgd=sgd_clf.fit(ar, Y)
    def save(self, fname='sgd.joblib'):
        dump(self.sgd, fname) 
        
    def load(self, fname='sgd.joblib'):
        self.sgd=load(fname) 
        
    def predict(self, x):
        self.sgd.predict(x)
          
    def getl(self):
        #find params for images
        with mss.mss() as sct:
            sleep(3)
            test = sct.shot(output='fullscreen.png')
        pr=cv2.imread(test,0) 
        os.remove(test)
        
        
    def gettbl(self,ts=4, save=False):
        self.tbl=DataFrame(columns=np.arange(4), index=np.arange(4))
        sleep(ts)
        for i in range(4):
            for j in range(4):
                test=scrn(i,j)
                pr=cv2.imread(test,0) 
                if not save:
                    os.remove(test)
                pr=self.sgd.predict(pr.reshape(1,-1) )[0]
                if pr=='np.nan':
                    self.tbl.iloc[i,j]=np.nan
                else:
                    self.tbl.iloc[i,j]=float(pr)
        self.tbl=self.tbl.astype(float)
        
        
        
        
class score():
    
    def fit(self,flist):
        ar=[]
        Y=[]
        for fl in flist:
            temp=cv2.imread(fl,0).reshape(-1,)
            ar.append(temp)
            Y.append(re.search( '/.*/(.*)/', fl).group(1) )
        ar=np.array(ar)
            
        sgd_clf = SGDClassifier(max_iter=500)
        self.sgd=sgd_clf.fit(ar, Y)
    def save(self, fname='score.joblib'):
        dump(self.sgd, fname) 
        
    def load(self, fname='score.joblib'):
        self.sgd=load(fname) 
        
    def predict(self, score='', maxlength=15,  sleep=5):
        if score=='':
            score=getscore(sleep=sleep)
        
        color=[187, 173, 160]
        colorcol=np.array([[color]*19]).astype('uint8')
        ld=getld(score)
        score=''
        for j in ld:
            temp=np.concatenate( (j, np.repeat( [colorcol], maxlength-len(j) , axis=1)[0]))   
            temp=np.reshape(f.arflat(temp), [-1,maxlength,3], order='F')
            Image.fromarray(temp).convert("RGB").save('temp.png')
            temp=cv2.imread('temp.png',0)
            score=score+(self.sgd.predict(temp.reshape(1,-1))[0])
            os.remove('temp.png')
        self.score=score
          
    def getl(self):
        #find params for images
        with mss.mss() as sct:
            sleep(3)
            test = sct.shot(output='fullscreen.png')
        pr=cv2.imread(test,0) 
        os.remove(test)
        
        
    def gettbl(self,ts=4, save=False):
        self.tbl=DataFrame(columns=np.arange(4), index=np.arange(4))
        sleep(ts)
        for i in range(4):
            for j in range(4):
                test=scrn(i,j)
                pr=cv2.imread(test,0) 
                if not save:
                    os.remove(test)
                pr=self.sgd.predict(pr.reshape(1,-1) )[0]
                if pr=='np.nan':
                    self.tbl.iloc[i,j]=np.nan
                else:
                    self.tbl.iloc[i,j]=float(pr)
        self.tbl=self.tbl.astype(float)
    