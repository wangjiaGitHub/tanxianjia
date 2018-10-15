# encoding: utf-8

dengluUrl = 'http://10.207.248.22:30063/doLogin'
data = {'username':'admin_baome_test','password':'admin123'}
def chaxunUrl(pn1=1,ps1=10,authorizeScope1='',openId1='',surveyTurn1='',beginDate1='',endDate1=''):
    chaxunUrl = 'http://10.207.248.22:30063/crazy/finder/game/logs?pn='+str(pn1)+ '&ps=' + str(ps1)+ '&authorizeScope=' + str(authorizeScope1)+ '&openId=' + str(openId1)+ '&surveyTurn=' + str(surveyTurn1)+ '&beginDate=' + str(beginDate1) + '&endDate=' + str(endDate1)

    return chaxunUrl
