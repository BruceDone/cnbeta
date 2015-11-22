__author__ = 'Bruce'
import time
import datetime
import json
import requests
import re
import random
from multiprocessing.dummy import Pool as ThreadPool

today_str = '2015-11-22 11:08:09'
url = 'http://www.cnbeta.com/topics/more?jsoncallback=jQuery180025747765181586146_1448074680464&page=1&id=%s&csrf_token=66726edea59f7cb303d0197407e9dde39d8b7903&_=1448074691275'
filter_today = lambda x: datetime.datetime.strptime(x['inputtime'],
                                                    "%Y-%m-%d %H:%M:%S").date().__str__() == datetime.datetime.strptime(
    today_str, '%Y-%m-%d %H:%M:%S').date().__str__()
rand_sleep = [1, 2, 3, 4, 5]


def load_config():
    objs = json.load(open('info.json', 'r'))
    return objs


def print_muti_query(objs):
    list_obj = []
    pool = ThreadPool(10)
    results = pool.map(__call_ajax_by_id, objs)
    pool.close()
    pool.join()


def print_single_query(objs):
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
                    #print '--title---:', t['title'], '---time is---:', t['inputtime']
                    list_obj.append(t)
                except:
                    continue
    return list_obj


def __call_ajax_by_id(obj):
    time.sleep(random.choice(rand_sleep))
    format_url = url % obj['uid']
    r = requests.get(format_url)
    info = r.text
    info = re.sub('jQuery.*?[(]', '', info)
    info = info.rstrip(')')
    s = json.loads(info)['result']['list']
    if s:
        for t in s:
            try:
                print '--title---:', t['title'], '---time is---:', t['inputtime']
            except:
                continue


if __name__ == '__main__':
    objs = load_config()
    # print_muti_query(objs)
    list_obj = print_single_query(objs)
    print list_obj
    res = sorted(list_obj, key=lambda student: student['inputtime'])
    for x in res:
        print x['inputtime'],x['title']
