# encoding=utf8
import pymongo
from bson.objectid import ObjectId

def search(collet,id):
    # 创建MongoDB的连接对象
    client = pymongo.MongoClient(host='116.196.95.152')
    # 指定数据库和用户名密码
    db = client.ins_survey
    db.authenticate('survey', 'survey')
    # 指定集合
    collection = db[collet]
    r = collection.find_one({'_id': id})
    return r

# s = search('gameLog','bd0dfc86-9775-4574-919f-f69d76a96eba')
# print s




