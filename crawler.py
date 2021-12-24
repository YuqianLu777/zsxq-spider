import requests

url = 'https://api.zsxq.com/v2/groups/15281118415522/topics?scope=all&count=20'
cookies = {"Cookie":'zsxq_access_token=A5B570DE-AFCD-71DA-6D3D-11B0E79664A6_07FED59ED2AA2EEA'}
headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/96.0.4664.110 Safari/537.36', }

responese = requests.get(url, cookies=cookies, headers = headers).content

print(requests.get(url, cookies=cookies, headers = headers).status_code)