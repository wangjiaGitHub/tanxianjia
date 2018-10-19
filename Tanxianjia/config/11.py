# encoding=utf8
import conf
import re
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from collections import OrderedDict

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

url = conf.dengluUrl
r = requests.post(url,data=conf.data)
needCookie = r.cookies.get_dict()
lookdetailurl = 'http://10.207.248.22:30063/crazy/finder/game/log?gameLogID=297d7039-9748-4ae2-a4ea-fefc3f3a12e7'
r3 = requests.get(lookdetailurl, cookies=needCookie)
d = getCard(r3.text.encode('utf-8'))
for key in d.keys():
    print key


