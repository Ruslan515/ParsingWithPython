import xlwt
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re
from time import sleep
import csv

class Bot:
    def __init__(self):
        self.navigate();

    def get_html(self, url):
        r = requests.get(url)
        return r.text

    #вычисляем количество страниц на вкладке OPEN
    def totalPages(self, html):
        soup = BeautifulSoup(html, 'lxml')
        name_buttons = re.compile(r'\w+:\w+:\w+Last_\d+$')
        pages = soup.find('div', class_='formRepeatPagination2_NAVIGATION-BUTTONS-DIV').find('input', {'name': name_buttons}) # находим кнопку которая соо-ет условиям
        numStr = re.findall(r'\d+$', pages.attrs['id'])
        total_pages = int(numStr[0])
        print(total_pages)
        return total_pages

    def go_to_tab(self, numTab):

        # name_buttons = re.compile('//input[@name="\w*:\w*:\w*\d_\d"]$')
        numberTab = str(numTab)
        print('numberTab:', numberTab)
        name_buttons = 'contentForm:j_idt766:j_idt817_Next_' + numberTab
        print('name_buttons:', name_buttons)
        try:
            # buttons = self.driver.find_element_by_xpath(name_buttons)
            #buttons = self.driver.find_element_by_id(name_buttons)
            buttons = self.driver.find_element_by_name(name_buttons)
            print('This buttons', buttons)
            buttons.click()
            sleep(15)
            nameScreen = 'GE' + numberTab + '.png'
            self.driver.save_screenshot(nameScreen)
        except:
            buttons = None
            nameScreen = 'GE' + numberTab + '.png'
            self.driver.save_screenshot(nameScreen)
            print('BAd buttons', buttons)

    def write_csv(self, data, status_tender):
        print('write_CSV!')
        file_name = 'GeBiz_' + status_tender + '.csv'
        with open(file_name, 'a', encoding='utf-8') as f:
            print('file open')
            writer = csv.writer(f)
            print('file write now DATA:', data)
            #'tender': tenders[i].text, 'name_tender': name_tenders[i].text, 'dateClosing': date_closing[i],
            #'agency': inf_tanders[i * 3].text, 'Published': inf_tanders[i * 3 + 1].text,
             #          'Category': inf_tanders[i * 3 + 2].text, 'status': status[i].text}
            writer.writerow((data['tender'],
                             data['name_tender'],
                             data['dateClosing'],
                             data['agency'],
                             data['Published'],
                             data['Category'],
                             data['status']))
            print('write end')

    # Собираем данные по текущей вкладке
    def parse_tab(self, status_tender):
        try:
            tenders = self.driver.find_elements_by_xpath('//div[@class="formSectionHeader6_TEXT"]')
            print('Tenders OK', tenders[0].text)
            print('Len tenders: ', tenders.__len__())
        except:
            tenders = 0
            print('Bad Tenders!!!')

        try:
            name_tenders = self.driver.find_elements_by_class_name('commandLink_TITLE-BLUE')
            print('Tenders Name OK',name_tenders[0].text)
        except:
            name_tenders = 0
            print('Bad Name Tenders!!!')

        try:
            inf_tenders = self.driver.find_elements_by_class_name('formOutputText_VALUE-DIV')
            # inf_tanders[0] == Agency, inf_tanders[1] == Published, inf_tanders[2] == Procurement Category и так далее
            print('inf_tenders OK',inf_tenders[0].text)
        except:
            inf_tenders = 0
            print('Bad inf_tenders!!!')

        try:
            date_closing = self.driver.find_elements_by_xpath('//div[@class="formOutputText_HIDDEN-LABEL outputText_DATE-GREEN"]')
            print('date_closing OK',date_closing[0].text)
        except:
            date_closing = 0
            print('Bad date_closing!!!')

        try:
            status = self.driver.find_elements_by_xpath('//div[@class="label_MAIN label_WHITE-ON-GRAY"]')
            print('status OK',status[0].text)
        except:
            status = 0
            print('Bad status!!!')

        data = {}
        for i in range(0, len(tenders)):
            data[i] = {'tender': tenders[i].text, 'name_tender': name_tenders[i].text, 'dateClosing': date_closing[i].text,
                       'agency': inf_tenders[i * 3].text, 'Published': inf_tenders[i * 3 + 1].text,
                       'Category': inf_tenders[i * 3 + 2].text, 'status': status[i].text}


        print('DATA:', data)
        for i in range(0, len(data)):
            self.write_csv(data[i], status_tender)


    def parse_open(self):

        url = 'https://www.gebiz.gov.sg/ptn/opportunity/BOListing.xhtml?origin=menu'
        r = self.get_html(url)
        total_pages = self.totalPages(r)

        self.driver = webdriver.Chrome()
        self.driver.get('https://www.gebiz.gov.sg/ptn/opportunity/BOListing.xhtml?origin=menu')

        for i in range(2, total_pages + 1):
            print('i: ', i - 1)
            self.parse_tab('open')  # собираем данные с данной вкладки
            self.go_to_tab(i)  # переходим к следующей вкладке
            sleep(5)


    def parse_close(self):
        self.parse_tab('close')

    def navigate(self):


        self.parse_open()


        #self.parse_close()



def main():
    b = Bot()


if __name__ == '__main__':
    main()