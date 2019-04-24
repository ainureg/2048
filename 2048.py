from pynput.keyboard import Listener, Key, Controller
import os
from time import sleep
from datetime import datetime
os.chdir('/home/ainur/git/2048/')
from pandas import concat
from functions import mv, getkey#,gotmove 
from classes2048 import state, tbl# score, 

def on_release(key):
    global globvar
    if key == Key.esc:
##        Stop listener
#        globvar=False
        return False
    
def on_press(key):
    global t
    ts=0.25
    t.gettbl(ts=ts)
    if key == Key.enter:
        while t.statepredict()=='going':
            k=getkey(t.tbl)
            mv(k)
            t.gettbl(ts=ts)
            if (t.tbl.sum().sum()-t.prev.sum().sum() ) not in [0,2,4]:
                if str(input('\n pause\n type to save data (wrong tables)'))!='':
                    print('prev\n',t.prev,'\ntbl', t.tbl, '\n')
                    sleep(2)
                    folder='./temp/'+str(datetime.now())+'/'
                    os.mkdir(folder)
                    t.gettbl(save=True, folder=folder)
                    concat([t.tbl,t.prev,],keys=['cur', 'prev',]).to_csv(folder+'tbl', header='None', index='None', sep='\t')  
                    game.predict(save=True,folder=folder)
                    print('Плохая таблица тут '+ folder +'\n________________')
            
        folder='./temp/'+str(datetime.now())+'/'
        os.mkdir(folder)
        t.gettbl(save=True, folder=folder)
        concat([t.tbl,t.prev,],keys=['cur', 'prev',]).to_csv(folder+'tbl', header='None', index='None', sep='\t')  
                    
        game.predict(save=True, folder=folder)
        print('Проигрыш тут'+ folder +'\n________________')           
        keyboard.press(Key.f5)
        sleep(0.02)
        keyboard.release(Key.f5)
        sleep(2)

        on_press(Key.enter)
    return True

if __name__ == "__main__":
    os.chdir('/home/ainur/git/2048/')

#    globvar=True
    global game

    game=state()
    t=tbl(game)
    t.statepredict()
    keyboard = Controller()
    with Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        
        print('still running...')
        listener.join()
#            if not listener.running:
#                break
        



    





