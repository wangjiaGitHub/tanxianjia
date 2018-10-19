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
    u'''探险英雄后端管理'''
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
        u'''查阅页面展示内容与数据库对比'''
        global content
        # 输入查询条件的url
        self.url2 = conf.chaxunUrl(pn1=1, ps1=10)
        self.r = requests.get(self.url2, cookies=self.needCookie)
        # print self.r.text
        pattern = re.compile(r'<th><input name="print" type="checkbox" value="(.*?)"></th>(.*?)</td>.*?</tr>', re.S)
        content = pattern.findall(self.r.text)
        time.sleep(3)

        for i in content:
            # 获取每一行的记录
            i = list(i)
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

            beginTime = list(beginTime)
            beginTime.insert(10,' ')
            beginTime = ''.join(beginTime)
            endTime = list(endTime)
            endTime.insert(10, ' ')
            endTime = ''.join(endTime)
            if authorizeScope == u'手动授权':
                authorizeScope = 'snsapi_userinfo'
            if surveyTurn == u'否':
                surveyTurn = 'NOT_SURVEY_TURN'

            #连上数据库对比并且断言
            s = mongoDB.search('gameLog',gameID)   # <type 'dict'>
            self.assertEqual(s['gameName'],gameName,msg=u'名字错误')
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
        time.sleep(3)

    # #查看详情中的游戏过程
    # def test_case2(self):
    #     u'''查看详情中的游戏过程'''
    #     for i in content:
    #         # 获取每一行的记录
    #         i = list(i)
    #         lst = getPerGameLog.findLog(i)
    #         gameID = lst[0]
    #         self.lookdetailurl = 'http://10.207.248.22:30063/crazy/finder/game/log?gameLogID='+gameID
    #         self.r = requests.get(self.lookdetailurl,cookies=self.needCookie)
    #
    #         #获取轨迹 时间戳，并断言
    #         track = lookdetail.getSome('track',self.r.text)
    #         trackTimestamp = lookdetail.getSome('trackTimestamp',self.r.text)
    #         s = mongoDB.search('gameLog', gameID)  # <type 'dict'>
    #         if track != '':
    #             self.assertEqual(s['track'],track,msg=u'轨迹错误')
    #         if trackTimestamp != '':
    #             self.assertEqual(s['trackTimestamp'],trackTimestamp,msg=u'轨迹时间戳错误')
    #
    #         # 获取游戏分享次数，风险卡片分享次数，风险卡片箱点击次数，上一场景点击次数，下一场景点击次数
    #         gameShareTimes = int(lookdetail.getSome('gameShareTimes',self.r.text).encode('utf-8')) #<type 'unicode'>
    #         cardShareTimes = int(lookdetail.getSome('cardShareTimes',self.r.text).encode('utf-8'))
    #         cardBoxClickTimes = int(lookdetail.getSome('cardBoxClickTimes',self.r.text).encode('utf-8'))
    #         rSceneClickTimes = int(lookdetail.getSome('rSceneClickTimes',self.r.text).encode('utf-8'))
    #         nSceneClickTimes = int(lookdetail.getSome('nSceneClickTimes',self.r.text).encode('utf-8'))
    #         s2 = mongoDB.search('gameStatistics', gameID)  # <type 'dict'>
    #         self.assertEqual(s2['gameShareTimes'],gameShareTimes,msg=u'游戏分享次数错误')  #<type 'int'>
    #         self.assertEqual(s2['cardShareTimes'],cardShareTimes,msg=u'风险卡片分享错误')
    #         self.assertEqual(s2['cardBoxClickTimes'], cardBoxClickTimes, msg=u'宝盒点击次数错误')
    #         self.assertEqual(s2['rSceneClickTimes'], rSceneClickTimes, msg=u'上一场景点击次数错误')
    #         self.assertEqual(s2['nSceneClickTimes'], nSceneClickTimes, msg=u'下一场景点击次数错误')
    #     time.sleep(3)
    #
    # # 查看详情中的场景记录（除却风险卡片）
    # def test_case3(self):
    #     u'''查看详情中的场景记录（除却风险卡片）'''
    #     for i in content:
    #         # 获取每一行的记录
    #         i = list(i)
    #         lst = getPerGameLog.findLog(i)
    #         gameID = lst[0]
    #         self.lookdetailurl = 'http://10.207.248.22:30063/crazy/finder/game/log?gameLogID=' + gameID
    #         self.r = requests.get(self.lookdetailurl, cookies=self.needCookie)
    #         s = mongoDB.search('gameLog', gameID)  # <type 'dict'>
    #         s2 = mongoDB.search('gameStatistics', gameID)  # <type 'dict'>
    #
    #         #场景记录中  场景id，场景名称，获得星星数，游戏轨迹,进入次数，分享次数，提示次数
    #         le = lookdetail.getMore('sceneID', self.r.text)#看sceneID的个数
    #         if le == 0:
    #             continue
    #         else:
    #             #没有风险卡片
    #             lst = lookdetail.getNoCard(self.r.text.encode('utf-8'))
    #             le = len(lst)
    #             y = 0
    #             for i in lst:
    #                 sceneID =i[0]
    #                 sceneName = i[1]
    #                 starCount = int(i[2].encode('utf-8'))
    #                 gameRecord = i[3]
    #                 playTimes = int(i[4].encode('utf-8'))
    #                 shareTimes = i[5]
    #                 tipTimes = i[6]
    #                 #场景id，场景名称，获得星星数，游戏轨迹断言
    #                 self.assertEqual(s['sceneRecordListList'][y]['sceneID'], sceneID, msg=u'场景ID错误')
    #                 self.assertEqual(s['sceneRecordListList'][y]['sceneName'], sceneName, msg=u'场景名字错误')
    #                 self.assertEqual(s['sceneRecordListList'][y]['starCount'], starCount, msg=u'获得星星数错误')
    #                 if gameRecord != '':
    #                     self.assertEqual(s['sceneRecordListList'][y]['gameRecord'], gameRecord, msg=u'场景游戏轨迹错误')
    #                 #进入次数，分享次数和提示次数断言
    #                 self.assertEqual(s2['sceneStatisticsList'][y]['playTimes'], playTimes, msg=u'场景进入次数错误')
    #                 if shareTimes != '':
    #                     shareTimes = int(shareTimes.encode('utf-8'))
    #                     self.assertEqual(s2['sceneStatisticsList'][y]['shareTimes'], shareTimes, msg=u'场景分享次数错误')
    #                 if tipTimes != '':
    #                     tipTimes = int(tipTimes.encode('utf-8'))
    #                     self.assertEqual(s2['sceneStatisticsList'][y]['tipTimes'], tipTimes, msg=u'场景提示错误')
    #                 y = y+1


    # 查看详情中的场景记录（风险卡片）
    def test_case4(self):
        u'''查看详情中的场景记录（风险卡片）'''
        for i in content:
            # 获取每一行的记录
            i = list(i)
            lst = getPerGameLog.findLog(i)
            gameID = lst[0]
            print gameID
            self.lookdetailurl = 'http://10.207.248.22:30063/crazy/finder/game/log?gameLogID=' + gameID
            self.r = requests.get(self.lookdetailurl, cookies=self.needCookie)
            s = mongoDB.search('gameLog', gameID)  # <type 'dict'>
            s2 = mongoDB.search('gameStatistics', gameID)  # <type 'dict'>

            le = lookdetail.getMore('sceneID', self.r.text)#看sceneID的个数
            if le == 0:
                continue
            else:
                l = lookdetail.getName(r'<label class="col-sm-2 control-label center">名称：</label>', self.r.text.encode('utf-8'))
                if l != 0:
                    #有风险卡片
                    d = lookdetail.getCard(self.r.text.encode('utf-8'))
                    y = 0
                    for key in d.keys():
                        self.assertEqual(s['sceneRecordListList'][y]['sceneID'], key, msg=u'场景ID错误')
                        l = d[key]
                        print d[key]
                        print s['sceneRecordListList'][0]['collectedRisk'][0]
                        for x in range(len(l)):
                            #获取风险卡片名称
                            if x%3 == 0:
                                #数
                               self.assertEqual(s['sceneRecordListList'][y]['collectedRisk'][x/3]['name'], d[key][x], msg=u'风险卡片名字错误')
                            # 获取风险卡片code
                            elif x%3 == 1:
                                pass
                            # 获取风险卡片描述
                            else:
                                pass
                        y += 1






























