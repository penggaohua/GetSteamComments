import re
from datetime import datetime
#steam 评论，用户信息爬取
import requests
import time
import xlwt
import urllib

'''
需求：抓取 unpacking 所有评论
https://store.steampowered.com/app/1135690/Unpacking/
'''




#https://store.steampowered.com/appreviews/933110?cursor=*&language=schinese&day_range=365&review_type=all&purchase_type=all&filter=recent  //帝国时代3

from GetCommentInfo import  *
from bs4 import BeautifulSoup
appName = "Unpacking"
#appid = input("steam：请输入appid：")
#appid=1566690  #重装前哨
#appid= 933110  #d帝国时代3
#appid = 578080  #pubg
#appid = 433850
appid = 1135690  #unpacking
#appid = 2877720  #糟糕他们太爱我了怎么办  (测试用）
#appid= 2276420 #《绝命游歌》 测试用
maxDataSize = 10
#maxDataSize = input("请输入要请求数据的条数(10的倍数)：")

listAllContent = [] #所有的评论数据
nextCursor = "*" #索引下一页评论的cursor
reloadDataNum = 0 #重新拉取次数
reloadDataNumMax = 5 #重新拉取次数最大 = 5 ， 超过次数结束爬取。
lastedNum = 0
totalEndNum = 0
# PUBG 578080


def getGameName() :
#    resp = requests.get((f"https://store.steampowered.com/app/{appid}"),timeout=5).json()
     resp = requests.get((f"https://store.steampowered.com/app/578080/PUBG"),timeout=5)  #测试用
     print(resp.text)
#     print(resp)
#
#     soup= BeautifulSoup(resp.text,"html.parser")
#     # Note=open('xxx.txt',mode='w', encoding='utf-8')
#     # Note.write(soup.prettify())
#     for business in soup.find_all('span',{'itemprop': ['name']}):
#         print("获取游戏名字:")
#         appName = business.string
#         print(appName)
#         appName = appName.replace(":","-")
#         appName = appName.replace(":","-")
#         appName = appName.replace("/","-")
#         appName = appName.replace("|","-")
#         appName = appName.replace("?","-")
#         appName = appName.replace("？","-")
#         appName = appName.replace(">","-")
#         appName = appName.replace("<","-")
#         print(appName)
    #return   appName


def change_time(format,timestamp):
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime(format)

def getInitCursorValue_writeExcel(page_num) :
    #先打开一张表格
    print("开始存储!")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet("游戏数据", cell_overwrite_ok=True)
    #col = ["用户名","是否推荐",  "游戏时长(小时)", '发布于', "具体时间","评论"]
    col = ["用户名","是否推荐",  "评论"]
    for i in range(len(col)):
        sheet.write(0, i, col[i])  # 列名
    #需要一个pointer

    isEnd = False
    global reloadDataNum
    global nextCursor
    global lastedNum
    global totalEndNum
    headers = {
    'Content-Type': 'application/json'
    }

    line_count = 1
    for num  in range(page_num):
        try:
            print(f"开始第{num}页采集")
        # 昨天的328能用的
        #  resp = requests.get((f"https://store.steampowered.com/appreviews/{appid}?cursor={nextCursor}&language=schinese&day_range=365&review_type=all&purchase_type=all&filter=recent"),timeout=5).json()
           # resp_name = requests.get((f"https://store.steampowered.com/app/{appid}"), timeout=5).json()
            #all  所有语言  schinese  简体中文
           # url = f"https://store.steampowered.com/appreviews/{appid}?cursor={nextCursor}&language=all&day_range=365&review_type=all&purchase_type=all&filter=recent"
           # url = f"https://store.steampowered.com/appreviews/{appid}?cursor={nextCursor}&language=schinese&day_range=1200&review_type=schinese&purchase_type=all&filter=recent"
            url = f"https://store.steampowered.com/appreviews/{appid}?cursor={nextCursor}&language=english&day_range=1200&review_type=schinese&purchase_type=all&filter=recent"

               # https: // store.steampowered.com / appreviews / {appid}?cursor = {nextCursor} & language = schinese & day_range = 365 & review_type = all & purchase_type = all & filter = recent

            resp = requests.get((url),timeout=5).json()
            resp_timestamp= requests.get((url+"&json=1"),timeout=5).json()
        except Exception as e:
            print(f"request failed：请求评论失败，尝试重新拉取...{reloadDataNum}")
            resp = ""
            isEnd = True
            reloadDataNum = reloadDataNum + 1
            time.sleep(1)
        if isEnd :
            return isEnd
        reloadDataNum = 0 #reset

        cursor = resp["cursor"]
        cursor = cursor.replace("+","%2B")
        nextCursor = cursor
        html = resp["html"] #本页评论数据
        soup= BeautifulSoup(html,"html.parser")
        #print(soup)
        #解析 用户名
        listName = get_name_list(soup)
        listRecommend = get_recommend_list(soup)
     #   print(listRecommend)
        listPlayTime = get_playtime_list(soup)
        listPostDate= get_postDate_list(soup)
        listComment =  get_comment_list(soup)
        revews_list = resp_timestamp["reviews"]
        #    print(num,line_count)
        temp= line_count
        #写入表格
        #todo 用迭代器来做
        if not  listName:
            print("listName 为空")
            break;
        for line in range(temp, temp+len(listName)):
                timestamp  = revews_list[line%20-1]["timestamp_created"]
            #    print(listName)
                sheet.write(line, 0, listName[line%20-1])
                sheet.write(line, 1, listRecommend[line%20-1])
              #  sheet.write(line, 2, listPlayTime[line%20-1])
             #   sheet.write(line, 3, change_time("%m月%d日",timestamp))
             #   sheet.write(line, 4, change_time('%Y-%m-%d %H:%M:%S',timestamp))
              #  sheet.write(line, 5, listComment[line%20-1])
                sheet.write(line, 2, listComment[line%20-1])

                line_count+=1
                print(f"pointer->{line_count}")

    print(line_count)
    current_time = time.strftime('%Y%m%d_%H%M%S')
    #appName =  getGameName()
    tt = f"res\游戏[{appName}]抓取时间[{current_time}]评论数[{line_count-1}条]].xls"
    book.save(tt)
    return isEnd




if __name__ == '__main__':
    start = time.time()
    #getInitCursorValue_writeExcel(1210)
    getInitCursorValue_writeExcel(1105)

   # getGameName()

    print("耗费时间:",time.time()-start)
    time.sleep(1)
