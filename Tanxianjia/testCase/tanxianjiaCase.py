#!/usr/bin/env python
# encoding: utf-8

import unittest
import time
import requests
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from config import conf
from config import getPerGameLog
from config import mongoDB
from config import lookdetail


class TanxianjiaTest(unittest.TestCase):
    content = []

    # 登录保ME后台
    @classmethod
    def setUpClass(cls):
        print u'测试开始'
        cls.url = conf.dengluUrl
        cls.r = requests.post(cls.url,data=conf.data)
        cls.needCookie = cls.r.cookies.get_dict()

    @classmethod
    def tearDownClass(cls):
        print u'测试结束'

    #测试每一行的内容跟数据库是否一致
    def test_case1(self):
        global content
        # 输入查询条件的url
        self.url2 = conf.chaxunUrl(pn1=1, ps1=10)
        self.r = requests.get(self.url2, cookies=self.needCookie)
        # print self.r.text
        pattern = re.compile(r'<th><input name="print" type="checkbox" value="(.*?)"></th>(.*?)</td>.*?</tr>', re.S)
        content = pattern.findall(self.r.text)
        time.sleep(3)

        # for i in content:
        #     # 获取每一行的记录
        #     i = list(i)
        #     lst = getPerGameLog.findLog(i)
        #     gameID = lst[0]
        #     gameName = lst[2]
        #     gameVersion = lst[3]
        #     openID = lst[4]
        #     lastOpenID = lst[5]  #数据库字段可为空
        #     beginTime = lst[6]
        #     endTime = lst[7]
        #     track = lst[8]   #数据库字段可为空
        #     authorizeScope = lst[9]
        #     surveyTurn = lst[10]
        #     gameChannel = lst[11]
        #
        #     beginTime = list(beginTime)
        #     beginTime.insert(10,' ')
        #     beginTime = ''.join(beginTime)
        #     endTime = list(endTime)
        #     endTime.insert(10, ' ')
        #     endTime = ''.join(endTime)
        #     if authorizeScope == u'手动授权':
        #         authorizeScope = 'snsapi_userinfo'
        #     if surveyTurn == u'否':
        #         surveyTurn = 'NOT_SURVEY_TURN'
        #
        #     # #连上数据库对比并且断言
        #     s = mongoDB.search('gameLog',gameID)   # <type 'dict'>
        #     self.assertEqual(s['gameName'],gameName,msg=u'名字错误')
        #     self.assertEqual(s['gameVersion'], gameVersion, msg=u'版本错误')
        #     self.assertEqual(s['openID'], openID, msg=u'openID错误')
        #     self.assertEqual(s['beginTime'], beginTime, msg=u'beginTime错误')
        #     self.assertEqual(s['endTime'], endTime, msg=u'endTime错误')
        #     self.assertEqual(s['authorizeScope'], authorizeScope, msg=u'authorizeScope错误')
        #     self.assertEqual(s['surveyTurn'], surveyTurn, msg=u'surveyTurn错误')
        #     self.assertEqual(s['gameChannel'], gameChannel, msg=u'gameChannel错误')
        #     if lastOpenID in s.keys():
        #         self.assertEqual(s['lastOpenID'], lastOpenID, msg=u'lastOpenID错误')
        #     if track in s.keys():
        #         self.assertEqual(s['track'], track, msg=u'track错误')


    def test_case2(self):
        for i in content:
            # 获取每一行的记录
            i = list(i)
            lst = getPerGameLog.findLog(i)
            gameID = lst[0]
            self.lookdetailurl = 'http://10.207.248.22:30063/crazy/finder/game/log?gameLogID='+gameID
            self.r = requests.get(self.lookdetailurl,cookies=self.needCookie)

            #获取轨迹 时间戳，并断言
            track = lookdetail.getSome('track',self.r.text)
            trackTimestamp = lookdetail.getSome('trackTimestamp',self.r.text)
            s = mongoDB.search('gameLog', gameID)  # <type 'dict'>
            if track != '':
                self.assertEqual(s['track'],track,msg=u'轨迹错误')
            if trackTimestamp != '':
                self.assertEqual(s['trackTimestamp'],trackTimestamp,msg=u'轨迹错误')

            break
        time.sleep(3)







