# -*- coding: UTF-8 -*-
import requests, re, time, random,os
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from lxml import etree
from bs4 import BeautifulSoup
from itertools import chain
#--------------------------------------
# 91 的临时站点，可以随时更换
#URL = "http://91porn.com/"
#URL = "http://91.91p17.space/"
#URL = "https://p06.rocks"
URL = "https://1012.91p51.live"
cookie = 'CLIPSHARE=bi7qqdgekgd3peik32kh9ltp13' #隔一段时间最好换一下cookie
#--------------------------------------
zone_1 = "top"
zone_2 = "hot"
zone_3 = "ori"
zone_4 = "long"
zone_5 = "longer"
zone_6 = "tf"
zone_7 = "mf"
zone_8 = "rf"
'''
category=top  #本月最热
category=hot  #当前最热
category=ori  #原创
category=long  #10min
category=longer  #20min
category=tf  #本月收藏
category=mf  #收藏最多
category=rf  #当前加精
'''
#----------------------------------------

def visit(url):
    retries = Retry(total=5,backoff_factor=10, status_forcelist=[500,502,503,504])
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Cache-Control':'max-age=0',
        'sec-fetch-dest': 'document',
        'Connection':'keep-alive',
        'Cookie':cookie,
        'Host':'1012.91p51.live',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=retries))
    html = s.get(url, headers=headers, stream=True)
    return html

def parseList(url):
    url_list = []
    list_new = []
    title_list = []
    m3u8_list = []
    selector = etree.HTML(visit(url).text)
    title = selector.xpath('//span[@class="video-title title-truncate m-t-5"]/text()')
    img_url = selector.xpath('//img[@class="img-responsive"]/@src')
    for t in title:
        title_data = t
        title_list.append(title_data)
    img_url_str = ','.join(img_url)
    m3u8url_str = re.findall(r"\b\d+\b", img_url_str)
    for i in m3u8url_str:
        m3u8_data = 'https://la.killcovid2021.com//m3u8/' + i + '/' + i + '.m3u8'
        m3u8_list.append(m3u8_data)
    list_new = list(chain.from_iterable(zip(title_list,m3u8_list)))
    n = 2
    for i in  range(0, len(list_new), n):
        lists_new = list_new[i:i + n]
        lists_str = '<>'.join(lists_new)
        url_list = lists_str.replace('[','').replace(']','').replace(' ','').replace(',','').replace('(','').replace(')','').replace('"','').replace('原创','')
        print(url_list)
        with open(os.getcwd()+"/url.txt","a",encoding='utf-8') as f:
            f.write(url_list + '\n')

def download_m3u8():
    path = r"url.txt"
    file = open(path,"r",encoding="utf-8",errors="ignore")
    while True:
        mystr = file.readline()#表示一次读取一行
        if not mystr:
            break
        str = mystr
        url = str.splitlines()
        title,urls = ''.join(url).split('<>',1)
        os.system(os.getcwd() + '/Settings/./ffmpeg -y -i ' + urls + ' -vcodec copy -acodec copy -absf aac_adtstoasc ' + os.getcwd() +'/Videos/' + title + '.mp4')
    os.system('rm -rf url.txt')#每次下载完以后删除url.txt
    os.system(os.getcwd() + 'bash upload.sh')#运行自动上传脚本

def enter(category):
    end = int(input("请输入想爬的页数:")) + 1
    for page in range(1, end):
        url = URL + '/v.php?category=' + category + '&viewtype=basic&page=' + str(page)
        print('正在爬取>>>>>>>>>>' + url + '<<<<<<<<<<正在爬取')
        time.sleep(random.randint(1, 3))
        parseList(url)
        print('爬取完毕>>>>>>>>>>' + url + '<<<<<<<<<<爬取完毕')
        

if __name__ == '__main__':
    print('==========')
    print('1、本月最热')
    print('2、当前最热')
    print('3、原    创')
    print('4、1 0 分钟')
    print('5、2 0 分钟')
    print('6、本月收藏')
    print('7、收藏最多')
    print('8、当前加精')
    print('==========')
    zone = input('请输入需要爬取的分区：')
    if int(zone) == 1:
        category = zone_1
        enter(category)
        download_m3u8()
    elif int(zone) == 2:
        category = zone_2
        enter(category)
        download_m3u8()
    elif int(zone) == 3:
        category = zone_3
        enter(category)
        download_m3u8()    
    elif int(zone) == 4:
        category = zone_4
        enter(category)
        download_m3u8()    
    elif int(zone) == 5:
        category = zone_5
        enter(category)
        download_m3u8()
    elif int(zone) == 6:
        category = zone_6
        enter(category)
        download_m3u8()
    elif int(zone) == 7:
        category = zone_7
        enter(category)
        download_m3u8()
    elif int(zone) == 8:
        category = zone_8
        enter(category)
        download_m3u8()



















