from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests
import pandas as pd
import re
from lxml import etree

# 登录QQ空间
def get_shuoshuo(qq):
    chromedriver = r"D:\BaiduNetdiskDownload\chromedriver\chromedriver.exe"
    driver = webdriver.Chrome(chromedriver)
    # 使用get()方法打开待抓取的URL
    driver.get('http://user.qzone.qq.com/{}/311'.format(qq))
    time.sleep(2)
    # 等待5秒后，判断页面是否需要登录，通过查找页面是否有相应的DIV的id来判断
    try:
        driver.find_element_by_id('login_div')
        a = True
    except:
        a = False
    if a == True:
        # 如果页面存在登录的DIV，则模拟登录
        driver.switch_to.frame('login_frame')
        driver.find_element_by_id('switcher_plogin').click()
        driver.find_element_by_id('u').clear()  # 选择用户名框
        driver.find_element_by_id('u').send_keys('2757544027')
        driver.find_element_by_id('p').clear()
        driver.find_element_by_id('p').send_keys('wangdawei')
        driver.find_element_by_id('login_button').click()
        time.sleep(5)
    driver.implicitly_wait(3)

    # 判断好友空间是否设置了权限，通过判断是否存在元素ID：QM_OwnerInfo_Icon
    try:
        driver.find_element_by_id('QM_OwnerInfo_Icon')
        b = True
    except:
        b = False
    # 如果有权限能够访问到说说页面，那么定位元素和数据，并解析
    info = []
    if b == True:
        page = 1  # 第一页
        try:
            while page:
                ##下拉页面
                for j in range(1, 5):
                    driver.execute_script("window.scrollBy(0,5000)")
                    time.sleep(2)

                driver.switch_to.frame('app_canvas_frame')
                #print(driver.page_source)
                html=etree.HTML(driver.page_source)
                #评论人昵称
                nickname=html.xpath('//div[@class="comments_content"]/a[@class="nickname"]/text()')
                print(nickname)
                #评论人QQ
                qq=html.xpath('//div[@class="comments_content"]/a[@class="nickname"]/@href')
                print(qq)
                #评论时间
                con_time=html.xpath('//div[@class="comments_content"]/div[@class="comments_op"]/span[1]/text()')
                print(con_time)
                #评论内容
                comments=html.xpath('//div[@class="comments_content"]/span[@style="display: none;"]/following-sibling::span/text()')
                print(comments)
                #被回复人昵称
                to_name=html.xpath('//div[@class="box bgr3"]/div[@class="bd"][1]/a/text()')[0]
                print(to_name)
                #被回复人qq
                to_qq=html.xpath('//div[@class="box bgr3"]/div[@class="bd"][1]/a/@href')[0]
                to_qq_extract=to_qq.split('/')[-2]
                print(to_qq_extract)
                #变成字典列表
                qq_dict_list=[{'被回复人QQ':to_qq_extract,'被回复人昵称':to_name,'评论人昵称':each_nickname,'评论人QQ':each_qq,'评论时间':each_con_time,'评论内容':each_comments} for each_nickname,each_qq,each_con_time,each_comments in zip(nickname,qq,con_time,comments)]
                print(qq_dict_list)
                #整合到info里
                info.extend(qq_dict_list)
                print(info)

                #soup = BeautifulSoup(driver.page_source, "html.parser")
                # for con in soup.select('ol[id="msgList"] > li'):
                #     print('======')
                #     comments = con.select('li[class="comments_item bor3"]')
                #     for comment in comments:
                #         res = {}
                #         nickname = comment.select('.nickname')[0].getText()
                #         qq = comment.select('.nickname')[0]['href'].split('/')[3]
                #         con_time = comment.select('.comments_op span')[0].getText()
                #         content_list = comment.select('.comments_content span')
                #         if '回复' not in content_list[0].getText():
                #             content = content_list[0].getText()  # 'hello'+
                #         else:
                #             content = content_list[1].getText()
                #         to_qq = comment.select('.comments_content span a')  # [0]#['data-uin']
                #         res['评论人昵称'] = nickname
                #         res['评论人QQ'] = qq
                #         res['评论内容'] = content
                #         res['评论时间'] = con_time
                #         res['被回复人qq'] = to_qq
                #         info.append(res)
                #         print(info)
                page = page + 1
                try:
                    driver.find_element_by_link_text(u'下一页').click()  # 点击下一页
                    driver.switch_to.default_content()  # 跳出当前frame
                except Exception as e:
                    print('无下一页！')
                    break
                time.sleep(3)
            driver.quit()
        except Exception as e:
            # 我没有判断什么时候为最后一页，当爬取到最后一页，
            # 默认点击下一页，会出现异常，我直接在这认为它是爬到末尾了，还是有待优化
            driver.quit()
            driver.close()
    else:
        print("可能设置了权限！")
    print("爬取完成，爬到的最后页数为" + str(page - 1))
    return info

df = pd.DataFrame(get_shuoshuo('250284494'))