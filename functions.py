#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 16:00:44 2018

@author: ainur
"""
import time
from pynput.keyboard import Key, Controller
import numpy as np
import os
import re
from pandas import DataFrame


from datetime import datetime
import mss.tools
import mss

try:
    from PIL import Image
except ImportError:
    import Image

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(x,*args, **kwargs):
        return x


def getflist(path='./data/numbers',exclude_prefixes =('__', '.')):  # exclusion prefixes):
    flist = list()
    for (dirpath, dirnames, filenames) in os.walk(path):
        flist += [os.path.join(dirpath, file) for file in filenames
              if not file.startswith(exclude_prefixes)]
    return(flist)

def getfit(flist, max_iter=500):
    from sklearn.linear_model import SGDClassifier
    ar=[]
    Y=[]
    for fl in flist:
        temp=np.array(Image.open(fl).convert('L')).reshape(-1,)
#        temp=cv2.imread(fl,0).reshape(-1,)
        ar.append(temp)
#        re.search( '/(.*)/', fl).group(1) if fl doesnt start with ./
        Y.append(re.search( '/.*/(.*)/', fl).group(1) )
    ar=np.array(ar)
        
    sgd_clf = SGDClassifier(max_iter=max_iter)
    sgd_clf.fit(ar, Y)
    return(sgd_clf)
        
#from itertools import product
def getkey(M):
    keys=[Key.right, Key.down, Key.up, Key.left]    
    cols=['k1','k2','s','nanc', 's0']
    solutions=DataFrame(columns=cols)
    for k1 in [Key.right, Key.down, Key.up]   :
        temp=M.copy(deep=True)
        temp2=nt(temp,k1)
        if (not temp2.equals(M) ):
            temp2=temp2.apply(np.log2)
            temp2=temp2.sum().sum()
#            print(temp2)
            for k2 in keys:
    #            temp=M.copy(deep=True)
                temp=nt(nt(temp,k1),k2)
                temp=temp.apply(np.log2)
                stemp=temp.sum().sum()
                
                counttemp=nancount(temp)
                solutions=solutions.append(DataFrame([[k1,k2,stemp,counttemp, temp2]],
                                                     columns=cols),ignore_index=True)
    solutions=solutions.loc[ solutions.s==solutions.s.min(),:]
    solutions=solutions.loc[ solutions.nanc==solutions.nanc.min(),:]
    solutions.loc[solutions.s0==solutions.s0.min(),:]
    if len (solutions)==0:
        k1=Key.left
    else:
        k1=solutions.iloc[0,0]
    return(k1)

def mv(k):
    keyboard = Controller()
    keyboard.press(k)
    keyboard.release(k)
    return(True)
    


def scrn (n,m,l1=107,l2=15,top=335, left=556):
    with mss.mss() as sct:
        # The screen part to capture
#        monitor = {"top": 335+l2+n*(l1+l2), "left": 581+l2+m*(l1+l2), \
#                   "width": l1, "height": l1}
        monitor = {"top": 335+l2+n*(l1+l2), "left": 581+l2+m*(l1+l2), \
                   "width": l1, "height": l1}
        
        out = str(n)+'*'+str(m)+str(datetime.now().time())+".png".format(**monitor)
        # Grab the data
        sct_img = sct.grab(monitor)
        # Save to the picture file
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=out)
#        print(out)
        return(out)
        
#next predicting
def nt (m, key):
    if key==Key.down:
        m=rotated(m)
    elif key==Key.right:
        m=rotated(rotated(m))
    elif key==Key.up:
        m=rotated(rotated(rotated(m)))
    for i in range(4):        
        temp=m.loc[i, list(map(lambda x: ~np.isnan(x), m.loc[i,:] )) ]
        temp=np.asarray(temp)
        if len(temp)>1:
            j=0
            while j <(len(temp)-1) :
#                print(i,j, temp)
                if temp[j]==temp[j+1]:
                    temp=np.concatenate( (temp[0:j],float(2*temp[j]),temp[(j+2):] ), axis=None)
                j=j+1
        temp=np.asarray(temp).astype(float)
        m.loc[i,:]=np.full(4,np.nan)
        m.loc[i,:(len(temp)-1)]=temp
    if key==Key.up:
        m=rotated(m)
    elif key==Key.right:
        m=rotated(rotated(m))
    elif key==Key.down:
        m=rotated(rotated(rotated(m)))
    return(m)
    
def rotated(df):
    cols=df.columns
    df=df.T.reset_index().reindex(columns=np.arange(3,-1,-1)) 
    df.columns=cols
    return(df )
    
from functools import reduce
def nancount(M):
    return(np.count_nonzero(~np.isnan(reduce(lambda a, x: a + x, (M.values).tolist()))))

def getpredict(sgd_clf_score,score='', maxlength=15,  sleep=5):
    if score=='':
        score=getscore(sleep=sleep)
    color=[187, 173, 160]
    colorcol=np.array([[color]*19]).astype('uint8')
    ld=getld(score)
    score=''
    for j in ld:
        temp=np.concatenate( (j, np.repeat( [colorcol], maxlength-len(j) , axis=1)[0]))   
        temp=np.reshape(arflat(temp), [-1,maxlength,3], order='F')
        Image.fromarray(temp).convert("RGB").save('temp.png')
        temp=cv2.imread('temp.png',0)
        score=score+(sgd_clf_score.predict(temp.reshape(1,-1))[0])
        os.remove('temp.png')
    return(score)

pright=710
ptop=185
pwidth=100
pheight=19

def getscore(sleep=5,pright=pright,ptop=ptop,pwidth=pwidth,pheight=pheight):    
    time.sleep(sleep)
    with mss.mss() as sct:
        # The screen part to capture
        monitor = {"top": ptop, "left": pright-pwidth, "width": pwidth, "height": pheight}
        output = "temp/"+str(datetime.now().time()).format(**monitor)
    
        # Grab the data
        sct_img = sct.grab(monitor)
    
        # Save to the picture file
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        print(output)
    return(output)
    
#if the column consist of one color
def monocol(col):
#    l=len(col)
    for i in col:
        for j in range(3):
            if i[j]!=col[0][j]:
                return (False)
    return (True)

from itertools import chain
def arflat(temp):
    temp=[k for k in temp]
    temp= list(chain(*temp))
    return(temp)

pright=910
ptop=185
pwidth=100
pheight=19
def getld(file, pheight=pheight):
    img = Image.open(file)
    arr = np.array(img)
#    temp=np.reshape(arflat(arr), [-1,pheight,3], order='F')
    temp=np.reshape(arflat(arr), [-1,len(arr),3], order='F')

    digits=0
    previous=monocol(temp[0])
    layer=1
    ld=[]
    ld.append([])
    while layer!=(len(temp)):
        current=monocol(temp[layer])
        if (current!=previous) & current:
            digits=digits+1
            ld.append([])
        if not current:
            ld[digits].append(temp[layer])
        previous=current
        layer=layer+1
    del ld[digits]
    return(ld)







