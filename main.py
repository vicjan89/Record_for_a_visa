from pyautogui import Point, alert, position, click, hotkey
import pyautogui
import pyperclip
import playsound
import time
import datetime
import smtplib
import os
from tqdm import tqdm
import json

EMAIL_FROM = os.getenv('EMAIL_FROM')
PASSWORD_FROM = os.getenv('PASSWORD_FROM')
EMAIL_TO = os.getenv('EMAIL_TO')

coords = {'check_site_download':[Point(923,195), 'Наведите мышь на надпись Apply for VISA to POLAND'],
          'select_center':[Point(818, 537), 'Наведите мышь на поле выбора визового центра']}

def calibrate():
    title = 'Калибровка сайта'
    alert(text='Начинается сохранение координат полей и надписей сайта. После наведения на запрошиваемый объект нажимайте на клавиатуре Ввод/Enter')
    for value in coords.values():
        alert(text=value[1], title=title, button='Ok')
        value[0] = position()
    with open('Coordinates.json', 'w', encoding='utf-8') as file:
        json.dump(coords, file, indent=4, ensure_ascii=False)

def load_calobration():
    with open('Coordinates.json', 'r', encoding='utf-8') as file:
        return json.load(file)


def send_email():
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login(EMAIL_FROM, PASSWORD_FROM)
    smtpObj.sendmail(EMAIL_FROM, EMAIL_TO, 'Hooray! There are places for a visa!')
    smtpObj.quit()

def wait_dawnload():
    s = ''
    while 'Apply for VISA' not in s:
        click(coords['check_site_download'], clicks=3)
        time.sleep(2)
        hotkey('ctrl', 'c')
        s = pyperclip.paste()


coords = load_calobration()

time.sleep(5)
pyautogui.FAILSAFE = True
wait_dawnload()
while True:
    for i in range(212,537,25):
        click(coords['select_center']) #выбор визового центра
        time.sleep(2)
        click(818, i) #нажимаем на визовый центр
        wait_dawnload()
        click(818, 564, clicks=3) #проверка наличия мест
        time.sleep(2)
        hotkey('ctrl', 'c')
        buffer = pyperclip.paste()
        if 'no open seats' in buffer:
            print(datetime.datetime.now(),buffer)
        else:
            click(622, 398, clicks=3)  # проверка наличия мест
            time.sleep(2)
            hotkey('ctrl', 'c')
            buffer = pyperclip.paste()
            if 'no open seats' in buffer:
                print(datetime.datetime.now(), buffer)
            else:
                print('Ура, есть места!')
                playsound.playsound('signal-gorna-na-obed.mp3', True)
                input()
    for i in tqdm(range(300)):
        time.sleep(1)

