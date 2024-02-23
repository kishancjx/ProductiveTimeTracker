#modules related to windows current process
import psutil
from ctypes import wintypes, windll
from typing import Optional
import ctypes



#tkinter related modules
import tkinter as tk
from tkinter import filedialog
from tkinter import Canvas
from tkinter.constants import BOTH
from tkinter.ttk import Label

#extra modules
import time
import sys
import os
import time as tm
import json


window=tk.Tk()
window.geometry('150x40')
window.title("kTimerX")

window.overrideredirect(True)

#initializing Some variables:
start_time = None
total_pause_time = 0
running = False
appdictionary={}
is_started = False
is_paused = False
is_resumed= False
is_reset = False
is_same = False
pausebyclick = False
resumebyclick=False


# This will Make the tkinter window borderless
# Basically , it will check every 100millisecond in a recursive way
# If the windows is normal( meaning not borderless) then it will make it borderless
# TODO: Make this Function more efficient (aka dont use this recursive loop of checking every 100millisecond)
def make_window_borderless():
    if window.state()== "normal":
        window.overrideredirect(True)  
    window.after(100,make_window_borderless)

    
# This Does Nothing
def test():
    print("TEST")

    
# Stopwatch related Functions:

## This Will Start the Timer
def start_timer():
    global is_started , is_paused , is_resumed , is_reset
    global start_time
    global running, start_time

    running = True
    is_started = True
    is_paused = False
    is_resumed = False
    is_reset = False

    start_time = tm.monotonic()
    update_timer()
    my_menu.entryconfig(0,state=tk.DISABLED)
    my_menu.entryconfig(1,state=tk.NORMAL)
    my_menu.entryconfig(3,state=tk.NORMAL)

## This will Stop the Timer , I mean Pause
def stop_timer():
    global running, pause_start_time, total_pause_time
    global is_paused , is_started, is_resumed , is_reset

    is_started=True
    is_paused = True
    is_resumed= False
    is_reset = False
    running = False
    pause_start_time = tm.monotonic()
    my_menu.entryconfig(1,state=tk.DISABLED)
    my_menu.entryconfig(2,state=tk.NORMAL)
    my_menu.entryconfig(3,state=tk.NORMAL)

## This will Resume the Timer
def resume_timer():    
    global running, start_time, pause_start_time
    global total_pause_time , is_paused, is_started, is_resumed , is_reset

    is_started=True
    is_paused = False
    is_resumed= True
    is_reset = False
    running = True
    pause_end_time = tm.monotonic()
    total_pause_time += (pause_end_time - pause_start_time)
    my_menu.entryconfig(2,state=tk.DISABLED)
    my_menu.entryconfig(1,state=tk.NORMAL)
    my_menu.entryconfig(3,state=tk.NORMAL)
    update_timer()


## This Will Reset the Timer
def reset_timer():
    global running, start_time, total_pause_time
    global is_paused, is_started, is_resumed , is_reset

    is_started=False
    is_paused = False
    is_resumed= False
    is_reset = True
    running = False
    start_time = None
    total_pause_time = 0
    running=False
    
    time_label.config(text="00:00:00")
    my_menu.entryconfig(0,state="active")
    my_menu.entryconfig(1,state="disabled")
    my_menu.entryconfig(2,state="disabled")
    my_menu.entryconfig(3,state="disabled")

## This will Update the values of the time on the GUI every second
def update_timer():
    global running, time_label, start_time, total_pause_time
    
    if running :
        elapsed_time = tm.monotonic() - start_time - total_pause_time
        time_string = tm.strftime('%H:%M:%S', tm.gmtime(elapsed_time))
        time_label.config(text=time_string)
    window.after(1000, update_timer)

# This will minimize the app    
def minimize():
    window.overrideredirect(False)
    window.state(newstate="iconic")



# This two functions will work only when it was paused by clicking
def stop_timer_byclick():
    global running, pause_start_time, total_pause_time
    global is_paused , is_started, is_resumed , is_reset
    running = False
    pause_start_time = tm.monotonic()
    my_menu.entryconfig(1,state=tk.DISABLED)
    my_menu.entryconfig(2,state=tk.NORMAL)
    my_menu.entryconfig(3,state=tk.NORMAL)
def resume_timer_byclick():    
    global running, start_time, pause_start_time, total_pause_time , is_paused, is_started, is_resumed , is_reset
    running = True
    pause_end_time = tm.monotonic()
    total_pause_time += (pause_end_time - pause_start_time)
    my_menu.entryconfig(2,state=tk.DISABLED)
    my_menu.entryconfig(1,state=tk.NORMAL)
    my_menu.entryconfig(3,state=tk.NORMAL)
    update_timer()




# In this function, I have added the ability to select my favourite(productivity) apps
# And after selecting it, it gets added into settings.json file.
def openapp():
    global userapppath
    global exactappname
    global appdictionary
        
    sub_menu=tk.Menu(my_menu, tearoff=False)
    app_path= tk.filedialog.askopenfilename()
    rfilepath= r"{"+str(app_path)+""
    appname=os.path.basename(rfilepath)
    userapppath=app_path
    exactappname=appname

    key=f"{exactappname}"
    value=f"{userapppath}"
    appdictionary[key]=value

    #this will write the apps which i choose in the settings.json
    with open("settinggg.json", "w") as j:
        json.dump(appdictionary,j, indent=2)
        j.close()


# This function will reset the settings.json
def resetapps():
        global appdictionary
        appdictionary={}
        with open("settinggg.json","w") as jt:
            jt.close()


# It will kill/close the tkinter window
def closetkinter():
    window.quit()

# This brings right click menu
def pop_rightCLick(click):
    my_menu.tk_popup(click.x_root, click.y_root)

# This function allows us to drag tkinter window, from clicking withing the window
def move(event):
    window.geometry(f'+{event.x_root}+{event.y_root}')


# Checks whether menuwasclicked
def buttonclick():
    global buttonwasclickedbro
    buttonwasclickedbro= True
    # print("button was clicked")


# TKINTER's MAIN MENU
my_menu= tk.Menu(window , tearoff=False)
my_menu.add_command(label="Start",command=lambda:[buttonclick(),start_timer()])
my_menu.add_command(label="pause",command=lambda:[buttonclick(), stop_timer_byclick()])
my_menu.add_command(label="Resume",command=lambda:[buttonclick(),resume_timer_byclick()])
my_menu.add_command(label="ResetTimer", command=reset_timer)
my_menu.add_command(label="AddNayaApp", command=openapp)
my_menu.add_command(label="ClearApps", command=resetapps)
my_menu.add_command(label="minimize", command=minimize)
my_menu.add_separator()
my_menu.add_command(label="BandKaro" , command=closetkinter)
my_menu.entryconfig(1,state="disabled")
my_menu.entryconfig(2,state="disabled")
my_menu.entryconfig(3,state="disabled")
window.bind("<Button-3>", pop_rightCLick)
window.bind('<B1-Motion>',move) 
my_menu.bind("<Button-1>", anotherTest)

# This code allow to stay on top (aka always on Top)
window.wm_attributes("-topmost",1)

# Displaying the Time
time_label=tk.Label(text="00:00:00", font=('Raleway',20))
time_label.pack()


# Loads everything from settings.json to the appdictionary variable
with open("settinggg.json","rt") as f:
    try:
        appdictionary=json.load(f )
        f.close()
    except:
        pass

# This applist function  contains the list of apps which i added.
def returnAddedAppsList():
    applist= list(appdictionary.keys())
    return applist

# Funtion to find the currentworking window:
def getForegroundWindowTitle() -> Optional[str]:
    hWnd = windll.user32.GetForegroundWindow()
    pid= wintypes.DWORD()
    windll.user32.GetWindowThreadProcessId(hWnd, ctypes.byref(pid))   
    return psutil.Process(pid.value).name()   

# This checks if currentrunning apps are in addedapps list
def appsamechecker():
    currentRunningApp= getForegroundWindowTitle()
    addedapps= returnAddedAppsList()
    addedapps.append("python.exe")  #this will add the tkinter window as a productivity app.
    addedapps.append("main.exe")  #this will add the tkinter window as a productivity app.
    global is_same
    if currentRunningApp in addedapps:
        is_same = True
    else:
        is_same= False
    window.after(1000,appsamechecker)
    # print(is_same)

# This will ensure that the timer is running or paused according to whether the person is productivity or not
def ensureTimer():
    global is_paused, is_started, is_resumed , is_reset , is_same
    global running
    if is_started :
        if is_same==False and running:
            running=False
            stop_timer()
        if is_paused and is_same:
            resume_timer()
    # print(is_same)
    window.after(1000,ensureTimer)



# FINALLY JUST RUNNING THE FUNCTIONS

## This will check if the currentrunning app is one of the selected productivity apps
appsamechecker()

## This will ensure the timer works correctly
test()

## This will check and make window borderless
make_window_borderless()

## This runs the tkinter mainloop
window.mainloop()
