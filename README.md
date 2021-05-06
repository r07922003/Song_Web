# Bmat Song Crawler
[-Demo Link (heroku)](https://bmat-chart.herokuapp.com/)\
[-Demo Link (AWS ec2)](https://chart.dwave.cc/)\
-Nelson 2021.04.26

## 爬取資料
### 目前平台:
1. QQ
2. Kugou
3. NetEase

### 開始爬取日期: 3/15
### Timestamp: 1615737600
### Bmat S3 bucket_name: s3://bmat.charts.shared/deepwave/
## 資料夾格式
>-Web
>> -category
>>> Kugou_category.json
>>> 
>>> kuwo_category.json
>>> 
>>> NetEase_category.json
>>> 
>>> QQ_category.json
>>
>> -config
>>> setting.json
>>
>> clean_data_ver1.py
>> 
>> clear_data_ver2.py
>> 
>> config.py
>> 
>> crawler.py
>> 
>> json_to_xlsx.py
>> 
>> mysql.py
##  執行過程
- Step 1. **創建platform's category json檔案**
- Step 2. **讀取category json檔，根據origin toplist ID抓取當周的排行榜音樂資訊**
- Step 3. **抓每首歌的詳細信息 (Lyrics)**
- Step 4. **Data cleaning**
- Step 5. **Build Song Table**
- Step 6. **Build Intermediate_Table**

![](https://i.imgur.com/5z45oM6.png)
## crawler.py
```
$ python crawler.py --action all --xlsx False
--action  platformname  platform to be crawlered
--xlsx    boolean       Output xlsx or not,now just support QQ and NetEase
```

## clean_data_ver1.py
取四個platform共同欄位 
+ songname
+ album_name
+ duration
+ singer name
+ lyrics
## clean_data_ver2.py
+ Increasing songID
+ Building Song Table
+ Building Intermediate_Table
# DataBase Design
![](https://i.imgur.com/nYThFPX.png)
