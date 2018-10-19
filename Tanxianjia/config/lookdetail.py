# encoding=utf8
import re
from collections import OrderedDict

def getSome(id,text):
    pattern = re.compile('id="'+id+'">(.*?)</label>', re.S)
    content = pattern.findall(text)
    res = content[0]
    return res

def getMore(id,text):
    pattern = re.compile('id="' + id + '">(.*?)</label>', re.S)
    content = pattern.findall(text)
    return len(content)

def getName(p,text):
    pattern = re.compile(p, re.S)
    content = pattern.findall(text)
    return len(content)

#没有风险卡片
def getNoCard(text):
    pattern = re.compile(r'<label class="col-sm-2 control-label">场景ID：</label>(.*?)<label class="col-sm-12 control-label">收集的卡片：</label>',re.S)
    content = pattern.findall(text)
    lst1 = []
    for i in content:
        p = re.compile(r'<label class="col-sm.*?control-label".*?>(.*?)</label>', re.S)
        c = p.findall(i)
        lst2 = []
        for i in range(len(c)):
            if i%2 == 0:
                lst2.append(c[i])
        lst1.append(lst2)
    return lst1

#获取风险卡片信息
def getCard(text):
    d = OrderedDict()
    l = []
    #先获取SceneID,放在一个tuple
    pattern = re.compile(r' <label class="col-sm-2 control-label" id="sceneID">(.*?)</label>',re.S)
    content = pattern.findall(text)
    sce = tuple(content)

    #获取风险卡片，存为list
    pattern = re.compile(r'<label class="col-sm-12 control-label">收集的卡片：</label>(.*?)<div id="menuContent" class="menuContent" style="display:none; position: absolute;">', re.S)
    content = pattern.findall(text)
    s = ''.join(content).replace(' ','').replace('\n','').split('收集的卡片：')
    for y in s:
        # 处理每一个场景的风险卡片
        pattern = re.compile(r'<labelclass="col-sm-3control-label">(.*?)</label>', re.S)
        content = pattern.findall(y)
        l.append(content)
    for x in range(len(sce)):
        k = sce[x]
        d[k] = l[x]
    return d













