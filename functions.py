#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 16:00:44 2018

@author: ainur
"""
import time
from pynput.keyboard import Key, Controller
import numpy as np
globvar=True
keyboard = Controller()
def on_release(key):
    global globvar
    if key == Key.esc:
#        Stop listener
        globvar=False
        return False
    
def on_press(key):
    global globvar
    if key == Key.enter:
        if globvar:
            times=20
            tm=0
            for i in range (times):
                mv(Key.right,tm)
                mv(Key.right,tm)
                mv(Key.down,tm)
    return True
        

def mv(k,tm=0.01):
    keyboard.press(k)
    keyboard.release(k)
    time.sleep(tm)
    return(0)
    
    
from datetime import datetime
import mss.tools
import mss

def scrn (n,m,l1=107,l2=15):
    with mss.mss() as sct:
        # The screen part to capture
        monitor = {"top": 335+l2+n*(l1+l2), "left": 581+l2+m*(l1+l2), \
                   "width": l1, "height": l1}
        out = str(n)+'*'+str(m)+str(datetime.now().time())+".png".format(**monitor)
        
        # Grab the data
        sct_img = sct.grab(monitor)
        
        # Save to the picture file
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=out)
        print(out)
        return(out)

def nextt (m, key):
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
                    temp=np.concatenate( (temp[0:j],2*temp[j],temp[(j+2):] ), axis=None)
                j=j+1
                    
        temp=np.asarray(temp)
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
    
#    
#def mvline(a):
# 


def justify(a, invalid_val=0, axis=1, side='left'):    
    """
    Justifies a 2D array

    Parameters
    ----------
    A : ndarray
        Input array to be justified
    axis : int
        Axis along which justification is to be made
    side : str
        Direction of justification. It could be 'left', 'right', 'up', 'down'
        It should be 'left' or 'right' for axis=1 and 'up' or 'down' for axis=0.

    """

    if invalid_val is np.nan:
        mask = ~np.isnan(a)
    else:
        mask = a!=invalid_val
    justified_mask = np.sort(mask,axis=axis)
    if (side=='up') | (side=='left'):
        justified_mask = np.flip(justified_mask,axis=axis)
    out = np.full(a.shape, invalid_val) 
    if axis==1:
        out[justified_mask] = a[mask]
    else:
        out.T[justified_mask.T] = a.T[mask.T]
    return out