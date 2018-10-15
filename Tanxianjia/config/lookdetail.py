# encoding=utf8
import re

def getSome(id,text):
    pattern = re.compile('id="'+id+'">(.*?)</label>', re.S)
    content = pattern.findall(text)
    res = content[0]
    return res

