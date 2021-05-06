import requests
import json
import argparse
import os
import datetime
import time
import base64
from json_to_xlsx import QQ_Kuwo_csv_arry,NetEase_csv_arry
from tqdm import trange
from config import default,setting

def open_top_category(Category_path):
    """
    Category_path : the path of platform's category (.json) 
    """
    with open(Category_path,'r',encoding='utf-8') as f:
        data = json.load(f)
    return data

def get_url_info(setting,category):
    """
    input
        url : api
        headers : hearders
        category : the output of open_top_category()
    output
        dict
    """
    Dict = {}
    for ID in category:
        successful = True
        print("now:",ID,category[ID])
        req = requests.get(setting.url+str(ID),headers=setting.headers)
        while(successful):
            try:
                Dict[ID] = req.json()
                successful = False
            except:
                req = requests.get(setting.url+str(ID),headers=setting.headers)
    return Dict

def save_dict_to_json(Dict,Platform_name):
    """
    input
        Dict : the file we want to store
        Platform_name : the file which we save the json
    """
    if not os.path.isdir(Platform_name):
        os.mkdir(Platform_name)
    now_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    Platform_name = Platform_name+"/"+Platform_name+"_dict_"+str(now_time)+".json"
    with open(Platform_name,mode='w+',encoding='utf-8') as f:
        json.dump(Dict,f,ensure_ascii=False,sort_keys=False,indent=4)
    print(Platform_name+"is saved")
    return 

def get_song_lyric(platform,Dict):
    """
    get song lyric and put that in exist dict
    intput
        platform : QQ,Kugou,Kuwo,NetEase
        dict : the output of get_url_info()
    """
    if platform==setting.QQ:
        for index in Dict:
            for num in trange(len(Dict[index]['songlist']),ascii=True,desc="now ID:"+str(index)):
                song = Dict[index]['songlist'][num]
                platform.song_lyric_params['songid'] = song['data']['songid']
                platform.song_lyric_params['songmid'] = song['data']['songmid']
                req = requests.get(platform.song_lyric_url,headers=platform.headers,params=platform.song_lyric_params)
                try:
                    lyric = req.json()['lyric']
                    message_bytes = base64.b64decode(lyric)
                    message = message_bytes.decode()
                    song['data']['lyric'] = message
                except:
                    song['data']['lyric'] = 'None'
        return Dict

    elif platform==setting.NetEase:
        for index in Dict:
            for num in trange(len(Dict[index]['result']['tracks']),ascii=True,desc="now ID:"+str(index)):
                song = Dict[index]['result']['tracks'][num]
                ID = song['id']
                req = requests.post(platform.song_lyric_url+str(ID)+"&os=pc&lv=-1&tv=-1&kv=-1",headers=platform.headers)
                try:
                    lyric = req.json()['lrc']['lyric']
                    song['lyric'] = lyric
                except:
                    song['lyric'] = 'None'
                try:
                    klyric = req.json()['klyric']['lyric']
                    song['klyric'] = klyric
                except:
                    song['klyric'] = 'None'
        return Dict

    elif platform==setting.Kuwo:
        for index in Dict:
            for num in trange(len(Dict[index]['data']['musicList']),ascii=True,desc="now ID:"+str(index)):
                song = Dict[index]['data']['musicList'][num]
                ID = song['rid']
                GET=True
                while(GET):
                    try:
                        req = requests.get(platform.song_lyric_url+str(ID),headers=platform.headers,proxies=platform.proxies,timeout=3)
                        GET = False
                    except:
                        pass
                lyric = ""
                try:
                    for line in req.json()['data']['lrclist']:
                        lyric+= str(line['time'])+"_"+line['lineLyric']+"/"
                    song['lyric'] = lyric
                except:
                    song['lyric'] = "None"
        return Dict

    elif platform==setting.Kugou:
        for index in Dict:
            for num in trange(len(Dict[index]['data']['info']),ascii=True,desc="now ID:"+str(index)):
                song = Dict[index]['data']['info'][num]
                Hash = song['hash']
                album_id = song['album_id']
                params = {
                    'hash':Hash,
                    'album_id':album_id,
                    '_':1497972864535,
                    }
                req = requests.get(platform.song_lyric_url,headers=platform.headers,params=params)
                song_info = req.json()['data']
                Dict[index]['data']['info'][num]['sond_detail'] = song_info
        return Dict

def main():
    
    crawler_parser = argparse.ArgumentParser(description="Flags for crawler")
    crawler_parser.add_argument(
        "--action", default=default.action, required=False, help="Crawler action climb what we want"
    )
    crawler_parser.add_argument(
        "--xlsx", default=default.xlsx, required=False, help="Output xlsx option,now just support QQ and NetEase"
    )
    args = crawler_parser.parse_args()

    bool_QQ = False
    bool_Kugou = False
    bool_Kuwo = False
    bool_NetEase = False

    if args.action =="all":
        bool_QQ = True
        bool_Kugou = True
        bool_NetEase = True

    elif args.action =="QQ":
        bool_QQ = True

    elif args.action =="Kugou":
        bool_Kugou = True

    elif args.action =="Kuwo":
        bool_Kuwo = True
    
    elif args.action =="NetEase":
        bool_NetEase = True

    if bool_QQ:
        QQ_category = open_top_category(setting.QQ.category_file_name )
        QQ_dict = get_url_info(setting.QQ,QQ_category)
        QQ_dict = get_song_lyric(setting.QQ,QQ_dict)
        save_dict_to_json(QQ_dict,"QQ")
        if args.xlsx:
            QQ_Kuwo_csv_arry().save_to_xlsx(QQ_dict,0)

    if bool_Kugou:
        Kugou_category = open_top_category(setting.Kugou.category_file_name)
        Kugou_dict = get_url_info(setting.Kugou,Kugou_category)
        Kugou_dict = get_song_lyric(setting.Kugou,Kugou_dict)
        save_dict_to_json(Kugou_dict,"Kugou")

    if bool_NetEase:
        NetEase_category = open_top_category(setting.NetEase.category_file_name)
        NetEase_dict = get_url_info(setting.NetEase,NetEase_category)
        NetEase_dict = get_song_lyric(setting.NetEase,NetEase_dict)
        save_dict_to_json(NetEase_dict,"NetEase")
        if args.xlsx:
            NetEase_csv_arry().save_to_xlsx(NetEase_dict)

if __name__ == "__main__":
    main()