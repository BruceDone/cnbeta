__author__ = 'Bruce'

import json
import os


def load_config():
    a = os.path.curdir
    objs = json.load(open('info.json', 'r'))
    return objs


PAGE_LIST = load_config()
