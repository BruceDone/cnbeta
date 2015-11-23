__author__ = 'Bruce'
import time
import datetime
import json
import requests
import re
import random
from multiprocessing.dummy import Pool as ThreadPool

list_obj = []
today_str = '2015-11-23 11:08:09'
url = 'http://www.cnbeta.com/topics/more?jsoncallback=jQuery180025747765181586146_1448074680464&page=1&id=%s&csrf_token=66726edea59f7cb303d0197407e9dde39d8b7903&_=1448074691275'
filter_today = lambda x: datetime.datetime.strptime(x['inputtime'],
                                                    "%Y-%m-%d %H:%M:%S").date().__str__() == datetime.datetime.strptime(
    today_str, '%Y-%m-%d %H:%M:%S').date().__str__()
rand_sleep = [1, 2, 3, 4, 5]


def load_config():
    objs = json.load(open('info.json', 'r'))
    return objs


def do_muti_query(objs):
    pool = ThreadPool(15)
    results = pool.map(__call_ajax_by_id, objs)
    pool.close()
    pool.join()


def do_single_query(objs):
    time.sleep(random.choice(rand_sleep))
    list_obj = []
    for p in objs:
        format_url = url % p['uid']
        r = requests.get(format_url)
        info = r.text
        info = re.sub('jQuery.*?[(]', '', info)
        info = info.rstrip(')')
        s = json.loads(info)['result']['list']
        s = filter(filter_today, s)
        if s:
            for t in s:
                try:
                    list_obj.append(t)
                except:
                    continue


def __call_ajax_by_id(obj):
    time.sleep(random.choice(rand_sleep))
    format_url = url % obj['uid']
    r = requests.get(format_url)
    info = r.text
    info = re.sub('jQuery.*?[(]', '', info)
    info = info.rstrip(')')
    s = json.loads(info)['result']['list']
    s = filter(filter_today, s)
    if s and len(s) > 0:
        for t in s:
            try:
                list_obj.append(t)
            except:
                continue


if __name__ == '__main__':
    objs = load_config()[1:10]
    # print_muti_query(objs)
    #list_obj = do_single_query(objs)
    print 'now do the muti query'
    do_muti_query(objs)
    if not list_obj:
        print 'empty list objs'
    else:
        res = sorted(list_obj, key=lambda artic: artic['inputtime'],reverse=True)
        for i in res:
            print '***************************'
            for k,v in i.items():
                print k,v
