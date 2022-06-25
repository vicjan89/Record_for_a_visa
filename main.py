import pyautogui
import pyperclip
import playsound
import time
import datetime
import smtplib
import os
from tqdm import tqdm

EMAIL_FROM = os.getenv('EMAIL_FROM')
PASSWORD_FROM = os.getenv('PASSWORD_FROM')
EMAIL_TO = os.getenv('EMAIL_TO')

def wait_dawnload():
    s = ''
    while 'Apply for VISA' not in s:
        pyautogui.click(923, 195, clicks=3)
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'c')
        s = pyperclip.paste()


time.sleep(5)
pyautogui.FAILSAFE = True

while True:
    for i in range(212,537,25):
        pyautogui.click(818, 537) #выбор визового центра
        time.sleep(2)
        pyautogui.click(818, i) #нажимаем на визовый центр
        wait_dawnload()
        pyautogui.click(818, 564, clicks=3) #проверка наличия мест
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'c')
        buffer = pyperclip.paste()
        if 'no open seats' in buffer:
            print(datetime.datetime.now(),buffer)
        else:
            print('Ура, есть места!')
            playsound.playsound('signal-gorna-na-obed.mp3', True)
            smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
            smtpObj.starttls()
            smtpObj.login(EMAIL_FROM, PASSWORD_FROM)
            smtpObj.sendmail(EMAIL_FROM, EMAIL_TO, 'Hooray! There are places for a visa!')
            smtpObj.quit()
            input()
    for i in tqdm(range(300)):
        time.sleep(1)

