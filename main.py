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
    SCROLL_AUTORIZATION = 8

    LOG = 'my.log'

    def __init__(self, name_file, address):
        self.name_file = name_file
        self.status = None
        self.address = address

    @staticmethod
    def wait_element(element, time_wait, region=None):
        '''Ожидание появления на экране элемента element. Если за time_wait секунд не появился то возвращает None'''
        coords = None
        start = datetime.now()
        if isinstance(element, str):
            element = (element,)
        while (datetime.now() - start) < timedelta(seconds=time_wait):
            for i in element:
                coords = locateCenterOnScreen(i, region=region)
                if coords:
                    return coords
        return None

    @staticmethod
    def check_text(text, time_wait):
        start = datetime.now()
        while (datetime.now() - start) < timedelta(seconds=time_wait):
            click(50,200)
            hotkey('ctrl', 'a')
            hotkey('ctrl', 'c')
            s = pyperclip.paste()
            click(50, 200)
            if text in s:
                return True
        return False

    def logging(self, text):
        print(datetime.now(), text)
        print(datetime.now(), text, file=self.log)

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

    def find_visa(self, list_sity):
        run = True
        while run:
            for i in list_sity:
                self.wait_element('static/site_work.png', 120, region=(0, 0, 150, 150))
                coords = self.wait_element('static/select_city_check.png', 30, region=(350,450,200,200))
                if coords:
                    click(coords.x + 250, coords.y-7)  # выбор визового центра
                else:
                    self.status = None
                    run = False
                    break
                coords = self.wait_element('static/' + str(i) + '.png',300)
                if coords:
                    click(coords)  # нажимаем на визовый центр
                self.wait_element('static/site_work.png', 120, region=(0, 0, 150, 150))
                if self.check_text('Нет доступных мест', 10):
                    self.logging('Нет мест в центре ' + str(i))
                else:
                    self.logging('Пробую выбрать категорию визы')
                    coords = self.wait_element('static/category_record.png',5, region=(400, 420, 300,230))
                    if coords:
                        click(coords.x + 300, coords.y)
                        moveTo(0,200)
                    if self.wait_element('static/select_record_category.png',5, region=(420, 320, 730,330)):
                        self.logging('Похоже сайт не работает.')
                        self.status = self.ENTER_ADDRESS
                        run = False
                        break
                    coords = self.wait_element('static/karta_polaka_visa_D.png', 3, region=(600, 550, 350,210))
                    if coords:
                        click(coords)
                        self.logging('Выбираю визу D по карте поляка.')
                        click(locateCenterOnScreen('static/next.png'))
                        self.wait_element('static/site_work.png', 120, region=(0, 0, 150, 150))
                        if self.check_text('Нет доступных мест', 10):
                            self.logging('Нет мест в центре ' + str(i))
                        else:
                            self.status = self.THERE_ARE_PLACES
                            run = False
                            break
                    click(50,200)
                    coords = self.wait_element('static/category_record.png', 5, region=(400, 420, 300, 230))
                    if coords:
                        click(coords.x + 300, coords.y)
                        moveTo(0, 200)
                    coords = self.wait_element('static/nacional_visa_D.png', 3, region=(600, 550, 350,210))
                    if coords:
                        click(coords)
                        self.logging('Выбираю визу D национальную.')
                        self.wait_element('static/site_work.png', 120, region=(0, 0, 150, 150))
                        click(locateCenterOnScreen('static/next.png'))
                        self.wait_element('static/site_work.png', 120, region=(0, 0, 150, 150))
                        if self.check_text('Нет доступных мест', 10):
                            self.logging('Нет мест в центре ' + str(i))
                        else:
                            self.status = self.THERE_ARE_PLACES
                            run = False
                            break
                    click(50, 200)
                    coords = self.wait_element('static/category_record.png', 5, region=(400, 420, 300, 230))
                    if coords:
                        click(coords.x + 300, coords.y)
                        moveTo(0, 200)
                    coords = self.wait_element('static/courier_visa_D.png', 3, region=(600, 550, 350,210))
                    if coords:
                        click(coords)
                        self.logging('Выбираю курьера на визу D')
                        self.wait_element('static/site_work.png', 120, region=(0, 0, 150, 150))
                        click(locateCenterOnScreen('static/next.png'))
                        self.wait_element('static/site_work.png', 120, region=(0, 0, 150, 150))
                        if self.check_text('Нет доступных мест', 10):
                            self.logging('Нет мест в центре ' + str(i))
                        else:
                            if self.check_text('доступных мест нет', 10):
                                self.logging('Нет мест в центре ' + str(i))
                            else:
                                if self.check_text('Sorry, looks like you were going too fast.', 5):
                                    self.status = self.ENTER_ADDRESS
                                else:
                                    self.status = self.THERE_ARE_PLACES
                                run = False
                                break
                click(locateCenterOnScreen('static/next.png'))
                self.wait_element('static/site_work.png', 120, region=(0, 0, 150, 150))
            if run:
                for i in tqdm(range(400)):
                    sleep(1)

    def check_status(self):
        self.wait_element('static/site_work.png', 120, region=(0, 0, 150, 150))
        if self.status == None:
            start = datetime.now()
            while (datetime.now() - start) < timedelta(seconds=10):
                click(50,200)
                hotkey('ctrl', 'a')
                hotkey('ctrl', 'c')
                s = pyperclip.paste()
                if 'Выбрать город' in s:
                    self.logging('Выбран статус поиска визы.')
                    self.status = self.FIND_VISA
                    break
                elif 'Запись на подачу документов' in s:
                    self.logging('Выбираем "Запись на подачу документов."')
                    self.status = self.SELECT_FIND_VISA
                    break
                elif 'Назначить дату подачи документов' in s:
                    if 'Ваша учетная запись заблокирована' in s:
                        sleep(130)
                    self.logging('Нажимаем капчу')
                    self.status = self.AUTORIZATION
                    break
                elif 'You are now in line' in s:
                    self.status = self.NOT_WORK
                    break
                elif 'Инструкция' in s:
                    self.status = self.SCROLL_AUTORIZATION
            else:
                self.status = self.ENTER_ADDRESS
            click(50, 200)

    def autorization(self):
        self.wait_element('static/site_work.png', 120, region=(0, 0, 150, 150))
        coords = self.wait_element(('static/capcha.png', 'static/capcha2.png'), 10, region=(350, 450, 200, 200))
        if coords:
            click(coords)
        sleep(5)
        click(locateCenterOnScreen('static/next.png'))
        sleep(5)
        self.status = None
        self.wait_element('static/site_work.png', 120, region=(0, 0, 150, 150))

    def select_find_visa(self):
        self.wait_element('static/site_work.png', 120, region=(0, 0, 150, 150))
        coords = self.wait_element('static/schedule_appointment_rus.png', 10, region=(170, 240, 300, 160))
        if coords:
            click(coords)
        else:
            coords = self.wait_element('static/schedule_appointment.png', 10, region=(170, 240, 300, 160))
            if coords:
                click(coords)
            else:
                self.logging('Не нашёл пункт меню "Запись на подачу документов".')
        sleep(5)
        self.status = None

    def enter_address(self):
        pyautogui.hotkey('alt', 'd')
        pyperclip.copy(self.address)
        pyautogui.hotkey('ctrl', 'v')
        pyperclip.copy('')
        sleep(1)
        press('enter')
        self.status = None
        sleep(1)
        self.wait_element('static/site_work.png', 240, region=(0,0,150,150))

    def record_for_visa(self):
        sleep(1)
        pyautogui.screenshot(str(datetime.now()).split('.')[0].replace(':', '-') +'.png')
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
                        self.logging('Ввод адреса сайта.' + self.address)
                        self.enter_address()
                        self.logging('Адрес сайта введён.')
                elif self.status == self.NOT_WORK:
                        self.logging('Сайт ожидает очереди.')
                        self.wait_site_work()
                        self.logging('Очередь подошла.')
                elif self.status == self.AUTORIZATION:
                        self.logging('Авторизация.')
                        self.autorization()
                        self.logging('Конец авторизации.')
                elif self.status == self.FIND_VISA:
                        self.logging('Начало поиска визового центра со свободными местами.')
                        self.find_visa((3,4,5,6,7,8,9,10,11,12,13))
                        self.logging('Конец поиска визового центра со свободными местами.')
                elif self.status == self.SELECT_FIND_VISA:
                        self.logging('Выбор меню поиска визового центра.')
                        self.select_find_visa()
                        self.logging('Выбрано меню поиска визового центра.')
                elif self.status == self.THERE_ARE_PLACES:
                    self.logging('Есть свободные места. Начало записи на подачу документов.')
                    playsound.playsound('signal-gorna-na-obed.mp3')
                    # self.send_email()
                    self.record_for_visa()
                elif self.status == self.SCROLL_AUTORIZATION:
                    self.logging('Скроллинг вниз и авторизация.')
                    self.autorization()
                    self.logging('Конец авторизации.')


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
    print('Версия 0.02')
    fv.run()
except Exception as e:
    playsound.playsound('signal-gorna-na-obed.mp3')
    fv.logging(e)

