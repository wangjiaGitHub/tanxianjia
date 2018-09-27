#!/usr/bin/env python
# encoding: utf-8

import unittest
import requests
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from config import conf
from config import getPerGameLog
from config import mongoDB


class TanxianjiaTest(unittest.TestCase):

    # 登录保ME后台
    @classmethod
    def setUpClass(cls):
        cls.url = conf.dengluUrl
        cls.r = requests.post(cls.url,data=conf.data)
        cls.needCookie = cls.r.cookies.get_dict()

    @classmethod
    def tearDownClass(cls):
        print u'测试结束'

    def test_Search(self):
        #输入查询条件的url
        self.url2 = conf.chaxunUrl(pn1=2,ps1=20)
        self.r = requests.get(self.url2,cookies=self.needCookie)
        # print self.r.text
        parttern = re.compile(r'</thead>.*?<tr>(.*?)</tr>.*?</table>', re.S)
        content = parttern.findall(self.r.text)

        for i in content:
            # 获取每一行的记录
            lst = getPerGameLog.findLog(i)
            gameID = lst[0]
            gameName = lst[2]
            gameVersion = lst[3]
            openID = lst[4]
            lastOpenID = lst[5]  #数据库字段可为空
            beginTime = lst[6]
            endTime = lst[7]
            track = lst[8]   #数据库字段可为空
            authorizeScope = lst[9]
            surveyTurn = lst[10]
            gameChannel = lst[11]

            if authorizeScope == u'手动授权':
                authorizeScope = 'snsapi_userinfo'
            if surveyTurn == u'否':
                surveyTurn = 'NOT_SURVEY_TURN'
            # #连上数据库对比并且断言
            s = mongoDB.search(gameID)   # <type 'dict'>\
            # self.assertEqual(s['gameName'],'ttt',msg=u'名字错误')
            self.assertEqual(s['gameVersion'], gameVersion, msg=u'版本错误')
            self.assertEqual(s['openID'], openID, msg=u'openID错误')
            self.assertEqual(s['beginTime'], beginTime, msg=u'beginTime错误')
            self.assertEqual(s['endTime'], endTime, msg=u'endTime错误')
            self.assertEqual(s['authorizeScope'], authorizeScope, msg=u'authorizeScope错误')
            self.assertEqual(s['surveyTurn'], surveyTurn, msg=u'surveyTurn错误')
            self.assertEqual(s['gameChannel'], gameChannel, msg=u'gameChannel错误')
            if lastOpenID in s.keys():
                self.assertEqual(s['lastOpenID'], lastOpenID, msg=u'lastOpenID错误')
            if track in s.keys():
                self.assertEqual(s['track'], track, msg=u'track错误')













