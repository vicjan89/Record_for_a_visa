from pyautogui import alert, position, click, hotkey, prompt, locateOnScreen, locateCenterOnScreen, write, press
import pyautogui
import pyperclip
from PIL import Image
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
    THERE_ARE_PLACES = 6
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
        run = True
        while run:
            for i in range(1,13):
                x,y = locateCenterOnScreen('static/select_city_check.png')
                click(x + 250, y)  # выбор визового центра
                sleep(2)
                click(locateCenterOnScreen('static/' + str(i) + '.png'))  # нажимаем на визовый центр
                sleep(3)
                if locateOnScreen('static/no_sits.png'):
                    print(datetime.now(), 'Нет мест в центре ' + str(i), file=self.log)
                else:
                    run = False
                    self.status = self.THERE_ARE_PLACES
                    break
            if run:
                for i in tqdm(range(600)):
                    sleep(1)

    def check_status(self):
        click(50, 300)
        sleep(2)
        hotkey('ctrl', 'a')
        sleep(2)
        hotkey('ctrl', 'c')
        s = pyperclip.paste()
        click(50, 300)
        if 'You are now in line' in s:
            self.status = self.NOT_WORK
        elif locateOnScreen('static/select_sity.png'):
            if self.status == self.THERE_ARE_PLACES:
                playsound.playsound('signal-gorna-na-obed.mp3')
            else:
                self.status = self.FIND_VISA
        elif locateOnScreen('static/schedule_appointment_rus.png'):
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
        print(self.address)
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
                if self.status == self.ENTER_ADDRESS:
                        print(datetime.now(), 'Ввод адреса сайта.', self.address, file=self.log)
                        self.enter_address()
                        print(datetime.now(), 'Адреса сайта введён.', file=self.log)
                elif self.status == self.NOT_WORK:
                        print(datetime.now(), 'Сайт ожидает очереди.', file=self.log)
                        self.wait_site_work()
                        print(datetime.now(), 'Очередь подошла.', file=self.log)
                elif self.status == self.AUTORIZATION:
                        print(datetime.now(), 'Авторизация.', file=self.log)
                        self.autorization()
                        print(datetime.now(), 'Конец авторизации.', file=self.log)
                elif self.status == self.FIND_VISA:
                        print(datetime.now(), 'Начало поиска визового центра со свободными местами.', file=self.log)
                        self.find_visa()
                        print(datetime.now(), 'Конец поиска визового центра со свободными местами.', file=self.log)
                elif self.status == self.SELECT_FIND_VISA:
                        print(datetime.now(), 'Выбор меню поиска визового центра.', file=self.log)
                        self.select_find_visa()
                        print(datetime.now(), 'Выбрано меню поиска визового центра.', file=self.log)

def split_image(image_name, num):
    image = Image.open(image_name)
    size_image = image.size
    step = int(size_image[1]/num)
    name = 1
    for i in range(0, size_image[1], step):
        image_new = image.crop((0,i,size_image[0],i+step))
        image_new.save('static/' + str(name) + '.png')
        name += 1


fv = Find_visa('Coordinates', ADDRESS)
fv.load_calibration()
fv.run()

