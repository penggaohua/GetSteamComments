Tool_抓取steam评论_方案2.py

import requests
import io
import sys
import urllib.request
from bs4 import BeautifulSoup
'''


'''

appid = 1566690  #outpust
appid= 578080  #pubg

#入口
#https://steamcommunity.com/app/578080/reviews/?browsefilter=toprated&snr=15_100010
#https://steamcommunity.com/app/578080/reviews/?browsefilter=mostrecent&snr=15_100010&p=1
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码
headers = {    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'}
file = open('steamComments.txt', 'w+', encoding='utf-8')
for i in range(0,10):
    url = ('https://steamcommunity.com/app/1566690/homecontent/?userreviewsoffset=' +
           str(10 * (i - 1)) + '&p=' +
           str(i) + '&workshopitemspage=' +
           str(i) + '&readytouseitemspage=' +
           str(i) + '&mtxitemspage=' +
           str(i) + '&itemspage=' +
           str(i) + '&screenshotspage=' +
           str(i) + '&videospage=' +
           str(i) + '&artpage=' +
           str(i) + '&allguidepage=' +
           str(i) + '&webguidepage=' +
           str(i) + '&integratedguidepage=' +
           str(i) + '&discussionspage=' +
           str(i) + '&numperpage=10&browsefilter=mostrecent&appid=433850&appHubSubSection=10&l=schinese&filterLanguage=default&searchText=&forceanon=1')
    #browserfiler = {toprated }


    html = requests.get(url, headers=headers).text
    #print(type(html))
    soup = BeautifulSoup(html, 'html.parser')
    #名字

    # for business in soup.find_all('div', class_="persona_name"):
    #     for bb in business.find_all('a') :
    #         listName.append(bb.string)
    user_name = soup.find_all('div',{'class': 'persona_name'})
    post_date = soup.find_all('div',{'class': 'date_posted'})
    comments = soup.find_all('div', {'class': 'apphub_CardContentMain'})

    #print(len(post_date))
    for i in range(len(post_date)):
        pd  = post_date[i].text.replace('<div class="date_posted">',"").replace("</div>","")
        comment = comments[i].text.replace('\n',"").replace('\t',"").replace('\r',"")
        print(f'''{pd}\t{comment}''')

    # for comment in comments:
    #     print(comment.text.replace('\n','""'))
    #     file.write(comment.text.replace('\n','""'))

file.close
