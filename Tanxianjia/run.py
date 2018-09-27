# encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import unittest
import time
from HTMLTestRunnerCN import HTMLTestRunner

if __name__ == '__main__':
    test_dir = './testCase'
    discover = unittest.defaultTestLoader.discover(test_dir,pattern='tanxianjiaCase.py')
    test_report = './report/'
    nowtime = time.strftime('%Y%m%d%H%M%S')
    test_report_file = u'探险英雄'+nowtime+'.html'
    file = test_report + test_report_file
    fp = open(file,'wb')
    runner = HTMLTestRunner(stream=fp,title=u'探险英雄后台自动化测试报告')
    runner.run(discover)
    fp.close()



