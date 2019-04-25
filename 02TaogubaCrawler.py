import requests
from bs4 import BeautifulSoup
import os
import threading
import random
import time
import datetime
import threadpool
import MySqlConnect


def getContent(count):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}
    url = 'https://www.taoguba.com.cn/Article/' + str(count) + '/1'
    # proxy_dict = [  # 免费代理ip  http://www.xiladaili.com/  #代理池
    #         # '60.255.186.169:8888', '42.176.36.251:43800', '120.198.61.126:38724', '39.105.171.101:3128',
    #         # '123.206.6.218:8888'
    #         '123.7.61.8:53281','106.12.7.54:8118','117.114.149.66:53281'
    #     ]
    f = open(".\\ip.txt")  # 返回一个文件对象
    proxy_dict = f.read().strip()
    proxy_dict = proxy_dict.split("\n")
    # print("proxy_dict:", proxy_dict)
    random_ip = random.choice(proxy_dict)
    proxy_dict = {'https:': random_ip}
    # print(random_ip)
    # requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
    s = requests.session()
    s.keep_alive = False  # 关闭多余连接
    f.close()

    try:
        res = s.get(url, headers=headers, proxies=proxy_dict)
        res = requests.get('https://www.taoguba.com.cn/Article/' + str(count) + '/1',
                           headers=headers)  # get方法中加入请求头
        soup = BeautifulSoup(res.text, 'html.parser')  # 对返回的结果进行解析
        # 提取文章内容
        tatime = soup.find_all('span', class_='p_tatime')  # 时间
        content = soup.find_all('div', class_='p_coten')  # 内容
        comment = soup.find_all('div', class_='pcnr_wz')  # 评论
        # print(len(comment),type(comment))
        allcomment = ''
        number = len(comment)  # 每个帖子的评论条数
        replyid = 1
        for i in range(number):  # postid发帖ID号  parentid发帖所属主题ID号
            allcomment += comment[i].text
            save2DB_comment(count, replyid, comment[i].text)
            replyid += 1
            # print(comment[i].text)
        # print(allcomment,type(allcomment))
        # print(str(count) + ':' + tatime[0].text + ":" + content[0].text + ":" + str(number) + ":" + allcomment)
        # save2DB_content(count, tatime[0].text, content[0].text, str(number), allcomment)  # 评论在一起
        save2DB_content(count, tatime[0].text, content[0].text, str(number))
    except Exception as e:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " - " + random_ip + " : " + url + "\n" + str(e))
    finally:
        return


# def save2DB_content(id, stringTime, content, number, comment):
#     sql = "INSERT INTO taoguba (\
#         id,\
#         stringTime,\
#         time,\
#         content,\
#         number,\
#         comment\
#         )\
#         VALUES(\"" + str(
#         id) + "\",\"" + stringTime + "\",\"" + stringTime + ":00\",\"" + content + "\",\"" + number + "\",\"" + comment.strip() + "\")"
#     # print(sql)
#     MySqlConnect.edit(sql)
def save2DB_content(id, stringTime, content, number):
    sql = "INSERT INTO taoguba (\
        id,\
        stringTime,\
        time,\
        content,\
        number\
        )\
        VALUES(\"" + str(
        id) + "\",\"" + stringTime + "\",\"" + stringTime + ":00\",\"" + content + "\",\"" + number + "\")"
    # print(sql)
    MySqlConnect.edit(sql)


def save2DB_comment(postid, replyid, comment):
    sql = "INSERT INTO comment (\
        postid, \
        replyid, \
        comment\
        )\
        VALUES(\"" + str(postid) + "\",\"" + str(replyid) + "\",\"" + comment + "\")"
    # print(sql)
    MySqlConnect.edit(sql)


if __name__ == "__main__":
    # 前两页测试
    begin = 79000
    end = 200000
    # 线程池：https://www.cnblogs.com/xiaozi/p/6182990.html
    pool = threadpool.ThreadPool(2)
    # for _count in range(begin,end):
    threadRequests = threadpool.makeRequests(getContent, range(begin, end))
    [pool.putRequest(req) for req in threadRequests]
    pool.wait()
