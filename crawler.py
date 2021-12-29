from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

global json_buffer

def initiate():

    # -*- iniate settings -*-
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('log-level=3')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation','enable-logging'])
    executable_path = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
    index_url = 'https://wx.zsxq.com/'
    mypage_url = 'https://api.zsxq.com/v2/groups/48844244242848/topics?scope=all&count=20'
    chrome_ser = Service(executable_path)
    browser = webdriver.Chrome(options = chrome_options, service = chrome_ser)

    browser.get(index_url)
    
    signal = ''
    counter = 0
    while counter < 5:
        signal = input("是否已经扫码登录完毕？ Y/N  ")
        if signal == 'Y' or 'y':
            browser.execute_script("window.open();")
            handles = browser.window_handles
            browser.switch_to.window(handles[1])
            browser.get(mypage_url)
            i = 0
            while i < 5:
                flag = html2json(browser.page_source)['succeeded']
                if flag == True:
#                    global json_buffer
#                    json_buffer = html2json(browser.page_source)
                    browser.close()
                    browser.switch_to.window(handles[0])
                    return browser
                else:
                    browser.refresh()
                    print('刷新页面')
                    i += 1
        else:
            counter += 1

    return EOF

def html2json(html:str):
    soup = BeautifulSoup(html, 'lxml')
    cc = soup.select('pre')[0]
    res = json.loads(cc.text)
    return res

def fetch_content(browser, group_no, no_page):
    group_url = 'https://api.zsxq.com/v2/groups/' + str(group_no)+'/topics?scope=all&count=20'
    browser.execute_script("window.open();")
    handles = browser.window_handles
    browser.switch_to.window(handles[1])
    browser.get(group_url)
    
    global json_buffer
    json_buffer = html2json(browser.page_source)
    topics = json_buffer['resp_data']['topics']
    print(topics)
    
    return True

if __name__ == "__main__":
    browser = initiate()
    fetch_content(browser, 48844244242848, 1)
    time.sleep(999)
    print(link.status_code)
    print(link.content)
    dict_content = json.loads(link.content)
    print(dict_content)
    topics_list = dict_content['resp_data']['topics']
    print(topics)
