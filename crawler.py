import requests
import json
import time

def initiate():
    url = 'https://api.zsxq.com/v2/groups/15281118415522/topics?scope=all&count=20'
    url = 'https://api.zsxq.com/v2/settings'

    '''
    cookies = {'zsxq_access_token':'8A1D9016-3DD4-F8FA-486E-9F93CAA8D0D3_07FED59ED2AA2EEA',
    'abtest_env':'projuct', 
    'sajssdk_2015_cross_new_user':'1',
    'sensorsdata2015jssdkcross':'%7B%22distinct_id%22%3A%2217dfa6a41fdacb-04efc6b090f618c-4303066-1327104-17dfa6a41fe900%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.google.com.hk%2F%22%7D%2C%22%24device_id%22%3A%2217dfa6a41fdacb-04efc6b090f618c-4303066-1327104-17dfa6a41fe900%22%7D'}'''
    
    headers = {
    'cookie':'abtest_env=product; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217dfa6a41fdacb-04efc6b090f618c-4303066-1327104-17dfa6a41fe900%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.google.com.hk%2F%22%7D%2C%22%24device_id%22%3A%2217dfa6a41fdacb-04efc6b090f618c-4303066-1327104-17dfa6a41fe900%22%7D; zsxq_access_token=9ECF7077-848E-9609-B3E6-0FDED0AD3074_07FED59ED2AA2EEA',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }
    
    response = requests.get(url, headers = headers)
    print(response.status_code)
    print(response.text)
    time.sleep(10000)
##    try 
    return response.content

if __name__ == "__main__":
    link = initiate()
    print(link.status_code)
    print(link.content)
    dict_content = json.loads(link.content)
    print(dict_content)
    topics_list = dict_content['resp_data']['topics']
    print(topics)

'''爬虫通用框架
import requests
def  getHTMLText(url):
    try:
        r = requests.get(url,timeout = 30) #30秒超时异常
        r.raise_for_status()#如果r返回的状态不是200，则引发HTTPError异常
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "产生异常"

if __name__ == "__main__":
    url = "http://www.baidu.com"
    print(getHTMLText(url))'''