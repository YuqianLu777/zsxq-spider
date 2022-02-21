#Next Step, 扩展fetch_content方法至多页，参数为browser, group_no, start_time, no_page

from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import datetime
from peewee import *
from db_init import Topic, File

global json_buffer

def initiate():

    # -*- iniate settings -*-
#   CMD启动Chrome命令 "c:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=5555 --user-data-dir="C:\selenium\AutomationProfile" 前提是该文件夹已存在 
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:5555")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('log-level=3')
#    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation','enable-logging'])
    executable_path = "C:\Program Files\Google\Chrome\Application\chromedriver.exe" #注意检查chrome driver版本#
    index_url = 'https://wx.zsxq.com/'
    mypage_url = 'https://api.zsxq.com/v2/groups/48844244242848/topics?scope=all&count=20' #用自己主页测试#
    chrome_ser = Service(executable_path)
    browser = webdriver.Chrome(service = chrome_ser, options=chrome_options)

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
                    print('Selenium启动成功')
                    return browser
                else:
                    browser.refresh()
                    browser.implicitly_wait(1.5)
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

def get_download_url(browser, href):
    no_handles = len(browser.window_handles)
    browser.execute_script("window.open();")
    browser.switch_to.window(browser.window_handles[no_handles])
    browser.get(href)
    json = html2json(browser.page_source)
    i = 0
    while i < 5:
        time.sleep(1.5)
        flag = json['succeeded']
        if flag == True:
            browser.close()
            browser.switch_to.window(browser.window_handles[no_handles-1])
            return json['resp_data']['download_url']
        else:
            browser.refresh()
            json = html2json(browser.page_source)
            time.sleep(1.5)
            print('刷新下载链接页面')
            i += 1
    if i==5: 
        print("取不到文件下载链接！")
        time.sleep(999)
#        browser.close()
#        browser.switch_to.window(browser.window_handles[no_handles-1])
        return False

def trans2datatime(input_time:str):
    date = input_time[0:10]
    time = input_time[11:23]
    return(date + ' ' + time)

def fetch_content(browser, group_no, no_page):
    group_url = 'https://api.zsxq.com/v2/groups/' + str(group_no)+'/topics?scope=all&count=20'
    db = SqliteDatabase('zsxq.db')
    db.connect()
    browser.execute_script("window.open();")
    handles = browser.window_handles
    browser.switch_to.window(handles[1])
    browser.get(group_url)
    
    global json_buffer
    json_buffer = html2json(browser.page_source)
    i = 0
    while i < 5:
        flag = html2json(browser.page_source)['succeeded']
        if flag == True:
            topics = json_buffer['resp_data']['topics']
            break
        else:
            browser.refresh()
            browser.implicitly_wait(1.5)
            json_buffer = html2json(browser.page_source)
            print('刷新页面')
            i += 1
    if i==5: 
        print("取不到页面内容！")
        print(html2json(browser.page_source))
        return False
    
    f = open("data.txt","w+",encoding="utf-8")
    f.write(str(datetime.datetime.now())+'\n')
    for item in topics:
        content_type = item['type']
        create_time = trans2datatime(item['create_time'])
        f.write(create_time+'\n')
        if content_type == 'talk':
            text = item['talk']['text']
            f.write(text+'\n')
            new_talk = Topic(topic_id = item['topic_id'], create_time = create_time, group_id = item['group']['group_id'], topic_content = text)
            new_talk.save()
            sleep(999)
            if item['talk'].get('files'):
                for each_file in item['talk']['files']:
                    href = 'https://api.zsxq.com/v2/files/' + str(each_file['file_id']) + '/download_url'
                    download_url = get_download_url(browser, href) 
                    f.write(each_file['name']+'\n')
                    f.write(download_url+'\n')
        elif content_type == 'q&a':
            text = item['question']['text']+'\n'+item['answer']['text']
            f.write(text+'\n')
        f.write('\n')
    f.close()
    
    browser.close()
    browser.switch_to.window(browser.window_handles[no_handles-1])
    return True

if __name__ == "__main__":
    browser = initiate()
    fetch_content(browser, 51122528441224, 1)
    time.sleep(999)
    print(link.status_code)
    print(link.content)
    dict_content = json.loads(link.content)
    print(dict_content)
    topics_list = dict_content['resp_data']['topics']
    print(topics)
