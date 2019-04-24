import numpy as np
#from sklearn.linear_model import SGDClassifier
from joblib import dump, load
from time import sleep
from pandas import DataFrame
from functions import getscore, getld, getflist, getfit, getGamePixels
import os
import mss
import mss.tools
from datetime import datetime
import shelve
try:
    from PIL import Image
except ImportError:
    import Image

class state():
    def __init__(self):
        self.load()
        shelf = shelve.open("./.conf/props.txt", flag='r')
        for key in shelf.keys():
            self.props = shelf[key]
            #do something with it
        shelf.close()

    def fit(self,folder='./data/gamestate'):
        flist=getflist(folder)
        self.stateSgd=getfit(flist, max_iter=600)
        
    def save(self, fname='./.conf/state.joblib'):
        dump(self.stateSgd, fname) 
        
    def load(self, fname='./.conf/state.joblib'):
        self.stateSgd=load(fname)
        return self.stateSgd
      
    # def predict_on_img(self, fl):
    #     array=Image.open(fl).convert('L')
    #     return (self.sgd.predict(array.reshape(1,-1))[0] )
        
    def statepredict(self, save=False,folder='./'):
        with mss.mss() as sct:
            # l1,l2 =107, 15
            # top, left =335, 581
            # monitor = {"top": top, "left": left, \
            #            "width": 4*l1+5*l2, "height": 4*l1+5*l2}
            
            # l1,l2 =107, 16
            # top, left =game.props['top']['l1']['starts']-l2, 581
            
            s=0
            for i in range(3):
                s=s+self.props['top']['l'+str(i+1)]['starts']-self.props['top']['l'+str(i)]['ends']
                s=s+self.props['left']['l'+str(i+1)]['starts']-self.props['left']['l'+str(i)]['ends']
            dif=int(round (s/6))
            monitor = {"top": self.props['top']['l0']['starts']-dif, 
                       "left": self.props['left']['l0']['starts']-dif, 
                       "width": self.props['left']['l3']['ends']-\
                       self.props['left']['l0']['starts']+2*dif,
                       "height": self.props['top']['l3']['ends']-\
                       self.props['top']['l0']['starts'] +2*dif}
            
            
            
            sct_img=sct.grab(monitor)
            
            if save:
                img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
                img=img.resize( (500,500) )
                output=folder+str(datetime.now())+".png".format(**monitor)
                img.save(output)
                # mss.tools.to_png(sct_img.rgb, sct_img.size,
                #     )
            sc=Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX").convert('L') 
            sc=np.array(sc.resize( (500,500) ) )
            
            self.now=self.stateSgd.predict(sc.reshape(1,-1))[0]
            return(self.now)
            
    def getprops(self, save=False):
        #some notes of using this
        import random
        from pynput.keyboard import Listener, Key
        keys= [Key.right,Key.down,Key.up,Key.left,]
        global tempy, tempx
        tempx=np.array([])
        tempy=np.array([])
        def on_release(key):
            if key == Key.esc:
    ##        Stop listener
                return (False)
    
        def on_press(key):
            global tempy
            global tempx
            from functions import mv
            if key == Key.enter:
                mv(random.choice(keys))
                sleep(1)
                with mss.mss() as sct:
                    temp = sct.grab(sct.monitors[0])
                    temp=Image.frombytes("RGB", temp.size, \
                    temp.bgra, "raw", "BGRX").convert('L')
                    temp=np.array(temp)
                    temp2=np.array(Image.fromarray( temp.flatten().reshape(-1,1050, order='F') ) )
                    temp2=list(map(sum,temp2))
                    temp=list(map(sum,temp))

                    if len(tempy)==0:
                        tempy=np.array([temp])
                        tempx=np.array([temp2])
                    else:
                        tempy=np.append(tempy,[temp], axis=0)
                        tempx=np.append(tempx,[temp2], axis=0)

                    
                return (True)
        with Listener(
            on_press=on_press,
            on_release=on_release) as listener:
                listener.join()
        qy=getGamePixels(tempy)
        qx=getGamePixels(tempx)
        
        props={}
        top={}
        left={}
        n=0
        left['l'+str(n)]={}
        left['l'+str(n)]['starts']=qx[0]

        top['l'+str(n)]={}
        top['l'+str(n)]['starts']=qy[0]
        prev=qy[0]
        
        for i in qy[1:]:
            if i!=prev+1:
                top['l'+str(n)]['ends']=prev
                n=n+1
                top['l'+str(n)]={}
                top['l'+str(n)]['starts']=i
            prev=i
        top['l'+str(n)]['ends']=i
        props['top']=top
        
        n=0
        prev=qx[0]
        for i in qx[1:]:
            if i!=prev+1:
                left['l'+str(n)]['ends']=prev
                n=n+1
                left['l'+str(n)]={}
                left['l'+str(n)]['starts']=i
            prev=i
        left['l'+str(n)]['ends']=i
        props['left']=left

        if save:
            shelf = shelve.open("./.conf/props.txt", flag="w")
            shelf['key1']=props
            shelf.close()
        self.props=props
        
        
        return (props)

class tbl(state):
    def __init__(self,state):
        self.stateSgd=state.stateSgd
        super().__init__()
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
          
    def gettbl(self,ts=0.05, save=False, folder='./'):
#        firsttime=True
        if hasattr(self, 'tbl'): #ввести аргумент чекинг
#            firsttime=False
            self.prev=self.tbl
        self.tbl=DataFrame(columns=np.arange(4), index=np.arange(4))
        sleep(ts)
#        l1,l2 =107, 15
#        top, left=337, 581
        with mss.mss() as sct:
            for i in range(4):
                for j in range(4):
                    monitor = {"top": self.props['top']['l'+str(i)]['starts'], 
                                "left": self.props['left']['l'+str(j)]['starts'], 
                                "width": self.props['left']['l'+str(j)]['ends'] - self.props['left']['l'+str(j)]['starts'] ,
                                "height": self.props['top']['l'+str(i)]['ends'] - self.props['top']['l'+str(i)]['starts']}
                    
                   #  monitor = {"top": top+l2+i*(l1+l2), "left": left+l2+j*(l1+l2), \
                   # "width": l1, "height": l1}
                   
                    
                    sct_img=sct.grab(monitor)
                    if save:
                        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
                        img=img.resize( (107,107) )
                        output=folder+str(datetime.now())+".png".format(**monitor)
                        img.save(output)

                    #     img = folder+str(i)+'*'+str(j)+str(datetime.now())+".png".format(**monitor)
                    #     mss.tools.to_png(sct_img.rgb, sct_img.size, output=img)
                    n=Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX").convert('L')
                    n=n.resize( (107,107) )
                    n=np.array(n)
                    n=self.sgd.predict(n.reshape(1,-1) )[0]
                    if n=='np.nan':
                        self.tbl.iloc[i,j]=np.nan
                    else:
                        self.tbl.iloc[i,j]=float(n)
        self.tbl=self.tbl.astype(float)
        return (self.tbl)
        

    
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
      #      temp=np.reshape(f.arflat(temp), [-1,maxlength,3], order='F')
            Image.fromarray(temp).convert("RGB").save('temp.png')
    #        temp=imread('temp.png',0)
            score=score+(self.sgd.predict(temp.reshape(1,-1))[0])
            os.remove('temp.png')
        self.score=score
          
    def getl(self):
        #find params for images
        with mss.mss() as sct:
            sleep(3)
            test = sct.shot(output='fullscreen.png')
     #   pr=cv2.imread(test,0) 
        os.remove(test)
        
        
    def sc(self,ts=4, save=False):
        self.tbl=DataFrame(columns=np.arange(4), index=np.arange(4))
        sleep(ts)
        for i in range(4):
            for j in range(4):
                scr=sum([i,j])
                pr=Image.open(scr).convert('L')
                
                #pr=imread(scr,0) 
                if not save:
                    os.remove(scr)
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
            # The screen part to capture
            monitor = {"top": ptop, "left": pright-pwidth, "width": pwidth, "height": pheight}
            if fname=='':
                fname = "temp/"+str(datetime.now()).format(**monitor)
        
            # Grab the data
            sct_img = sct.grab(monitor)
        
            # Save to the picture file
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=fname)
        return(fname)