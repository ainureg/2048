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
    temp=cv2.imread(fl,0).reshape(11449,)
    ar.append(temp)
    Y.append(re.search( '/.*/(.*)/', fl).group(1) )
ar=np.array(ar)
    
from sklearn.linear_model import SGDClassifier
sgd_clf = SGDClassifier(max_iter=500)
sgd_clf.fit(ar, Y)

import time






M=f.getM(sgd_clf)
M.copy(deep=True)

while True:
    time.sleep(1)
    k=Key.up
    s=2**100
    for key in [Key.right, Key.down, Key.up, Key.left]:
        if s>np.nanprod(f.nextt(M, key).values):
            s=np.nanprod(f.nextt(M, key).values)
            k=key
    f.mv(k, 1)
    M=f.getM(sgd_clf, 0.5)
    M.copy(deep=True)
    
    
    
    
    
    

with Listener(
        on_press=f.on_press,
        on_release=f.on_release) as listener:
    listener.join()
