#import pandas as pd
#import numpy as np
#import re
from pynput.keyboard import Listener, Key, Controller
import os
#os.chdir('/home/ainur/Desktop/Codes/Python/problems/2048/')

#from datetime import datetime
#import functions as f
from time import sleep
from functions import gotmove, mv
from classes import tbl
#t=tbl()
#t.load()


from classes import score
#sc=score()
#sc.load()
#sc.predict()
#sc.score























#just showing picture of an array






global globvar


def on_release(key):
    global globvar
    if key == Key.esc:
##        Stop listener
        globvar=False
#        from sys import exit
#        exit()
        return False
    
def on_press(key):
    global t
#    global globvar
 #   sleep(1)
    if key == Key.enter:
            with Listener(
            on_release=on_release) as listener:
                print('still running...')
        
                while globvar:
                    k=gotmove(t.tbl)
                    mv(k, 0)
                    t.gettbl(ts=0)
                    print(k,'\n___________________\n')
#    if key == Key.esc:
#        return False      
    
    return True





if __name__ == "__main__":
    os.chdir('/home/ainur/Desktop/Codes/Python/problems/2048/')
    sc=score()
    sc.load()
    t=tbl()
    t.load()
    t.gettbl()
    sleep(3)
    globvar=True
    keyboard = Controller()
    with Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        print('still running...')
        while globvar:
            #print('still running...')
            sleep(0.1)
            if not listener.running:
                break
        
    #    listener.join()
        



    




