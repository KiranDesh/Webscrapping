# predefined packages
from selenium import webdriver
import datetime
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import Select
from unicodedata import normalize
import csv

try:
    BASE_URL = 'https://main.sci.gov.in/case-status'
    chrome_options = Options()
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    driver = webdriver.Chrome('/home/kiran/Downloads/chromedriver_linux64/chromedriver')

    column_names = []
    datafields = []
    for num in range(100):
    #     columns = []
    #     data = []
    #     column_names.append(columns)
    #     datafields.append(data)


        driver.get(BASE_URL) #getting the BASE_URL
        html = driver.page_source
        # parsing the html content
        html_content = bs(html,'lxml')
        
        # getting dropdown years
        years_dropdown = html_content.find('select',{"id":'CaseDiaryYear'})
        years = [op.get_text() for op in years_dropdown.find_all('option') if int(op.get_text())>=2001]
        driver.find_element_by_id('CaseDiaryNumber').send_keys(str(num+1))
        print('Diary number : ',str(num+1))
        
        # looping through 20 years
        for year in years:       
            columns = []
            data = []
            column_names.append(columns)
            datafields.append(data)
            columns.clear()
            data.clear()
            # accessing dropdown till 2000
            dropdown_element = Select(driver.find_element_by_id('CaseDiaryYear'))
            dropdown_element.select_by_value(year)
            print("        year :",year)
            
            # finding the captcha 
            html_loop = driver.page_source
            html_content_loop = bs(html_loop,'lxml')
            captcha = html_content_loop.find('p',{'id':'cap'}).get_text().strip()

            # filling the captcha
            driver.find_element_by_id('ansCaptcha').send_keys(captcha)
            # clicking on submit button
            driver.find_element_by_id('getCaseDiary').click()
            time.sleep(6)

            # loading page to the end
            actions = ActionChains(driver)
            for _ in range(8):
                actions.send_keys(Keys.ARROW_DOWN).perform()
                time.sleep(2)
            
            html_case = driver.page_source
            # parsing the html content
            html_content = bs(html_case,'lxml')
            case_content = html_content.find('div',{'class':'panel-body table-responsive'})
            try:
                tr_block = case_content.find_all('tr')
                td_block = [i.find_all('td') for i in tr_block]
                for td in td_block:
                    columns.append(td[0].get_text())
                    data.append(td[1].get_text())
            except Exception:
                pass
    driver.quit()
except:
    pass
for col,datas in zip(column_names,datafields):
    
    with open('/home/kiran/Desktop/result/final_csv.csv', 'a') as csvfile:  
        # creating a csv writer object  
        csvwriter = csv.writer(csvfile)  

        # writing the fields  
        csvwriter.writerow(col)  

        # writing the data rows  
        csvwriter.writerows([datas]) 
