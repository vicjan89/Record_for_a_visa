from pyautogui import click, hotkey, locateOnScreen, locateCenterOnScreen, typewrite, press, moveTo
import pyautogui
import pyperclip
from PIL import Image
import playsound
from time import sleep
from datetime import datetime, timedelta
import smtplib
import os
from tqdm import tqdm
from dotenv import load_dotenv

ADDRESS = 'https://row2.vfsglobal.com/PolandBelarus-Appointment/Account/RegisteredLogin?q=shSA0YnE4pLF9Xzwon/x/ASnHZRMROGDyz5YljrTPrmD7weWKDzHm/9+x4kyou3TsMOg99oc+0bfYTDhNi8VXO2A4zs7wBkyB6b15tURU2eT0aS3CJYjFGR6LRWzfcsZ5BzitruEIjN+SeHc17EKqO0YlhR3T0Pc1cO5uD69/WY='
pyautogui.FAILSAFE = True

class Find_visa:

    NOT_WORK = 1
    AUTORIZATION = 2
    SELECT_FIND_VISA = 3
    FIND_VISA = 4
    ENTER_ADDRESS = 5
    THERE_ARE_PLACES = 6
    STOP = 7

    LOG = 'my.log'

    def __init__(self, name_file, address):
        self.name_file = name_file
        self.status = None
        self.address = address

    @staticmethod
    def wait_element(element, time_wait):
        '''Ожидание появления на экране элемента element. Если за time_wait секунд не появился то возвращает None'''
        coords = None
        start = datetime.now()
        while not coords:
            coords = locateCenterOnScreen(element)
            if (datetime.now() - start) > timedelta(seconds=time_wait):
                break
        return coords

    def send_email(self):
        load_dotenv('config.env')
        EMAIL_FROM = os.getenv('EMAIL_FROM')
        PASSWORD_FROM = os.getenv('PASSWORD_FROM')
        EMAIL_TO = os.getenv('EMAIL_TO')
        if EMAIL_FROM and PASSWORD_FROM and EMAIL_TO:
            smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
            smtpObj.starttls()
            smtpObj.login(EMAIL_FROM, PASSWORD_FROM)
            smtpObj.sendmail(EMAIL_FROM, EMAIL_TO, 'Hooray! There are places for a visa!')
            smtpObj.quit()

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
        self.status = None

    def find_visa(self):

        run = True
        while run:
            for i in range(1,14):
                coords = self.wait_element('static/select_city_check.png', 300)
                if coords:
                    click(coords.x + 250, coords.y-7)  # выбор визового центра
                coords = self.wait_element('static/' + str(i) + '.png',300)
                if coords:
                    click(coords)  # нажимаем на визовый центр
                if self.wait_element('static/no_sits.png', 10) or self.wait_element('static/no_sits_eng.png', 5):
                    print(datetime.now(), 'Нет мест в центре ' + str(i), file=self.log)
                else:
                    print(datetime.now(), 'Пробую выбрать категорию визы', file=self.log)
                    coords = self.wait_element('static/select_record_category.png',5)
                    if coords:
                        click(coords.x, coords.y - 23)
                        moveTo(0,200)
                        if self.wait_element('static/select_record_category.png',10):
                            print(datetime.now(), 'Похоже сайт не работает.', file=self.log)
                            self.status = self.ENTER_ADDRESS
                        else:
                            self.status = self.THERE_ARE_PLACES
                        run = False
                        break
            if run:
                for i in tqdm(range(600)):
                    sleep(1)

    def check_status(self):
        if self.status == None:
            sleep(5)
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
        coords = self.wait_element('static/capcha.png', 10)
        if coords:
            click(coords)
        sleep(5)
        click(locateCenterOnScreen('static/next.png'))
        sleep(5)
        self.status = None

    def select_find_visa(self):
        coords = self.wait_element('static/schedule_appointment.png', 10)
        if coords:
            click(coords)
        else:
            coords = self.wait_element('static/schedule_appointment_rus.png', 10)
            if coords:
                click(coords)
            else:
                print(datetime.now(), 'Не нашёл пункт меню "Запись на подачу документов".', self.log)
        self.status = None

    def enter_address(self):
        click(472, 62, clicks=3)
        print(self.address, file=self.log)
        typewrite(r'https://row2.vfsglobal.com/PolandBelarus-Appointment/Account/RegisteredLogin?q=shSA0YnE4pLF9Xzwon/x/ASnHZRMROGDyz5YljrTPrmD7weWKDzHm/9+x4kyou3TsMOg99oc+0bfYTDhNi8VXO2A4zs7wBkyB6b15tURU2eT0aS3CJYjFGR6LRWzfcsZ5BzitruEIjN+SeHc17EKqO0YlhR3T0Pc1cO5uD69/WY=')
        sleep(3)
        press('enter')
        self.status = None

    def record_for_visa(self):
        click(locateCenterOnScreen('static/select_record_category.png'))
        sleep(1)
        pyautogui.screenshot('my_screenshot.png')
        self.status = None
        if input('>') == 'q':
            self.status = self.STOP

    def run(self):
        sleep(5)
        with open(self.LOG, 'a', encoding='utf-8') as self.log:
            run = True
            while run:
                self.check_status()
                if self.status == self.STOP:
                    break
                elif self.status == self.ENTER_ADDRESS:
                        print(datetime.now(), 'Ввод адреса сайта.', self.address, file=self.log)
                        self.enter_address()
                        print(datetime.now(), 'Адрес сайта введён.', file=self.log)
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
                elif self.status == self.THERE_ARE_PLACES:
                    print(datetime.now(), 'Есть свободные места. Начало записи на подачу документов.', file=self.log)
                    playsound.playsound('signal-gorna-na-obed.mp3')
                    self.send_email()
                    self.record_for_visa()


def split_image(image_name, num):
    image = Image.open(image_name)
    size_image = image.size
    step = int(size_image[1]/num)
    name = 1
    for i in range(0, size_image[1], step):
        image_new = image.crop((0,i,size_image[0],i+step))
        image_new.save('static/' + str(name) + '.png')
        name += 1

try:
    fv = Find_visa('Coordinates', ADDRESS)
    fv.run()
except Exception as e:
    playsound.playsound('signal-gorna-na-obed.mp3')
    print(e)

