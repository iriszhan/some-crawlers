import requests
from bs4 import BeautifulSoup
import re

def get_html(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return " ERROR when get html"
def get_link(url):
    """

    :param main_url: 网站首页网址
    :param url:链接网址
    :return:完整的链接列表
    """
    all_link = []
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    url_list = []
    txt_tit = soup.find_all('div', {"class": "txt-tit"})
    for i in txt_tit:
        url_list.append(i.a.get("href"))
    # url_list_complete = []
    #  for i in url_list:
    #      url_new = main_url + i
    #      url_list_complete.append(url_new)
    all_link.extend(url_list)
    next_button = soup.find("a", attrs={'class': "next"})
    if next_button != None:
        page_num = next_button.previous_sibling.text
        p1 = r"[0-9]+"
        pattern1 = re.compile(p1)  # 我们在编译这段正则表达式
        matcher1 = re.findall(pattern1, page_num)[0]
        page_num = int(matcher1)# 页面总数
        cut_url = url[:-5]
        for i in range(2 - 1):
            nextpage_url = cut_url + '-' + str(i + 2) + '.html'
            html = get_html(nextpage_url)
            soup = BeautifulSoup(html, 'lxml')
            url_list = []
            txt_tit = soup.find_all('div', {"class": "txt-tit"})
            for i in txt_tit:
                url_list.append(i.a.get("href"))
            all_link.extend(url_list)


    print(all_link)
    print(page_num)


# myurl = "https://bbs.pcauto.com.cn/wenda-16488.html"
# get_link(myurl)
results_tbl1 = []
def get_main_content(firstpageurl):
    """
    抓取每个帖子下的主问题(topic)，以及楼主名(owner)，发表时间(time)和问题详情(details)。
    :param firstpageurl:包含主问题贴的网址（也就是每个贴的首页）
    :return:{topic: '', owner: '', time: '', details: ''}
    """
    result = {}
    firstpage = get_html(firstpageurl)
    soup = BeautifulSoup(firstpage, 'lxml')
    result['topic'] = soup.find('i', attrs={"id": "subjectTitle"}).text
    result['owner'] = soup.find('li',{'class':"ofw"}).a.text
    result['time'] = soup.find('div', {'class':"post_time"}).text.strip()
    p1 = r"[0-9]{4}-[0-9]{2}-[0-9]{2}\s[0-9]{2}:[0-9]{2}"
    pattern1 = re.compile(p1)  # 我们在编译这段正则表达式
    matcher1 = re.findall(pattern1, result['time'])[0]
    result['time'] = matcher1
    result['details'] = soup.find('div',{'class':"post_msg replyBody"}).text.strip()
    results_tbl1.append(result)

def get_reply(url):
    """
    爬取回复楼主贴的在url里的所有回复的回复者(name)，回复时间(time)和回答内容(content)。
    :param url:
    :return:[{name:'', time:'', content:''}]
    """
    one_que_result = []
    page = get_html(url)
    soup = BeautifulSoup(page, 'lxml')
    content = soup.find_all('div', attrs={"class": "post_msg replyBody"})
    content_new = []#存放url所在界面的全部评论
    for tag in content:
        content_new.append(tag.text.strip())

    print(content_new)
    name = soup.find_all('li',{'class':"ofw"})
    name_new = []
    for  tag in name:
        name_new.append(tag.a.text)
    name_new = name_new[::2]
    print(name_new)
    time = soup.find_all('div', {'class':"post_time"})
    time_new = []
    for tag in time:
        new = tag.text.strip()
        p1 = r"[0-9]{4}-[0-9]{2}-[0-9]{2}\s[0-9]{2}:[0-9]{2}"
        pattern1 = re.compile(p1)  # 我们在编译这段正则表达式
        new = re.findall(pattern1, new)[0]
        time_new.append(new)
    print(time_new)
    zipped = zip(time_new, name_new, content_new)
    result = [dict(time=time, name=name, content=content) for time, name, content in list(zipped)]
    one_que_result.extend(result)
    print(result)
    #判断有没有下一页，如果有下一页继续爬取到列表，没有就什么都不做。
    next_button = soup.find("div", attrs={'id': "pagerBottom", 'class':"pager"})
    if next_button != None:
        page_num = int(next_button.find("a").text)#页面总数
        cut_url = url[:-5]
        for i in range(page_num-1):
            nextpage_url = cut_url+'-'+str(i+2)+'.html'
            page = get_html(nextpage_url)
            soup = BeautifulSoup(page, 'lxml')
            content = soup.find_all('div', attrs={"class": "post_msg replyBody"})
            content_new = []  # 存放url所在界面的全部评论
            for tag in content:
                content_new.append(tag.text.strip())

            print(content_new)
            name = soup.find_all('li', {'class': "ofw"})
            name_new = []
            for tag in name:
                name_new.append(tag.a.text)
            name_new = name_new[::2]
            print(name_new)
            time = soup.find_all('div', {'class': "post_time"})
            time_new = []
            for tag in time:
                new = tag.text.strip()
                p1 = r"[0-9]{4}-[0-9]{2}-[0-9]{2}\s[0-9]{2}:[0-9]{2}"
                pattern1 = re.compile(p1)  # 我们在编译这段正则表达式
                new = re.findall(pattern1, new)[0]
                time_new.append(new)
            print(time_new)
            zipped = zip(time_new, name_new, content_new)
            result = [dict(time=time, name=name, content=content) for time, name, content in list(zipped)]
            one_que_result.extend(result)
            print(result)
    print(one_que_result)#包含所有回复的列表，第一个元素为楼主的提问帖，其他为别人的回复。




    # get_main_content("https://bbs.pcauto.com.cn/topic-15005723.html")
    # print(results_tbl1)

# get_reply("https://bbs.pcauto.com.cn/topic-10202941.html")
get_link("https://bbs.pcauto.com.cn/wenda-16488.html")