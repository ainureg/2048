import pandas as pd
import numpy as np
#try:
#    from PIL import Image
#except ImportError:
#    import Image

import re

from pynput.keyboard import Listener, Key
import os
os.chdir('/home/ainur/Desktop/Codes/Python/2048/')
#from datetime import datetime
import functions as f
import cv2


flist = list()
for (dirpath, dirnames, filenames) in os.walk('./data'):
    flist += [os.path.join(dirpath, file) for file in filenames]

ar=[]
Y=[]
for fl in flist:
    #print(fl)
    temp=cv2.imread(fl,0).reshape(11449,)
    ar.append(temp)
    Y.append(re.search( '/.*/(.*)/', fl).group(1) )
ar=np.array(ar)
    
from sklearn.linear_model import SGDClassifier
sgd_clf = SGDClassifier(max_iter=500)
sgd_clf.fit(ar, Y)

#import time





M=f.getM(sgd_clf)
#tempM=M.copy(deep=True)


while True:
    s=2**100
    for key in [Key.right, Key.down, Key.up, Key.left]:
        tempM=M.copy(deep=True)
        tempM=f.nt(tempM,key)
#        print(tempM)
        print(s,np.nanprod(tempM.values) ,f.nancount(tempM), f.nancount(M),np.nanprod(tempM.values) ,(not tempM.equals(M) ) )
        print(( (   (f.nancount(tempM) <= f.nancount(M) ) &\
            (s>=np.nanprod(tempM.values) )  )  & (not tempM.equals(M) ) ))
        if ((  ( f.nancount(tempM) <= f.nancount(M) ) &\
            (s>=np.nanprod(tempM.values) )  )  & (not tempM.equals(M) ) ):
            s=np.nanprod(tempM.values)
            k=key
    print(k)
    f.mv(k, 0.2)
    M=f.getM(sgd_clf, 0.001)
    

    
    
    
    

with Listener(
        on_press=f.on_press,
        on_release=f.on_release) as listener:
    listener.join()
