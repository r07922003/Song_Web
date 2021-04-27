#QQ 酷我 酷播 網易雲 爬下來的json轉成.csv
import xlsxwriter
import time

class QQ_Kuwo_csv_arry():
    def __init__(self):
        self.top_list_row = []
        self.song_list_row = []

    def dict_to_array(self,Dict):
        for i in Dict:
            if type(Dict[i])==dict:
                self.dict_to_array(Dict[i])
                
            elif type(Dict[i])==list:
                for line_num in range(len(Dict[i])):
                    self.create_song_list(Dict[i][line_num],line_num)
                    
            else:
                if self.top_list_row:
                    self.top_list_row[0].append(i)
                    self.top_list_row[1].append(Dict[i])
                else:
                    self.top_list_row.append([i])
                    self.top_list_row.append([Dict[i]])
                    
    def create_song_list(self,List,line_num):
        if line_num==0:
            for i in List:
                if type(List[i])==dict:
                    self.create_song_list(List[i],line_num)
                elif type(List[i])==list:
                    singer_string=""
                    for singer in List[i]:
                        for k in singer:
                            singer_string+= str(k)+":"+str(singer[k])+" "
                    if self.song_list_row:
                        self.song_list_row[0].append(i)
                        self.song_list_row[1].append(singer_string)
                    else:
                        self.song_list_row.append([i])
                        self.song_list_row.append([singer_string])
                    
                    
                else:
                    if self.song_list_row:
                        self.song_list_row[0].append(i)
                        self.song_list_row[1].append(List[i])
                    else:
                        self.song_list_row.append([i])
                        self.song_list_row.append([List[i]])
        else:
            if line_num+2 > len(self.song_list_row):
                self.song_list_row.append([])
                
            for i in List:
                if type(List[i])==dict:
                    self.create_song_list(List[i],line_num)
                elif type(List[i])==list:
                    singer_string=""
                    for singer in List[i]:
                        for k in singer:
                            singer_string+= str(k)+":"+str(singer[k])+" "
                    self.song_list_row[-1].append(singer_string)
                    
                else:
                    self.song_list_row[-1].append(List[i])
            
    def save_to_xlsx(self,QQ_dict,file_num):
        now_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())    
        if file_num==0:
            filename = "QQ_"+str(now_time)+".xlsx"
        else:
            filename = "Kuwo_"+str(now_time)+".xlsx"
        wb = xlsxwriter.Workbook(filename)
        for key in QQ_dict:
            csv_array = QQ_Kuwo_csv_arry()
            csv_array.dict_to_array(QQ_dict[key])

            ws = wb.add_worksheet(key)

            for row_num, data in enumerate(csv_array.top_list_row):
                for column_num, Data in enumerate(data):
                    ws.write_string(row_num,column_num, str(Data))
            for row_num, data in enumerate(csv_array.song_list_row):
                for column_num, Data in enumerate(data):
                    ws.write_string(row_num+2,column_num, str(Data))
        wb.close()
        
        
class NetEase_csv_arry():
    def __init__(self):
        self.top_list_row = []
        self.song_list_row = []
        
    def dict_to_array(self,Dict):
        for i in Dict:
            if type(Dict[i])==dict:
                self.dict_to_array(Dict[i])
                
            elif i=='tracks':
                for line_num in range(len(Dict[i])):
                    self.create_song_list(Dict[i][line_num],line_num,"")
                
            elif type(Dict[i]) ==list and i!='expertTags':
                string = ""
                for word in Dict[i]:
                    string += str(word)+" "
                if self.top_list_row:
                    self.top_list_row[0].append(i)
                    self.top_list_row[1].append(string)
                else:
                    self.top_list_row.append([i])
                    self.top_list_row.append([string])
            else:
                if self.top_list_row:
                    self.top_list_row[0].append(i)
                    self.top_list_row[1].append(Dict[i])
                else:
                    self.top_list_row.append([i])
                    self.top_list_row.append([Dict[i]])
                    
    def create_song_list(self,List,line_num,key_name):
        if line_num==0:
            for i in List:
                if type(List[i])==dict:
                    self.create_song_list(List[i],line_num,i)
                elif type(List[i])==list:
                    singer_string=""
                    for singer in List[i]:
                        if singer==dict:
                            for k in singer:
                                singer_string+= str(k)+":"+str(singer[k])+" "
                        else:
                            singer_string += str(singer)+"_" 
                    if self.song_list_row:
                        self.song_list_row[0].append(i)
                        self.song_list_row[1].append(singer_string)
                    else:
                        self.song_list_row.append([i])
                        self.song_list_row.append([singer_string])
                    
                    
                else:
                    if self.song_list_row:
                        self.song_list_row[0].append(key_name+i)
                        self.song_list_row[1].append(List[i])
                    else:
                        self.song_list_row.append([key_name+i])
                        self.song_list_row.append([List[i]])
                        
        else:
            if line_num+2 > len(self.song_list_row):
                self.song_list_row.append([])
                
            for i in List:
                if type(List[i])==dict:
                    self.create_song_list(List[i],line_num,i)
                elif type(List[i])==list:
                    singer_string=""
                    
                    for singer in List[i]:
                        if singer==dict:
                            for k in singer:
                                singer_string+= str(k)+":"+str(singer[k])+" "
                        else:
                            singer_string += str(singer)+"_" 
                    self.song_list_row[-1].append(singer_string)
                    
                else:
                    self.song_list_row[-1].append(List[i])
                    
    def save_to_xlsx(self,NetEase_dict):
        now_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())    
        filename = "NetEase_"+str(now_time)+".xlsx"
        wb = xlsxwriter.Workbook(filename)
        for key in NetEase_dict:
            csv_array = NetEase_csv_arry()
            csv_array.dict_to_array(NetEase_dict[key])

            ws = wb.add_worksheet(key)

            for row_num, data in enumerate(csv_array.top_list_row):
                for column_num, Data in enumerate(data):
                    ws.write_string(row_num,column_num, str(Data))
            for row_num, data in enumerate(csv_array.song_list_row):
                for column_num, Data in enumerate(data):
                    ws.write_string(row_num+2,column_num, str(Data))
        wb.close()