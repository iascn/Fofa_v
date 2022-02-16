import requests
import re
import base64
import time
import sys

'''
@author : xxx 3.1
更改before 日期
更改cookie
python3 Fofa.py fofa语句
e.g. ：python3 Fofa.py 'app="Apache_OFBiz"'
'''




headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"}
url = "https://fofa.info/result?qbase64="
#1. 需要更改时间
after = "2020-01-01"
before = "2022-01-13"
#search = '"ValidateLogin" && title=="后台登录"'
search = sys.argv[1]
#2. 需要更改cookie
cookies = {""}


#return - str_data
def dchge_l(data,offnum):
    data = time.strptime(data,'%Y-%m-%d')
    data = time.mktime(data)
    data = int(data) - int(86400*offnum)
    data = float(data)
    data = time.localtime(data)
    data = time.strftime("%Y-%m-%d",data)
    return(data)

#return + str_data
def dchge_a(data,offnum):
    data = time.strptime(data,'%Y-%m-%d')
    data = time.mktime(data)
    data = int(data) + int(86400*offnum)
    data = float(data)
    data = time.localtime(data)
    data = time.strftime("%Y-%m-%d",data)
    return(data)

def timc(data):
    data = time.strptime(data,'%Y-%m-%d')
    data = time.mktime(data)
    return(int(data))


def crl(url,search,after,before):
    stxt = search+' && after="{0}" && before="{1}"'.format(after,before)
    url = url + str(base64.b64encode(stxt.encode('utf-8')))[2:-1]
    return url

f = open('url.txt','w')

def num(url):
    a = requests.get(url,cookies=cookies,timeout=10)
    n1 = re.findall('<li class="number">(\d)</li>',a.text)
    print('all page '+str(int(n1[-1])-1))
    for i in n1:
        i = str(int(i)-1)
        stxt = url + '&page='+i+'&page_size=10'
        print('page '+i)
        a = requests.get(stxt,cookies=cookies,timeout=10)
        #c2 = re.findall('(http://.*?)"',a.text)
        #c1 = re.findall('>(https://.*?)<',a.text)
        c = re.findall('<span class="aSpan"><a href="(.*?)" target="_blank">',a.text)
        #c = c1 + c2
        if i == str(int(n1[-1])-1):
            time = re.findall('<span>(\d*?-\d*?-\d*?)</span>',a.text)
            print('                             stop in => '+time[-1])
        for k in c:
            f.write(k+'\n')
            print(k)
    return time[-1]

before = dchge_a(before,1)
while 1:
    tmp = before
    print(dchge_l(before,1)+' => => => '+after)
    lurl = crl(url,search,after,before)
    before = num(lurl)
    before = dchge_a(before,1)
    if before == tmp:
        before = dchge_l(before,1)
        print("Warning !!!!  lose lose lose more 50 a day !")
    after = dchge_l(after,50)

f.close()
