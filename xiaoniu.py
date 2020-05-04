import requests
import time 
import logging
from tqdm import tqdm 
import os
import sys 

logger = logging.Logger(__name__)

session = requests.Session()
session.headers['User-Agent'] = 'Mozilla/5.0 '
session.proxies={}

session.verify=False
requests.urllib3.disable_warnings(requests.urllib3.exceptions.InsecureRequestWarning)

translate_file=None 
translate_before_file=None 
total=0
last_i=0
def retry(fail_sleep_time,callback):
    def decorator(func):
        def wrapper(*args,**kwargs):
            sleep_time=kwargs.pop('sleep_time',0)
            while True:
                try:
                    result=func(*args,**kwargs)
                    time.sleep(sleep_time)
                    return result 
                except Exception as e:
                    print(e)
                    with open('error.log','a') as f:
                        f.write(time.asctime())
                        f.write(' ')
                        f.write(str(e))
                        f.write('\n')
                    callback()
                    time.sleep(fail_sleep_time)
        return wrapper
    return decorator 

def on_error():
    global last_i
    _last_i=0
    if not os.path.exists(translate_file):
        last_i=_last_i
        return
    with open(translate_file,encoding='utf-8') as fin:
        for _ in fin:
            _last_i+=1
    last_i=_last_i
    return

def _total():
    global total 
    _total=0
    if not os.path.exists(translate_before_file):
        raise ValueError("Output directory [{}] isn't exists.".format(translate_before_file))
    with open(translate_before_file,encoding='utf-8') as fin:
        for _ in fin:
            _total+=1
    total=_total

@retry(30,on_error)
def trans(text,src='en',tgt='yue'):
    res=session.get(
        'https://test.niutrans.vip/NiuTransServer/testtrans',
        params={
            'from':src,
            'to':tgt,
            'src_text':text,
        },
    )
    assert res.status_code==200,res.text 
    return res.json()['tgt_text']

def translate(_translate_file,_translate_before_file,src='en',tgt='yue',sleep_time=5):
    global translate_file
    global translate_before_file
    translate_file=_translate_file
    translate_before_file=_translate_before_file
    _total()
    success_index=[]#记录成功的行号，也用于后续拼接
    with open(translate_before_file,encoding='utf-8') as fin:
        with open(translate_file,'a',encoding='utf-8') as fout:
            for i,text in enumerate(tqdm(fin,total=total,desc='翻译进度',ascii=True)):
                if (i%2) ==0:
                    if i<last_i:
                        continue 
                    fout.write(text.rstrip()+'\t'+trans(text.rstrip(),src=src,tgt=tgt,sleep_time=sleep_time))
                    success_index.append(i)
                    fout.write('\n')
                    fout.flush()
                else:
                    continue
    return success_index

if __name__ == '__main__':
    my_success_index=translate('translate.txt','translate_before.txt')
    with open('index.txt','a',encoding='utf-8') as f:
        for i in my_success_index:
            f.write(str(i)+'\n')