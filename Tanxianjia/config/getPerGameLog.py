# encoding: utf-8

import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# s是list类型
def findLog(s):
    str1 = ','.join(s)
    dd = str1.replace(' ', '').replace('\n', '')
    pattern = re.compile(r'<th>(.*?)</th>', re.S)
    res = pattern.findall(dd)
    l = len(res)
    lst = []
    lst.append(s[0])
    for i in range(l):
        if res[i] == '':
            lst.append('None')
        else:
            lst.append(str(res[i]).strip())
    return lst






