import requests
import re
import base64
import time
import sys

'''
@author : xxx 4.1
更改before 日期
更改cookie !!!!
python3 Fofa.py fofa语句
e.g. ：python3 Fofa.py 'app="Apache_OFBiz"'
'''




headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"}
url = "https://fofa.info/result?qbase64="
#1. 需要更改时间
after = "2021-01-01"
before = "2022-03-04"
#search = '"ValidateLogin" && title=="后台登录"'
search = sys.argv[1]
#2. 需要更改cookie
cookies = {""}


'''
参考下面这个....

cookies = {"Hm_lvt_b5514a35664fd4ac6a893a1e56956c97":"xxx","Hm_lpvt_b5514a35664fd4ac6a893a1e56956c97":"xx","isUpgrade":"","refresh_token":"xxx","befor_router":"","fofa_token":"xxx","user":"xxx"}
'''


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
    print(url)
    return(url)

f = open('url.txt','w')

def num(url):
    for i in range(1,4):
        i = str(i)
        last = 20
        if i == "3":
            last = 10
        stxt = url + '&page='+i+'&page_size='+str(last)
        print('page '+i)
        a = requests.get(stxt,cookies=cookies,timeout=10)
        #c2 = re.findall('(http://.*?)"',a.text)
        #c1 = re.findall('>(https://.*?)<',a.text)
        c = re.findall('<span class="aSpan"><a href="(.*?)" target="_blank">',a.text)
        #c = c1 + c2
        if (i == "3"):
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
