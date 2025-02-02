import time
import win32api, win32con
from random import randint

HOLD_MS, RELEASE_MS = 50, 50
while True: # 무한반복
    if win32api.GetKeyState(0x06) < 0:
        x, y = win32api.GetCursorPos()
        start = time.time()
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        end = time.time()
        time.sleep((HOLD_MS / 1000)-(end-start))
        start = time.time()
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        end = time.time()
        time.sleep((RELEASE_MS / 1000)-(end-start)) # 1 / (randint(1414, 1419) / 100)
        