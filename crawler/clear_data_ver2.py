"""clean data ver2"""
import os
import json
import difflib
from opencc import OpenCC
import re

def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False

def is_contains_japanese(strs):
    for _char in strs:
        if '\u0800' <= _char <= '\u4e00':
            return True
    return False

def is_contains_Korean(strs):
    for _char in strs:
        if '\uac00' <= _char <= '\ud7a3':
            return True
    return False


def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()

def clean_data_ver2():
    t2tw = OpenCC('t2tw') #繁體中文 -> 繁體中文 (台灣)
    s2t = OpenCC('s2t') #簡體中文 -> 繁體中文
    s2tw = OpenCC('s2tw') #簡體中文 -> 繁體中文 (台灣)
    t2s = OpenCC('t2s') #繁體中文 -> 簡體中文
    t2tw = OpenCC('t2tw') #繁體中文 -> 繁體中文 (台灣)
    tw2s = OpenCC('tw2s') #繁體中文 (台灣) -> 簡體中文

    song_dict = {}
    #auther_dict = {} not yet

    song_id = 1
    for i in os.listdir("clean_data/"):
        week_time = i.split('.')[0]
        with open("clean_data/"+str(week_time)+".json",mode='r',encoding='utf-8') as f:
            data = json.load(f)
        print("now week:%s" %week_time)
        for platform in data:
            print(platform)
            for toplist_id in data[platform]:
                print(toplist_id)
                for song in data[platform][toplist_id]:                
                    pre_songname = re.split('\(|\（|\)|）',song['songname'])
                    if not song_dict:
                        song['song_id'] = song_id
                        song_dict[tw2s.convert(pre_songname[0])] = song
                        song_id += 1      
                    else:
                        if is_contains_chinese(pre_songname[0]):  
                            pre_songname[0] = tw2s.convert(pre_songname[0])
                        repeat = False
                        
                        for name in list(song_dict):
                            score = string_similar(pre_songname[0],name)
                            if score >= 0.8:
                                repeat = True
                                break
                        if repeat:
                            song['song_id'] = song_dict[name]['song_id']
                        else:
                            song['song_id'] = song_id
                            song_dict[tw2s.convert(pre_songname[0])] = song
                            song_id += 1
        with open("clean_data/"+str(week_time)+"_ver2.json",mode='w+',encoding='utf-8') as f:
            json.dump(data,f,ensure_ascii=False,sort_keys=False,indent=4)
        
    with open("clean_data/song_table.json",mode="w+",encoding='utf-8') as f:
        json.dump(song_dict,f,ensure_ascii=False,sort_keys=False,indent=4)

def build_Intermediate_Table():
    platform_dict={
        'QQ':1,
        'Kugou':2,
        'kuwo':3,
        'NetEase':4
    }

    Intermediate_Table = []

    for i in os.listdir("clean_data/"):
        if len(i.split('_'))>=2:
            if i.split('_')[1]=='ver2.json':
                print("now file:",i)
                with open("clean_data/"+i,mode='r',encoding='utf-8') as f:
                    data = json.load(f)
                    for platform in data:
                        now_platform_id = platform_dict[platform]
                        for now_toplist_id in data[platform]:
                            for song in data[platform][now_toplist_id]:
                                now_song_id = song['song_id']
                                now_song_rank = song['rank']
                                now_song_week = song['week_date']
                                now_dict = {
                                    'Song_ID':now_song_id,
                                    'Toplist_ID':now_toplist_id,
                                    'Platform_ID':now_platform_id,
                                    'Rank':now_song_rank,
                                    'Week_time':now_song_week
                                }
                                Intermediate_Table.append(now_dict)
    Intermediate_Table = sorted(Intermediate_Table,key=lambda item:item['Song_ID'])
    with open("clean_data/Intermediate_Table.json",mode='w+',encoding='utf-8') as f:
        json.dump(Intermediate_Table,f,ensure_ascii=False,sort_keys=False,indent=4)

if __name__=="__main__":
    clean_data_ver2()
    build_Intermediate_Table()