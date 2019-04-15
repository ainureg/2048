import cv2, re
import numpy as np
from sklearn.linear_model import SGDClassifier
from joblib import dump, load
from time import sleep
from pandas import DataFrame
from functions import scrn, getscore, getld, getflist, getfit
import os
import mss
import mss.tools
from datetime import datetime
try:
    from PIL import Image
except ImportError:
    import Image

class tbl():
    def __init__(self):
        self.load()
        
    def fit(self,folder='./data/numbers'):
        flist=getflist()
        self.sgd=getfit(flist, max_iter=1000)
        
    def save(self, fname='./.conf/sgd.joblib'):
        dump(self.sgd, fname) 
        
    def load(self, fname='./.conf/sgd.joblib'):
        self.sgd=load(fname) 
        
    def predict(self, x):
        self.sgd.predict(x)
          
    def getl(self):
        sleep(3)
        #find params for images
#        with mss() as sct:
            
#            test = sct.shot(output='fullscreen.png')
#        pr=cv2.imread(test,0) 
#        os.remove(test)
    
    def gettbl(self,ts=0.05, save=False, folder='./'):
#        firsttime=True
        if hasattr(self, 'tbl'): #ввести аргумент чекинг
#            firsttime=False
            self.prev=self.tbl
        self.tbl=DataFrame(columns=np.arange(4), index=np.arange(4))
        sleep(ts)
        l1,l2 =107, 15
        top, left=335, 581
        with mss.mss() as sct:
            for i in range(4):
                for j in range(4):
                    monitor = {"top": top+l2+i*(l1+l2), "left": left+l2+j*(l1+l2), \
                   "width": l1, "height": l1}
                    
                    sct_img=sct.grab(monitor)
                    if save:
                        img = folder+str(i)+'*'+str(j)+str(datetime.now())+".png".format(**monitor)
                        mss.tools.to_png(sct_img.rgb, sct_img.size, output=img)
                    
                    n=Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX").convert('L')
                    n=np.array(n)
                    
#                    n = np.array(sct_img)
#                    n=cv2.cvtColor( n, cv2.COLOR_BGR2GRAY)
                    n=self.sgd.predict(n.reshape(1,-1) )[0]
                    if n=='np.nan':
                        self.tbl.iloc[i,j]=np.nan
                    else:
                        self.tbl.iloc[i,j]=float(n)
                                #pr=imread(img,0) 
                    
                    
##                    n=split(np.array(sct.grab(monitor)) )[0]
#                    
#                    #both work and nice                    
#                    n = np.array(sct.grab(monitor))
#                    n=cv2.cvtColor( n, cv2.COLOR_BGR2GRAY)
#
#                    
#                    n=self.sgd.predict(n.reshape(1,-1) )[0]
#                    if n=='np.nan':
#                        self.tbl.iloc[i,j]=np.nan
#                    else:
#                        self.tbl.iloc[i,j]=float(n)
#                    if save:
#
#                        img = folder+str(i)+'*'+str(j)+str(datetime.now())+".png".format(**monitor)
#                        sct_img = sct.grab(monitor)
#                        mss.tools.to_png(sct_img.rgb, sct_img.size, output=img)
#                        #pr=imread(img,0) 
        self.tbl=self.tbl.astype(float)
        return (self.tbl)
        

    
    
class state():
    def __init__(self):
        self.load()
    
    def fit(self,folder='./data/gamestate'):
        flist=getflist()
        self.sgd=getfit(flist, max_iter=600)
        
    def save(self, fname='./.conf/state.joblib'):
        dump(self.sgd, fname) 
        
    def load(self, fname='./.conf/state.joblib'):
        self.sgd=load(fname) 
      
    def predict_on_img(self, fname):
        sc=imread(fname,0)
        return (self.sgd.predict(sc.reshape(1,-1))[0] )
        
    def predict(self, save=False,folder='./'):
        with mss.mss() as sct:
            l1,l2 =107, 15
            top, left =335, 581
            monitor = {"top": top, "left": left, \
                       "width": 4*l1+5*l2, "height": 4*l1+5*l2}
            
            #n=split(np.array(sct.grab(monitor)) )[0]
#            sc=sct.grab(monitor)
#            if save:
#                mss.tools.to_png(sc.rgb, sc.size,
#                        output=folder+str(datetime.now())+".png".format(**monitor))
#            sc = np.array(sc)
#            sc=cv2.cvtColor( sc, cv2.COLOR_BGR2GRAY) 
            sct_img=sct.grab(monitor)
            if save:
                mss.tools.to_png(sct_img.rgb, sct_img.size,
                    output=folder+str(datetime.now())+".png".format(**monitor))
            sc=np.array(Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX").convert('L') )
            

            self.now=self.sgd.predict(sc.reshape(1,-1))[0]
            return(self.now)
          
            
class score():
    def fit(self,folder='./data/score'):
        flist=getflist()
        self.sgd=getfit(flist, max_iter=500)
        
    def save(self, fname='./.conf/score.joblib'):
        dump(self.sgd, fname) 
        
    def load(self, fname='./.conf/score.joblib'):
        self.sgd=load(fname) 
        
    def predict(self, score='', maxlength=15,  sleep=5):
        if score=='':
            score=getscore(sleep=sleep)
        #вроде работает, но надо поправить
        color=[187, 173, 160]
        colorcol=np.array([[color]*19]).astype('uint8')
        #list of digits
        ld=getld(score)
        score=''
        for j in ld:
            temp=np.concatenate( (j, np.repeat( [colorcol], maxlength-len(j) , axis=1)[0]))   
            temp=np.reshape(f.arflat(temp), [-1,maxlength,3], order='F')
            Image.fromarray(temp).convert("RGB").save('temp.png')
            temp=imread('temp.png',0)
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
                pr=imread(test,0) 
                if not save:
                    os.remove(test)
                pr=self.sgd.predict(pr.reshape(1,-1) )[0]
                if pr=='np.nan':
                    self.tbl.iloc[i,j]=np.nan
                else:
                    self.tbl.iloc[i,j]=float(pr)
        self.tbl=self.tbl.astype(float)
    
    def capture(self, fname=''):
        #pright=910
        pright=710
        ptop=185
        pwidth=100
        pheight=19
        with mss.mss() as sct:
    
#    def getscore(sleep=5,pright=pright,ptop=ptop,pwidth=pwidth,pheight=pheight):    
#        time.sleep(sleep)
#        with mss.mss() as sct:
            # The screen part to capture
            monitor = {"top": ptop, "left": pright-pwidth, "width": pwidth, "height": pheight}
            if fname=='':
                fname = "temp/"+str(datetime.now()).format(**monitor)
        
            # Grab the data
            sct_img = sct.grab(monitor)
        
            # Save to the picture file
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=fname)
        return(fname)