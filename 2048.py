from pynput.keyboard import Listener, Key, Controller
import os
from time import sleep
from functions import mv, getkey#,gotmove 
from classes2048 import state, tbl# score, 

#from mss import mss
#import mss.tools as msstools
from datetime import datetime

#global globvar


def on_release(key):
    global globvar
    if key == Key.esc:
##        Stop listener
#        globvar=False
        return False
    
def on_press(key):
    global t
    global game
    ts=0.22
    t.gettbl(ts=ts)
    if key == Key.enter:
        while game.predict()=='going':
            k=getkey(t.tbl)
            mv(k)
            t.gettbl(ts=ts)
            if (t.tbl.sum().sum()-t.prev.sum().sum() ) not in [0,2,4]:
                print('wrong gettbl')
                print('prev\n',t.prev,'\ntbl', t.tbl, '\n')
                
                folder='./temp/'+str(datetime.now())+'/'
                os.mkdir(folder)
                t.gettbl(save=True, folder=folder)
                t.prev.to_csv(folder+'prev', header='None', index='None', sep='\t')  
                t.tbl.to_csv(folder+'tbl', header='None', index='None', sep='\t')  
                game.predict(save=True,folder=folder)
                print('Плохая таблица тут '+ folder +'\n________________')
                
                int(input('\ninput for pause'))
                sleep(3)
                #print(k,'\n___________________\n')
            
#        if (game.now!='going'):
#            temp=int(input('\ninput for pause'))
#            sleep(1)
            
        folder='./temp/'+str(datetime.now())+'/'
        os.mkdir(folder)
        t.gettbl(save=True, folder=folder)
        t.prev.to_csv(folder+'prev', header='None', index='None', sep='\t')  
        t.tbl.to_csv(folder+'tbl', header='None', index='None', sep='\t')  
        game.predict(save=True, folder=folder)
        print('Проигрыш тут'+ folder +'\n________________')           
#            with mss() as sct:
#                sleep(3)
#                l1,l2 =107, 15
#                top, left =335, 381
#                monitor = {"top": top, "left": left, \
#"width": 4*l1+5*l2, "height": 4*l1+5*l2}
#                img = './temp/'+str(datetime.now())+".png".format(**monitor)
#                sct_img = sct.grab(monitor)
#                msstools.to_png(sct_img.rgb, sct_img.size, output=img)
        keyboard.press(Key.f5)
        sleep(0.05)
        keyboard.release(Key.f5)
        sleep(2)

        on_press(Key.enter)
    return True

if __name__ == "__main__":
    os.chdir('/home/ainur/git/2048/')
#    sc=score()
#    sc.load()
    t=tbl()
#    globvar=True
    global game

    game=state()
    game.predict()
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
        



    




