from pynput.keyboard import Listener, Key, Controller
import os
#from datetime import datetime
#import functions as f
from time import sleep
from functions import gotmove, mv
from classes import tbl
from classes import score

#global globvar


def on_release(key):
    global globvar
    if key == Key.esc:
##        Stop listener
#        globvar=False
#        from sys import exit
#        exit()
        return False
    
def on_press(key):
    global t
#    global globvar
    if key == Key.enter:
#        while globvar:
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
            sleep(0.1)
            if not listener.running:
                break
        



    




