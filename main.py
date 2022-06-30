from pyautogui import alert, position, click, hotkey, prompt, ImageNotFoundException, locateCenterOnScreen, write, press
import pyautogui
import pyperclip
import playsound
from time import sleep
from datetime import datetime, timedelta
import smtplib
import os
from tqdm import tqdm
import json

EMAIL_FROM = os.getenv('EMAIL_FROM')
PASSWORD_FROM = os.getenv('PASSWORD_FROM')
EMAIL_TO = os.getenv('EMAIL_TO')
ADDRESS = 'https://row2.vfsglobal.com/PolandBelarus-Appointment/Account/RegisteredLogin?q=shSA0YnE4pLF9Xzwon/x/ASnHZRMROGDyz5YljrTPrmD7weWKDzHm/9+x4kyou3TsMOg99oc+0bfYTDhNi8VXO2A4zs7wBkyB6b15tURU2eT0aS3CJYjFGR6LRWzfcsZ5BzitruEIjN+SeHc17EKqO0YlhR3T0Pc1cO5uD69/WY='


class Find_visa:

    NOT_WORK = 1
    AUTORIZATION = 2
    SELECT_FIND_VISA = 3
    FIND_VISA = 4
    ENTER_ADDRESS = 5
    LOG = 'my.log'

    def __init__(self, name_file, address):
        self.name_file = name_file
        self.status = 0
        self.address = address

    def calibrate_and_save(self):
        title = 'Калибровка сайта'
        alert(text='Начинается сохранение координат полей и надписей сайта. После наведения на запрошиваемый объект нажимайте на клавиатуре Ввод/Enter')
        for value in self.coords.values():
            if not isinstance(value, int):
                alert(text=value[1], title=title, button='Ok')
                value[0] = position()
        self.coords['num_centers'] = int(prompt(text='Введите количество визовых центров', title=title))
        with open(self.name_file + '.json', 'w', encoding='utf-8') as file:
            json.dump(self.coords, file, indent=4, ensure_ascii=False)

    def load_calibration(self):
        with open(self.name_file + '.json', 'r', encoding='utf-8') as file:
            self.coords = json.load(file)

    def send_email(self):
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.starttls()
        smtpObj.login(EMAIL_FROM, PASSWORD_FROM)
        smtpObj.sendmail(EMAIL_FROM, EMAIL_TO, 'Hooray! There are places for a visa!')
        smtpObj.quit()

    def wait_dawnload(self):
        s = ''
        t = datetime.now()
        while s == '':
            click(50,300)
            hotkey('ctrl', 'a')
            sleep(1)
            hotkey('ctrl', 'c')
            s = pyperclip.paste()
            click(50, 300)
            if (datetime.now()-t) > timedelta(minutes=5):
                break

    def wait_site_work(self):
        sleep(5)
        run = True
        while run:
            click(766,160, clicks=3)
            sleep(5)
            hotkey('ctrl', 'a')
            sleep(1)
            hotkey('ctrl', 'c')
            s = pyperclip.paste()
            if 'Your estimated wait time' not in s:
                run = False

    def find_visa(self):
        sleep(5)
        pyautogui.FAILSAFE = True
        self.wait_dawnload()
        step = int((self.coords['last_center'][0][1]-self.coords['first_center'][0][1])/(self.coords['num_centers']-1))
        stop = False
        while True:
            for i in range(self.coords['first_center'][0][1], self.coords['last_center'][0][1], step):
                click(self.coords['select_center'][0])  # выбор визового центра
                sleep(2)
                click(self.coords['first_center'][0][0], i)  # нажимаем на визовый центр
                self.wait_dawnload()
                hotkey('ctrl', 'a')
                sleep(1)
                hotkey('ctrl', 'c')
                buffer = pyperclip.paste()
                if 'no open seats' in buffer:
                    text_to_log = buffer.split('Centre')
                    text_to_log = text_to_log[1].split('Appointment Category')
                    text_to_log = text_to_log[0]
                    print(datetime.now(), text_to_log, file=self.log)
                elif 'Нет доступных мест' in buffer:
                    text_to_log = buffer.split('Нет доступных мест в выбранном Визовом Центре')
                    text_to_log = text_to_log[1].split('Категория Записи')
                    text_to_log = text_to_log[0]
                    print(datetime.now(), 'Нет доступных мест в выбранном Визовом Центре' + text_to_log[:-2], file=self.log)
                else:
                    stop = True
            if stop:
                break
            for i in tqdm(range(300)):
                sleep(1)

    def check_status(self):
        self.wait_dawnload()
        click(50, 300)
        sleep(2)
        hotkey('ctrl', 'a')
        sleep(2)
        hotkey('ctrl', 'c')
        s = pyperclip.paste()
        click(50, 300)
        if 'You are now in line' in s:
            self.status = self.NOT_WORK
        elif 'Apply for VISA' in s or 'Подача документов на визу' in s:
            if 'Select Centre' in s or 'Выбрать город' in s:
                self.status = self.FIND_VISA
            else:
                self.status = self.SELECT_FIND_VISA
        elif 'Электронная почта' in s:
            self.status = self.AUTORIZATION
        elif 'Invalid session. Kindly logout and click appointment click from vfsglobal.com site' in s or (
            'Please visit https://www.vfsglobal.com/ site then select -> Visiting Country' in s):
            self.status = self.ENTER_ADDRESS
        else:
            self.status = self.ENTER_ADDRESS

    def autorization(self):
        sleep(2)
        click(locateCenterOnScreen('static/capcha.png'))
        sleep(5)
        click(locateCenterOnScreen('static/next.png'))
        sleep(5)

    def select_find_visa(self):
        sleep(5)
        coords = locateCenterOnScreen('static/schedule_appointment.png')
        if coords != None:
            click(coords)
        else:
            coords = locateCenterOnScreen('static/schedule_appointment_rus.png')
            if coords != None:
                click(coords)
            else:
                print(datetime.now(), 'Не нашёл пункт меню "Запись на подачу документов".', self.log)
        sleep(5)


    def enter_address(self):
        click(self.coords['address_box'][0])
        write(self.address)
        sleep(3)
        press('enter')
        sleep(7)

    def run(self):
        sleep(5)
        with open(self.LOG, 'a', encoding='utf-8') as self.log:
            run = True
            while run:
                self.check_status()
                match self.status:
                    case self.ENTER_ADDRESS:
                        print(datetime.now(), 'Ввод адреса сайта.', self.address, file=self.log)
                        self.enter_address()
                        print(datetime.now(), 'Адреса сайта введён.', file=self.log)
                    case self.NOT_WORK:
                        playsound.playsound('signal-gorna-na-obed.mp3', True)
                        print(datetime.now(), 'Сайт ожидает очереди.', file=self.log)
                        self.wait_site_work()
                        print(datetime.now(), 'Очередь подошла.', file=self.log)
                    case self.AUTORIZATION:
                        playsound.playsound('signal-gorna-na-obed.mp3', True)
                        print(datetime.now(), 'Авторизация.', file=self.log)
                        self.autorization()
                        print(datetime.now(), 'Конец авторизации.', file=self.log)
                    case self.FIND_VISA:
                        playsound.playsound('signal-gorna-na-obed.mp3', True)
                        print(datetime.now(), 'Начало поиска визового центра со свободными местами.', file=self.log)
                        self.find_visa()
                        print(datetime.now(), 'Конец поиска визового центра со свободными местами.', file=self.log)
                    case self.SELECT_FIND_VISA:
                        playsound.playsound('signal-gorna-na-obed.mp3', True)
                        print(datetime.now(), 'Выбор меню поиска визового центра.', file=self.log)
                        self.select_find_visa()
                        print(datetime.now(), 'Выбрано меню поиска визового центра.', file=self.log)



fv = Find_visa('Coordinates', ADDRESS)
fv.load_calibration()
fv.run()

