from pynput.keyboard import Listener, Key, Controller
import os
from time import sleep
from functions import mv, mem#,gotmove 
from classes2048 import state, score, tbl

from mss import mss
import mss.tools as msstools
from datetime import datetime

#global globvar


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
    if key == Key.enter:
#        while globvar:
#    if key == Key.esc:
#        return False      
        
        try:
            while True:
                k=mem(t.tbl)
                mv(k, 0)
                t.gettbl(ts=0)
                #print(k,'\n___________________\n')
        except:
            
            with mss() as sct:
                sleep(10)
                l1,l2 =107, 15
                top, left =335, 381
                monitor = {"top": top, "left": left, \
"width": 4*l1+5*l2, "height": 4*l1+5*l2}
                
                img = './data/gamestate/lost/'+str(datetime.now().time())+".png".format(**monitor)
                sct_img = sct.grab(monitor)
                msstools.to_png(sct_img.rgb, sct_img.size, output=img)
                keyboard.press(Key.f5)
                keyboard.release(Key.f5)
                print('Проигрыш'+ str( datetime.now().time() ) +'\n________________')
                sleep(10)
                t.gettbl(ts=0)
                on_press(Key.enter)
            
    return True



#CPU times: user 377 ms, sys: 2.96 ms, total: 380 ms
#Wall time: 369 ms
#Out[56]: <Key.up: <65362>>

#def mem1(M):
#    keys=[Key.right, Key.down, Key.up, Key.left]    
#    cols=['k1','k2','s','nanc', 's0']
#    solutions=DataFrame(columns=cols)
#    for k1,k2 in product(keys,keys):
#        temp=M.copy(deep=True)
#        temp2=nt(temp,k1).apply(np.log2)
#        temp=nt(nt(temp,k1),k2)
#        temp=temp.apply(np.log2)
#        stemp=temp.sum().sum()
#        temp2=temp2.sum().sum()
#        counttemp=nancount(temp)
#        solutions=solutions.append(DataFrame([[k1,k2,stemp,counttemp, temp2]],
#                                             columns=cols),ignore_index=True)
#
#    
#    solutions=solutions.loc[ solutions.s==solutions.s.min(),:]
#    solutions=solutions.loc[ solutions.nanc==solutions.nanc.min(),:]
#    solutions.loc[solutions.s0==solutions.s0.min(),:]
#    k1=solutions.iloc[0,0]
#
#    return(k1)
    
    



if __name__ == "__main__":
    os.chdir('/home/ainur/Desktop/Codes/Python/problems/2048/')
    sc=score()
    sc.load()
    t=tbl()
    t.load()
    t.gettbl(ts=0)
#    sleep(3)
    globvar=True
    keyboard = Controller()
    with Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        
        
        print('still running...')
        listener.join()
#        while globvar:
#            sleep(0.1)
#            if not listener.running:
#                break
        



    




