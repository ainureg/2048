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

cols=['0','1','2','3']

M=pd.DataFrame(columns=np.arange(4), index=np.arange(4))
time.sleep(4)
for i in range(4):
    for j in range(4):
        test=f.scrn(i,j)
        
        pr=cv2.imread(test,0) 
        os.remove(test)
        pr=sgd_clf.predict(pr.reshape(1,-1) )[0]
        if pr=='np.nan':
            M.iloc[i,j]=np.nan
        else:
            M.iloc[i,j]=int(pr)




with Listener(
        on_press=f.on_press,
        on_release=f.on_release) as listener:
    listener.join()
