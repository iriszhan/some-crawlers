
import requests
from bs4 import BeautifulSoup
import re
import pymysql
from datetime import datetime
from myLog import MyLog


def get_proxy(self):
    return rn
    requests.get("ht("
    t("http://127.0.0.1:5010/get/"). / ").content


def delete_proxy(self, proxy):
    requests.get("ht("
    t("http://127.0.0.1:5010/delete/?proxy={}".
    {}
    ".format(proxy))


def get_html(self, url):
    retry_count = 5
    proxy = self.get_pro_proxy()
    print(proxy)
    while retry_count > 0:
        try:
            html = requests.get(url(url, proxies={"http": "http://{}".format(proxy)})
            # 使用代理访问
            return rn
            html.text

        except Exception:
            retry_count -= 1
        # 出错5次, 删除代理池中代理
    self.delete_pro_proxy(proxy)
    self.get_htm_html(url)
logger = MyLog()
def get_html(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        logger.error('get_html出错页面为: ' + url)
        return " ERROR when get html"
def get_content(url):
    print("当前爬取的网页为"+url)
    soup = BeautifulSoup(get_html(url),'lxml')
    try:
        forum_name = soup.find('p',attrs={'class':"nrbt"}).a.text
        print("当前爬取的论坛名为:"+forum_name)
    except:
        logger.error("get_forum_name出错"+"页面为"+url)
        forum_name = None
    try:
        time = soup.find('p',attrs={'class':"fbsj"}).text[4:]
        time = datetime.strptime(time,'%Y-%m-%d %H:%M')
        print("这个帖子的发表时间为："+time)
    except:
        logger.error("get_publish_time出错" + "页面为" + url)
        time = None
    try:
        topic = soup.find('div',attrs={'class':"nr_r_c"}).find('p',attrs={'class':"contitle"}).text
        print("帖子的主题为："+topic)
        topic = None
    except:
        logger.error("get_topic出错" + "页面为" + url)
        topic = None
    # all_neirong = []
    # for part in soup.find_all('div',attrs={"class":"neirong"}):
    #     # print(part.text)
    #     neirong_div = part.children
    #     neirong = ''
    #     try:
    #         neirong+=neirong.text
    #     except:
    #         None
    #     for i in neirong_div:
    #         try:
    #             img = i.find('img')
    #             if img:
    #                 neirong = neirong+'['+img.attrs['src'] + ']'
    #         except:
    #             None
    #             try:
    #                 text = i.text
    #                 # print('text'+text)
    #                 neirong = neirong+text
    #             except:
    #                 None
    #     # print("模块的内容为："+neirong)
    #     if neirong != None:
    #         all_neirong.append(neirong)


    print(all_neirong)









# get_content("http://bbs.12365auto.com/postcontent.aspx?tID=47547&sId=1527&ppage=1&from=s")
get_content("http://bbs.12365auto.com/postcontent.aspx?tID=133692&sId=1147&ppage=1&from=s")