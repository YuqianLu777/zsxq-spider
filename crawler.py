#Next Step, 先抓他个10页

from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
from datetime import datetime,timedelta
from peewee import *
from db_init import Topic, File
from db_restart import Topic_test, File_test

global json_buffer

def initiate():

    # -*- iniate settings -*-
#   CMD启动Chrome命令
#   "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=5555 --disable-popup-blocking --user-data-dir="C:\selenium\AutomationProfile"
#   前提是该文件夹已存在
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
            browser.switch_to.window(browser.window_handles[-1])
            browser.get(mypage_url)
            i = 0
            while i < 5:
                flag = html2json(browser.page_source)['succeeded']
                if flag == True:
#                    global json_buffer
#                    json_buffer = html2json(browser.page_source)
                    browser.close()
                    browser.switch_to.window(browser.window_handles[-1])
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
#    no_handles = len(browser.window_handles)
    browser.execute_script("window.open();")
    browser.switch_to.window(browser.window_handles[-1])
    browser.get(href)
    json = html2json(browser.page_source)
    i = 0
    while i < 5:
        time.sleep(1.5)
        flag = json['succeeded']
        if flag == True:
            browser.close()
            browser.switch_to.window(browser.window_handles[-1])
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

def fetch_content(browser, group_no, max_page, newest_time_str, oldest_time_str):
#end_time = 抓取的截止时间（包含该时点），start_time = 抓取的开始时间（包含该时点），max_page = 抓取的最大页数
#browser, group_no, start_time, no_page

    '''该方法return一个数组（状态，记录条数，最早时间，最晚时间）
    连接数据库

    for iterator < max_page:
        selenium打开新页面
        browser.get(get_url(end_time))
        
        确保正确打开页面
        if 此时end_time晚于start_time，则断开数据库连接 正常return
        get页面上的topics数量
        如果获取到的topics小于20，是否意味着已经到底？？？则获取完页面后断开数据库连接并return
        获取该页面上最新时间，if该时间早于start_time，遍历找到晚于等于start_time的最早topics，并更新页面上的topics数量
        
        循环处理范围内的topics:talk、Q%A、file_url
        case: talk & Q&A 查重并写入文本数据库
        case：file_url 查重并写入url数据库
        
        更新end_time
        selenium关闭页面

    正常return
    '''
    
    newest_time = datetime.strptime(newest_time_str, '%Y-%m-%d %H:%M:%S.%f')
    if newest_time_str != 'now':
        if oldest_time_str != 'oldest':
            oldest_time = datetime.strptime(oldest_time_str, '%Y-%m-%d %H:%M:%S.%f')
        else:
            oldest_time = datetime(1970, 1, 1)
        first_url = 'https://api.zsxq.com/v2/groups/' + str(group_no)+'/topics?scope=all&count=20&end_time=' + newest_time.strftime('%Y-%m-%dT%H%%3A%M%%3A%S.%f')[:-3]+'%2B0800'
    elif newest_time_str == 'now':
        if oldest_time_str != 'oldest':
            oldest_time = datetime.strptime(oldest_time_str, '%Y-%m-%d %H:%M:%S.%f')
        else:
            oldest_time = datetime(1970, 1, 1)
        first_url = 'https://api.zsxq.com/v2/groups/' + str(group_no)+'/topics?scope=all&count=20'
    
    db = SqliteDatabase('zsxq.db')
    #db = SqliteDatabase('test.db')
    db.connect()
    
    new_talk_list = []
    new_file_list = []
    last_time = datetime.now()
    next_url = first_url
    for ii in range(1,max_page+1):
   
        #打开新tab
        browser.execute_script("window.open();")
        browser.switch_to.window(browser.window_handles[-1])
        browser.get(next_url)
        
        #获取当前页面json，最多尝试5次，失败则返回异常
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
            with db.atomic():
                Topic_test.insert_many(new_talk_list).on_conflict(action='IGNORE').execute()
                File_test.insert_many(new_file_list).on_conflict(action='IGNORE').execute()
            db.close()
            #虽然报错但仍要把缓存写入db
            return False
    
        #获取一次刷新下的所有内容（file类型的不下载）
        #f = open("data.txt","w+",encoding="utf-8")
        #f.write(str(datetime.now())+'\n')
        for item in topics:
            content_type = item['type']
            create_time = datetime.strptime(item['create_time'], "%Y-%m-%dT%H:%M:%S.%f+0800")
            print(create_time)
            #f.write(create_time+'\n')
            if content_type == 'talk':
                text = ''
                images_url_list = ''
                if item['talk'].get('text'):
                    text = item['talk']['text'] + '\n'
                    #f.write(text+'\n')
                elif item['talk'].get('images'):
                    for each_image in item['talk']['images']:
                        images_url_list = images_url_list + each_image['large']['url'] + '\n'
                new_talk_list.append({ 
                            'topic_id': item['topic_id'],
                            'create_time': create_time,
                            'group_id': item['group']['group_id'],
                            'topic_content': text + images_url_list
                            })
                if item['talk'].get('files'):
                    for each_file in item['talk']['files']:
                        href = 'https://api.zsxq.com/v2/files/' + str(each_file['file_id']) + '/download_url'
                        #暂时不去get实际的下载连接
                        #download_url = get_download_url(browser, href) 
                        #f.write(each_file['name']+'\n')
                        #f.write(download_url+'\n')
                        new_file_list.append({
                            'file_id': each_file['file_id'],
                            'topic_id': item['topic_id'],
                            'file_name': each_file['name'],
                            #'file_content': download_url
                            'file_content': href
                            })
            elif content_type == 'q&a':
                text = item['question']['text']+'\n'+item['answer']['text']
                #f.write(text+'\n')
                new_talk_list.append({ 
                            'topic_id': item['topic_id'],
                            'create_time': create_time+'+0800',
                            'group_id': item['group']['group_id'],
                            'topic_content': text
                            })
            last_time = create_time
            #f.write('\n')
        #f.close()
        #关闭当前tab
        browser.close()
        browser.switch_to.window(browser.window_handles[-1])
        time.sleep(3)
        
        #计算新一页的url
        if len(new_talk_list)%20:
            break
        last_time = last_time + timedelta(microseconds = -1000)
        next_url = 'https://api.zsxq.com/v2/groups/' + str(group_no)+'/topics?scope=all&count=20&end_time=' + last_time.strftime('%Y-%m-%dT%H%%3A%M%%3A%S.%f')[:-3]+'%2B0800'
    
    #将内容写入数据库
    
    #以下为测试
    
    #Topic_test.truncate_table(restart_identity=True)
    #File_test.truncate_table(restart_identity=True)
    
    with db.atomic():
        Topic_test.insert_many(new_talk_list).on_conflict(action='REPLACE').execute()
        File_test.insert_many(new_file_list).on_conflict(action='IGNORE').execute()
    db.close()
    
    return True

if __name__ == "__main__":
    browser = initiate()
    time.sleep(3)
    fetch_content(browser, 51122528441224, 1, "2022-03-15 10:17:59.124", "oldest")
    print('读写完毕')
    time.sleep(999)
    print(link.status_code)
    print(link.content)
    dict_content = json.loads(link.content)
    print(dict_content)
    topics_list = dict_content['resp_data']['topics']
    print(topics)
