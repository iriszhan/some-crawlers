import requests
import pymysql
from fake_useragent import UserAgent
from lxml import etree
import re
import json

db = pymysql.connect('127.0.0.1', 'root', 'root', 'zc')
ua = UserAgent()
def get_html(url):
    try:
        headers = {'User-Agent': ua.random}
        r = requests.get(url, headers = headers, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print(" ERROR when get html")

def test(item):
    if item==[]:
        return None
    else:
        return item

def get_content(detail_url):
    contents = []
    each_html = get_html(detail_url)
    detail_url_list=[]
    if each_html:
        content={}
        each_html=etree.HTML(each_html)
        # try:
        next_page_sign = each_html.xpath('//div[@class="pcauto_page"]/a[@class="next"]')

        if next_page_sign == []:
            last_page_num = 1
            detail_url_list.append(detail_url)
        else:
            last_page_num = int(each_html.xpath('//div[@class="pcauto_page"]/a[last()-1]/text()')[0])
            detail_url_list.append(detail_url)
            for j in range(last_page_num-1):
                nextpage_url = detail_url +'p'+ str(j + 2) + '.html'
                detail_url_list.append(nextpage_url)
        print(detail_url_list)
        for each_link in detail_url_list:

            each_detail_html = get_html(each_link)
            each_html=etree.HTML(each_detail_html)
            content_div_right=each_html.xpath('//div[@class="rightBm"]')
            div_num = len(content_div_right)
            content_div_left = each_html.xpath('//td[@class="leftTD"]')
            # print(content_div_left)
            # score=each_html.xpath('//td[@class="leftTD"]//i[@class="score"]/text()')
            for i in range(div_num):
                content['forum']=each_html.xpath('//div[@class="title"]/h1/text()')
                r=content_div_right[i]
                # ziduan=r.xpath('.//b/text()')#加.才能表示在当前节点之下寻找，否则表示在全文范围内寻找。
                # print(r.xpath('.//b/text()'))
                content['advantage']=r.xpath('.//b[contains(text(), "优点：")]/following-sibling::*/text()')
                content['disadvantage'] = r.xpath('.//b[contains(text(), "缺点：")]/following-sibling::*/text()')
                content['waiguan'] = r.xpath('.//b[contains(text(), "外观：")]/following-sibling::*/text()')
                content['neishi'] = r.xpath('.//b[contains(text(), "内饰：")]/following-sibling::*/text()')
                content['kongjian'] = r.xpath('.//b[contains(text(), "空间：")]/following-sibling::*/text()')
                content['peizhi']= r.xpath('.//b[contains(text(), "配置：")]/following-sibling::*/text()')
                content['dongli'] = r.xpath('.//b[contains(text(), "动力：")]/following-sibling::*/text()')
                content['yueye']=r.xpath('.//b[contains(text(), "越野：")]/following-sibling::*/text()')
                content['caokong'] = r.xpath('.//b[contains(text(), "操控：")]/following-sibling::*/text()')
                content['youhao'] = r.xpath('.//b[contains(text(), "油耗：")]/following-sibling::*/text()')
                content['shushi'] = r.xpath('.//b[contains(text(), "舒适：")]/following-sibling::*/text()')
                content['xuancheliyou']=r.xpath('.//b[contains(text(), "选车理由：")]/following-sibling::*/text()')
                l=content_div_left[i]
                c=l.xpath('.//script/text()')[0]
                score_str = str(c.encode('utf-8'))
                score_str = score_str[12:-3]
                score_dic = eval(score_str)
                content['score_zonghe']=float(score_dic["score"])
                content['score_waiguan']=int(l.xpath('.//ul//span[contains(text(), "外观")]/following-sibling::b/text()')[0])
                content['score_neishi'] = int(l.xpath('.//ul//span[contains(text(), "内饰")]/following-sibling::b/text()')[0])
                content['score_kongjian'] = int(l.xpath('.//ul//span[contains(text(), "空间")]/following-sibling::b/text()')[0])
                content['score_peizhi'] = int(l.xpath('.//ul//span[contains(text(), "配置")]/following-sibling::b/text()')[0])
                content['score_dongli'] = int(l.xpath('.//ul//span[contains(text(), "动力")]/following-sibling::b/text()')[0])
                content['score_caokong'] = int(l.xpath('.//ul//span[contains(text(), "操控")]/following-sibling::b/text()')[0])
                content['score_youhao'] = int(l.xpath('.//ul//span[contains(text(), "油耗")]/following-sibling::b/text()')[0])
                content['score_shushi'] = int(l.xpath('.//ul//span[contains(text(), "舒适")]/following-sibling::b/text()')[0])

                content['advantage']=test(content['advantage'])
                content['disadvantage']=test(content['disadvantage'])
                content['waiguan']=test(content['waiguan'])
                content['neishi']=test(content['neishi'])
                content['kongjian']=test(content['kongjian'])
                content['peizhi'] =test(content['peizhi'])
                content['dongli']=test(content['dongli'])
                content['yueye']=test(content['yueye'])
                content['caokong']=test(content['caokong'])
                content['youhao']=test(content['youhao'])
                content['shushi']=test(content['shushi'])
                content['xuancheliyou']=test(content['xuancheliyou'])
                content['score_zonghe']=test(content['score_zonghe'])
                content['score_waiguan']=test(content['score_waiguan'])
                content['score_neishi']=test(content['score_neishi'])
                content['score_kongjian']=test(content['score_kongjian'])
                content['score_peizhi']=test(content['score_peizhi'])
                content['score_dongli']=test(content['score_dongli'])
                content['score_caokong']=test(content['score_caokong'])
                content['score_youhao']=test(content['score_youhao'])
                content['score_shushi']=test(content['score_shushi'])
                content['forum']=test(content['forum'])
                print(content)
                cursor = db.cursor(pymysql.cursors.DictCursor)
                sql = 'INSERT INTO task_id18 (advantage,disadvantage,waiguan,neishi,kongjian,peizhi,dongli,yueye,caokong,youhao,shushi,xuancheliyou,score_zonghe,score_waiguan,score_neishi,score_kongjian,score_peizhi,score_dongli,score_caokong,score_youhao,score_shushi,forum_name) values(%s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s, %s,%s, %s, %s,%s)'
                cursor.execute(sql, (content['advantage'],content['disadvantage'],content['waiguan'],content['neishi'],content['kongjian'],content['peizhi'],
                                     content['dongli'],content['yueye'],content['caokong'],content['youhao'],content['shushi'],content['xuancheliyou'],
                                     content['score_zonghe'],content['score_waiguan'],content['score_neishi'],content['score_kongjian'],content['score_peizhi'],
                                     content['score_dongli'],content['score_caokong'],content['score_youhao'],content['score_shushi'],content['forum']))
                db.commit()
        # except:
        #     print("此网页没有取到"+detail_url)

get_content('https://price.pcauto.com.cn/comment/sg10740/')
