import logging
logging.basicConfig()
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from datetime import *
import time
import pymysql
from bs4 import BeautifulSoup
import urllib.request
import json
import requests
import os #运行linux命令模块
import paramiko #登录模块
import re
import shelve
import sendNotify 
import  os
 

def Calfee(list):
    month=list[0]
    summaryBox=float(list[1])
    if int(month) in (1,2,3,4,11,12):
        if summaryBox<=201:
            print("冬季第一档：剩余",201-summaryBox)
            sum=summaryBox*0.5886
        elif 201<summaryBox<=401:
            print("冬季第二档：剩余",401-summaryBox)
            sum=201*0.5886+(summaryBox-201)*0.6388
        elif summaryBox>401:
            print("冬季第三档")
            sum=201*0.5886+((401-201)*0.6388)+((summaryBox-401)*0.8888)
    elif int(month) in (5,6,7,8,9,10):
        if summaryBox<=261:
            print("夏季第一档")
            sum=summaryBox*0.5886
        elif 261<summaryBox<=601:
            print("夏季第二档")
            sum=261*0.5886+(summaryBox-261)*0.6388
        elif summaryBox>601:
            print("夏季第三档")
            sum=261*0.5886+(601-261)*0.6388+(summaryBox-601)*0.8888
    else:
        print("没数据")
        sum=0
    return sum

access_id = os.environ['ID']
access_pw = os.environ['PW']

#1、模拟浏览器登录
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--window-size=1920,1080')

chrome_browser = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
chrome_browser.implicitly_wait(5)
chrome_browser.delete_all_cookies()
chrome_browser.get("https://95598.csg.cn/#/gd/login/login")
chrome_browser.find_element_by_xpath("//*[@id=\"app\"]/div/div/div/div[1]/div[3]/div/div/div/div[1]/div[1]/div[2]/span").click()
chrome_browser.find_element_by_class_name('input').send_keys(str(access_id))
time.sleep(1)
chrome_browser.find_element_by_css_selector("#app > div > div > div > div:nth-child(1) > div:nth-child(3) > div > div > div > div.loginContain > div.phoneInputA > div > div.inputContain.inputContainA > input").send_keys(str(access_pw))
time.sleep(1.3)
chrome_browser.find_element_by_class_name("ant-checkbox-input").click()
time.sleep(1)
chrome_browser.find_element_by_class_name("ant-btn.ant-btn-primary.ant-btn-block").click()
time.sleep(5)

chrome_browser.get("https://95598.csg.cn/#/gd/fee/feeService/calendar")
print("倒计时开始")
time.sleep(10)
db = shelve.open("cookies")   # 创建一个名为cookies的小型数据库
db["cookie"] = chrome_browser.get_cookies()   # 将获取到的数据写入cookie
summaryBoxlist=[] #存储每日电费
soup = BeautifulSoup(chrome_browser.page_source )
# 通过class获取有可能含有IP的元素列表
for tag in soup.find_all('div',class_="summaryBox"):
    # print(tag)
    s=tag.get_text().replace("\n","").replace(' ', '')
    print(s )
    summaryBoxlist.append(s)
    list_month_sum=re.findall(r"\d+\.?\d*",s)
    sum_total_fee=Calfee(list_month_sum)
    print(sum_total_fee,"元")
m_fullcalendar=soup.find_all ("tbody",class_="ant-fullcalendar-tbody")
for data in m_fullcalendar[0].find_all("div",class_="ant-fullcalendar-date"):

    # print(data.find("p",class_="duFont"))
    if data.find("p",class_="duFont") is not None:
        dufont=data.find("div",class_="ant-fullcalendar-value").get_text(),"号",data.find("p",class_="duFont").get_text()
        print( dufont )
        summaryBoxlist.append(dufont)

print(summaryBoxlist)
sendNotify.sendNotify().serverNotify("电费","总额："+str(sum_total_fee)+"元，"+str(summaryBoxlist))

 

