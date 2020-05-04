# -*- coding: utf-8 -*-
"""
Created on Sun Jan  6 01:42:53 2019

"""
from threading import Thread
import urllib.request as rqst
from urllib import parse
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import pickle
import json
from tqdm import tqdm_notebook as tqdm

def method_get_json(url,headers):
    req = rqst.Request(url=url,headers=headers)
    res = rqst.urlopen(req,timeout=100).read().decode('utf8')
    html = json.loads(res)
    return html

mainurl = 'http://a.vmall.com/uowap/index?method=internal.getTabDetail&serviceType=13&reqPageNum=1&uri=34789c86f4654624ba9e63cf1353c860&maxResults=25'

headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CLT-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.99 Mobile Safari/537.36',
    'Host': 'a.vmall.com',
    'Connection': 'Keep-Alive',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    }

#获得一级分类名称及对应url
mainhtml = method_get_json(mainurl,headers)
category1 = mainhtml['layoutData'][1]['dataList']
c1_list=[]
for c1 in category1:
    c1_detailId = c1['detailId']
    c1_name = c1['name']
    c1_url = 'http://a.vmall.com/uowap/index?method=internal.getTabDetail&serviceType=13&uri={}&maxResults=25&reqPageNum=1'.format(parse.quote(c1_detailId))
    c1_list.append({'c1_name':c1_name,'c1_detailId':c1_detailId,'c1_url':c1_url})
    
    
'''
#二级分类
url1_list = []
for i in range(1,len(c1_list)):
    url1_list.append('http://a.vmall.com/uowap/index?method=internal.getTabDetail&serviceType=13&uri={}&maxResults=25&reqPageNum=1'.format(parse.quote(c1_list[i]['c1_detailId'])))
c1_url=c1_list[1]['c1_url']
c2_overview_html=method_get_json(c1_url,headers)
c2_detail_url = 'http://a.vmall.com/uowap/index?method=internal.getTabDetail&serviceType=13&uri={}&maxResults=100000&reqPageNum=1'.format(parse.quote('app|C10374976__HiAd__null__second_cat_DOWNCOUNT_358__1__cdrInfo%3A20190131140701apsf4896096%5E%7BopType%7D%5E400010887%5EC10374976%5Esecond_cat_DOWNCOUNT_358%5E1%5E21ffed4c07be11e6bc3800163e0b0f53%5E17397%5Ee81f91784f393858208e227825da44a0eb7e04cfa1a46282fe16bebacdfd343b%5Ectr%5EU0NFOn5TUkM6%5E2019-01-31+14%3A07%3A01%5E5%5EP9_test%5E0.008425%5E0%5E6.0%5E6.0%5E4.99732%5E900086000032174902%5E20358%5E%5E%5E%5E8.0.1%5E1548914820917%5E0%5EZTA2M2NmZmFmNzk2NGExMzk0MDA3ZGI5MGUxYWNjOTQ%5E%5E%5E%5E0%5E%5E0%5E13.1301.10%5E%5ECN%5ECNY%5EANDROID%5E%5Esign%3A3e4215e8966df64b619ca81622a90cd2cb3d484707d4dc4f6f4be1fd81457a20%23isAdTag%3A0%23%3BlayoutId%3A806904__null'))
c2_detail_html = method_get_json(c2_detail_url,headers)
comment = 'http://a.vmall.com/uowap/index?method=internal.user.commenList3&serviceType=13&reqPageNum=79&maxResults=100&appid=C10374976'
comment_html = method_get_json(comment,headers)
'''

#获取二级分类及APP名称
class get_c2_and_appdetail(Thread):
    def __init__(self, c1_dict, headers, all_list):
        Thread.__init__(self)
        self._c1_dict = c1_dict
        self._header = headers
        self._all_list = all_list
        self.start()
        
    def run(self):
        c2_overview_html=method_get_json(self._c1_dict['c1_url'], self._header)
        for c2_detail in c2_overview_html['layoutData']:
            c2_detail_url = 'http://a.vmall.com/uowap/index?method=internal.getTabDetail&serviceType=13&uri={}&maxResults=100000&reqPageNum=1'.format(parse.quote(c2_detail['detailId']))
            c2_detail_html = method_get_json(c2_detail_url, self._header)
            c2_detail_list = c2_detail_html['layoutData'][0]['dataList']
            for c2_detail_dict in c2_detail_list:
                print(c2_detail_dict['name'])
                app_dict = {'c1':self._c1_dict['c1_name'],'c2':c2_detail_dict['tagName'],'appname':c2_detail_dict['name'],'package':c2_detail_dict['package']}           
                c2_detail_tag_url = 'http://a.vmall.com/uowap/index?method=internal.getTabDetail&serviceType=13&uri={}&maxResults=100000&reqPageNum=1'.format(parse.quote(c2_detail_dict['detailId']))
                c2_detail_tag_html = method_get_json(c2_detail_tag_url, self._header)
                for layout in c2_detail_tag_html['layoutData']:
                    if layout['layoutName']=='detaileditorrcommendcard':
                        app_dict['detaileditorrecommendcard']=layout['dataList'][0]['body']
                    if layout['layoutName']=='detailappintrocard':
                        app_dict['detailappintrocard']=layout['dataList'][0]['appIntro']
                    if layout['layoutName']=='detaillabelcard':
                        app_dict['detaillabelcard']= ','.join([l['tag'] for l in layout['dataList'][0]['tagList']])
                self._all_list.append(app_dict)

all_app_list, thread_pool = [], []
for i in range(1,len(c1_list)):
    app_spyder = get_c2_and_appdetail(c1_list[i], headers, all_app_list)
    thread_pool.append(app_spyder)

for each in thread_pool:
    each.join()
print('finished')

df = pd.DataFrame(all_app_list).drop_duplicates()

df.to_pickle('./huaweiapp_final_detail_3.pkl')
#df.to_csv(r'D:\glf_python\huaweiapp5.csv',index=False,encoding='gb18030')