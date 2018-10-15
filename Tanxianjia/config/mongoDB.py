# encoding=utf8
import pymongo
from bson.objectid import ObjectId

def search(collet,id):
    # 创建MongoDB的连接对象
    client = pymongo.MongoClient(host='jmongo-hb1-prod-mongo-usk7x69oif1.jmiss.jdcloud.com')
    # 指定数据库和用户名密码
    db = client.ins_survey
    db.authenticate('survey', 'survey')
    # 指定集合
    collection = db[collet]
    r = collection.find_one({'_id': id})
    return r

# s = search('gameLog','7c4ac49c-5890-4eed-bbaf-393105da8244')
# print s




