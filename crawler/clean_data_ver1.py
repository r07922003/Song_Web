"""
clean data

(1) 取四個platform共同的欄位 songname|album_name|duration|singer name|lyrics

                toplist song table attribute
QQ:         songname|song orig name|date|all comment_num|album_name|interval,duration|singer name|lyrics|
Kugou:      songname|              |date|               |album_name|interval,duration|singer name|lyrics|play_url
kuwo:       songname|              |date|               |album_name|interval,duration|singer name|lyrics|        |score100
NetEase:    songname|              |date|               |album_name|interval,duration|singer name|lyrics|                 |all playCount|all shareCount|all commentCount|company
"""


import os
import json
import time
import mysql
from config import db_settings,default

file_path = default.file_path
platform = {
    'QQ':0,
    "Kugou":1,
    "kuwo":2,
    "NetEase":3
}
platform_file = {}
sql = mysql.python_SQL(db_settings)
sql.connect_to_SqlServer()

def generate_song_data(songname,singer_name,week_time,album_name,interval,lyrics,rank):
    song_data = {}
    song_data['songname'] = songname
    song_data['singer_name'] = singer_name
    song_data['week_date'] = week_time
    song_data['album_name'] = album_name
    song_data['interval'] = interval
    song_data['lyrics'] = lyrics
    song_data['rank'] = rank
    return song_data

if __name__ == "__main__":

    now_data = {}
    week_time = int((time.time()-1615737600)/604800)+1

    for i in platform:
        all_file = os.listdir(file_path+i)
        for file in all_file:
            struct_time = file.split(".json")[0].split('dict_')[1]
            struct_time = time.strptime(struct_time,"%Y_%m_%d_%H_%M_%S")
            time_stamp = int(time.mktime(struct_time))
            time_week = int((time_stamp-1615737600)/604800)+1
            if time_week ==week_time:
                print(i,file)
                with open(file_path+i+"/"+file,'r',encoding='utf-8') as f:
                    data = json.load(f)
                platform_file[i] = data  
                
    for i in platform_file:
        now_data[i]={}
        for origin_ID in platform_file[i]:
            if sql.connection:
                with sql.cursor as my_cursor:
                    my_cursor.execute("select Toplist_ID  FROM Toplist where Origin_ID=%d and Platform_ID=%d" %(int(origin_ID),platform[i]+1))
                    now_toplist_ID = (my_cursor.fetchall()[0][0])
            sql.cursor = sql.connection.cursor()
            
            now_data[i][now_toplist_ID]=[]
            rank = 1
            
            if platform[i]==0:
                song_dict = platform_file[i][origin_ID]
                for song in song_dict['songlist']:
                    album_name = song['data']['albumname']
                    interval = song['data']['interval']
                    text = ""
                    for tsm in song['data']['singer']:
                        text += tsm['name']+"、"
                    singer_name = text
                    songname = song['data']['songname']
                    lyrics = song['data']['lyric']
                    temp = generate_song_data(songname,singer_name,week_time,album_name,interval,lyrics,rank)
                    now_data[i][now_toplist_ID].append(temp)
                    rank += 1
                    
            if platform[i]==1:
                song_dict = platform_file[i][origin_ID]
                for song in song_dict['data']['info']:
                    songname = song['sond_detail']['song_name']
                    album_name = song['sond_detail']['album_name']
                    singer_name = song['sond_detail']['author_name']
                    lyrics = song['sond_detail']['lyrics']
                    interval = song['duration']
                    temp = generate_song_data(songname,singer_name,week_time,album_name,interval,lyrics,rank)
                    now_data[i][now_toplist_ID].append(temp)
                    rank += 1
                
            if platform[i]==2:
                song_dict = platform_file[i][origin_ID]
                for song in song_dict['data']['musicList']:
                    singer_name = song['artist']
                    interval = song['duration']
                    album_name = song['album']
                    songname = song['name']
                    lyrics = song['lyric']
                    temp = generate_song_data(songname,singer_name,week_time,album_name,interval,lyrics,rank)   
                    now_data[i][now_toplist_ID].append(temp)
                    rank += 1
                
                    
            if platform[i]==3:
                for song in platform_file[i][origin_ID]['result']['tracks']:
                    songname = song['name']
                    text = ""
                    for tsm in song['artists']:
                        text += tsm['name']+"、"
                    singer_name = text
                    album_name = song['album']['name']
                    interval = song['duration']
                    lyrics = song['lyric']
                    temp = generate_song_data(songname,singer_name,week_time,album_name,interval,lyrics,rank)
                    now_data[i][now_toplist_ID].append(temp)
                    rank += 1   
                    
    with open("clean_data/"+str(week_time)+".json",mode='w+',encoding='utf-8') as f:
        json.dump(now_data,f,ensure_ascii=False,sort_keys=False,indent=4)
    print("save done")
