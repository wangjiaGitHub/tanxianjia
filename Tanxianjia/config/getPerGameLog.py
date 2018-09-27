# encoding: utf-8

import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def findLog(s):
    pattern = re.compile(r'<th>(.*?)</th>', re.S)
    res = pattern.findall(s)
    l = len(res)
    lst = []
    for i in range(l):
        if i == 0:
            s = str(res[i])[-38:-2]
            lst.append(s)
        elif res[i] == '':
            lst.append('None')
        else:
            lst.append(str(res[i]).strip())
    return lst






