from tkinter import *
import tkinter.messagebox as msgbox
import time
import threading
import random
import keyboard
import mouse
import sqlite3

conn = sqlite3.connect('settings.db')
cursor = conn.cursor() # 커서 생성
try:
    cursor.execute("CREATE TABLE settings (name text PRIMARY KEY, way text, key text, clicker text)")
except:
    pass

def _start_autoclicker():
    global CPS_start, CPS_end, ms_start, ms_end, autoclicker_key
    msgbox.showinfo("Info", "Autoclicker started.")
    CPS_from, CPS_to = CPS_start.get(), CPS_end.get()
    if CPS_from > CPS_to:
        CPS_to = CPS_from
        CPS_end.delete(0, len(CPS_end.get()))
        CPS_end.insert(1, CPS_to)
        CPS_from, CPS_to = CPS_start.get(), CPS_end.get()
    
    MS_from, MS_to = ms_start.get(), ms_end.get()
    if MS_from > MS_to:
        MS_to = MS_from
        ms_end.delete(0, len(ms_end.get()))
        ms_end.insert(1, MS_to)
        MS_from, MS_to = ms_start.get(), ms_end.get()
    
    macro_key = autoclicker_key.get()
    
    while True: # 무한반복
        autoclicker_activated = True
        if keyboard.is_pressed("/"): # /키(채팅)이 눌렸을 때는 오토클리커가 작동하지 않도록 하기
            autoclicker_activated = False
            while not keyboard.is_pressed("enter"):
                pass         
            autoclicker_activated = True
            
        elif keyboard.is_pressed(macro_key) and autoclicker_activated:
            if macro_with.get() == 0:
                CPS = random.randint(int(float(CPS_from)*100), int(float(CPS_to)*100)) / 100
                start = time.time()
                mouse.click()
                end = time.time()
                time.sleep(abs((1 / CPS)-(end-start)))
            else:
                ms = random.randint(int(MS_from), int(MS_to))
                start = time.time()
                mouse.click()
                end = time.time()
                time.sleep(abs((ms / 1000)-(end-start)))

def start_autoclicker():
    thread = threading.Thread(target=_start_autoclicker)
    thread.daemon = True
    thread.start()

def stop_autoclicker():
    exit(0)
    
def save_settings():
    global cursor, setting_name, macro_with, conn, autoclicker_key
    if macro_with.get() == 0:
        global CPS_start, CPS_end
        name = setting_name.get()
        way = 'CPS'
        clicker = f'({CPS_start.get()},{CPS_end.get()})'
    else:
        global ms_start, ms_end
        name = setting_name.get()
        way = 'ms'
        clicker = f'({ms_start.get()},{ms_end.get()})'
    key = autoclicker_key.get()
    try:
        cursor.execute(f"INSERT INTO settings VALUES ('{name}', '{way}', '{key}', '{clicker}')")
    except:
        cursor.execute(f"UPDATE settings SET name='{name}', way='{way}', key='{key}', clicker='{clicker}'")
    conn.commit()

def convert(fetchalled: list[str]):
    name, way, key = fetchalled[0], fetchalled[1], fetchalled[2]
    clickers = fetchalled[3].split(',')
    for idx in range(len(clickers)):
        clickers[idx] = clickers[idx].replace('(', '').replace(')', '')
    return name, way, key, clickers

def load_settings():
    global setting_name, cursor, conn
    name = setting_name.get()
    cursor.execute(f"SELECT * FROM settings WHERE name='{name}'")
    all = cursor.fetchall()
    print(all)
    name, way, key, clickers = convert(all[0])
    if way == "CPS":
        global CPS_start, CPS_end
        CPS_start.delete(0, len(CPS_start.get()))
        CPS_start.insert(1, clickers[0])
        CPS_end.delete(0, len(CPS_end.get()))
        CPS_end.insert(1, clickers[1])
        CPS_radio.select()
    else:
        global ms_start, ms_end
        ms_start.delete(0, len(CPS_start.get()))
        ms_start.insert(1, clickers[0])
        ms_end.delete(0, len(CPS_end.get()))
        ms_end.insert(1, clickers[1])
        MS_radio.select()
    autoclicker_key.delete(0, len(autoclicker_key.get()))
    autoclicker_key.insert(1, key)
    conn.commit()
    
window = Tk('Autoclicker')
window.title('Autoclicker')
window.geometry("400x350+530+200")
window.resizable(False, False)

macro_with = IntVar()

macro_with_label = Label(window, text='매크로 방식을 선택하세요.')
macro_with_label.place(x=10, y=10)

CPS_radio = Radiobutton(window, text='CPS', value=0, variable=macro_with)
CPS_radio.select()
CPS_radio.place(x=30, y=30)

MS_radio = Radiobutton(window, text='MS', value=1, variable=macro_with)
MS_radio.place(x=100, y=30)

CPS_start_label = Label(window, text='CPS From : ')
CPS_start_label.place(x=10, y=80)
CPS_start = Entry(window)
CPS_start.insert(1, '22.96')
CPS_start.place(x=80, y=80)

CPS_end_label = Label(window, text='CPS To : ')
CPS_end_label.place(x=10, y=100)
CPS_end = Entry(window)
CPS_end.insert(1, '22.96')
CPS_end.place(x=80, y=100)

ms_start_label = Label(window, text='MS From : ')
ms_start_label.place(x=10, y=145)
ms_start = Entry(window)
ms_start.insert(1, '71')
ms_start.place(x=80, y=145)

ms_end_label = Label(window, text='MS To : ')
ms_end_label.place(x=10, y=165)
ms_end = Entry(window)
ms_end.insert(1, '71')
ms_end.place(x=80, y=165)

autoclicker_key_label = Label(window, text='Autoclicker Key : ')
autoclicker_key_label.place(x=10, y=200)
autoclicker_key = Entry(window)
autoclicker_key.insert(1, 'CapsLock')
autoclicker_key.place(x=120, y=200)

start_button = Button(window, text='Start', width=7, command=start_autoclicker)
start_button.place(x=330, y=320)

stop_button = Button(window, text="Stop", width=7, command=stop_autoclicker)
stop_button.place(x=270, y=320)

setting_name = Entry(window, width=10)
setting_name.place(x=115, y=280)

setting_name_label = Label(window, text="Name of setting : ")
setting_name_label.place(x=10, y=280)

save_button = Button(window, text='Save', width=7, command=save_settings)
save_button.place(x=330, y=280)

load_button = Button(window, text='Load', width=7, command=load_settings)
load_button.place(x=270, y=280)

window.mainloop()
conn.close()
