from easydict import EasyDict as edict
import json
import os

default = edict()
default.action = "all"
default.xlsx = False
default.file_path = "C:/Users/Nealson/Desktop/IR/final_porject/" #the file path where save the crawler file like QQ,Kugou,NetEase
default.setting_path = "config/setting.json"

db_settings = edict()
db_settings.host = "localhost"
db_settings.port = 3306
db_settings.user = "nelson"
db_settings.password = str(os.environ['MYSQL_PASSWD'])
db_settings.database = 'Song_info'
db_settings.charset = "utf8"

with open(default.setting_path,'r',encoding='utf-8') as f:
    setting = json.load(f)
setting = edict(setting)
