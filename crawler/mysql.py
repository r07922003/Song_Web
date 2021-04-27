"""Mysql connection and query"""

import pymysql

class python_SQL():
    def __init__(self,db_settings):
        self.db_settings = db_settings
        self.connection = None
        self.cursor = None
        
    def show_tables(self):
        if self.connection:
            with self.cursor as my_cursor:
                my_cursor.execute("show tables;")
                for line in my_cursor.fetchall():
                    print(line)
            self.cursor = self.connection.cursor()
        else:
            print("no connection")
    
    def show_table_info(self,table_name):
        output = []
        if self.connection:
            cmd = "SELECT * FROM "+table_name
            with self.cursor as my_cursor:
                my_cursor.execute("SHOW COLUMNS FROM %s;" %table_name)
                text = ""
                for line in my_cursor.fetchall():
                    text+= "| "+line[0]+" |"
                print(text)
                my_cursor.execute(cmd)
                for line in my_cursor.fetchall():
                    print(line)
                    output.append(line)
            self.cursor = self.connection.cursor()
        else:
            print("no connection")
        return output
        
    def connect_to_SqlServer(self):
        try:
            self.connection = pymysql.connect(**self.db_settings)
            self.cursor = self.connection.cursor()
            #print("connect to %s@%s:%d sucessful" %(db_settings['user'],db_settings['host'],db_settings['port']))
        except Exception as ex:
            print("connect fail:",ex)
            
    def close(self):
        self.connection.close()
        self.connection = None
        
    def create_single_toplist_table(self,table_name,category):
        #create 各別的單一的 table 並非整合到統一一個table中
        if table_name== "Kugou_toplist":
            table_type = "(\
                            toplist_ID int NOT NULL PRIMARY KEY,\
                            toplist_Name varchar(50) character set utf8 NOT NULL,\
                            update_frequency varchar(25) character set utf8 NOT NULL\
                        );"
            insert_command = "insert into "+table_name+"(toplist_ID,toplist_Name,update_frequency)values(%d,'%s','%s')"
        else:
            table_type = "(\
                            toplist_ID int NOT NULL PRIMARY KEY,\
                            toplist_Name varchar(50) character set utf8 NOT NULL\
                        );"
            insert_command = "insert into "+table_name+"(toplist_ID,toplist_Name)values(%d,'%s')"
            
        create_table_command = "create table "+ table_name +" "+ table_type
        if self.connection:
            with self.cursor as my_cursor:
                
                my_cursor.execute(create_table_command)
                    
                if table_name=="Kugou_toplist":
                    for ID in category:
                        print(insert_command %(int(ID),category[ID]['rankname'],category[ID]['update_frequency']))
                        my_cursor.execute(insert_command %(int(ID),category[ID]['rankname'],category[ID]['update_frequency']))
                if table_name=="NetEase_toplist":
                    for ID in category:
                        print(insert_command %(int(ID),category[ID]['name']))
                        my_cursor.execute(insert_command %(int(ID),category[ID]['name']))
                else:
                    for ID in category:
                        print(insert_command %(int(ID),category[ID]))
                        my_cursor.execute(insert_command %(int(ID),category[ID]))
            self.connection.commit()
            self.cursor = self.connection.cursor()

        else:
            print("no connection")
            
    def create_toplist_table(self,table_name,category):
        table_type = "(\
                        Toplist_ID int NOT NULL PRIMARY KEY,\
                        Name varchar(50) character set utf8 NOT NULL,\
                        Origin_ID bigint NOT NULL,\
                        Platform_ID int NOT NULL\
                    );"
        insert_command = "insert into "+table_name+"(Toplist_ID,Name,Origin_ID,Platform_ID)values(%d,'%s',%d,%d)"
            
        create_table_command = "create table "+ table_name +" "+ table_type
        if self.connection:
            with self.cursor as my_cursor:
                
                my_cursor.execute(create_table_command)
                
                for i in range(len(category)):
                    now_ID = i*100 + 1
                    now = sorted(category[i].items(), key=lambda d: int(d[0]))
                    for line in now:
                        if i==1:
                            my_cursor.execute(insert_command %(int(now_ID),line[1]['rankname'],int(line[0]),int(i+1)))
                        elif i==3:
                            my_cursor.execute(insert_command %(int(now_ID),line[1]['name'],int(line[0]),int(i+1)))
                        else:
                            my_cursor.execute(insert_command %(int(now_ID),line[1],int(line[0]),int(i+1)))
                        now_ID += 1
            self.connection.commit()
            self.cursor = self.connection.cursor()    
        
    def create_platform_table(self):
        table_name = "Platform"
        table_type = "(\
                        Platform_ID int NOT NULL PRIMARY KEY,\
                        Name varchar(50) character set utf8 NOT NULL\
                    );"
        
        insert_command = "insert into "+table_name+"(Platform_ID,Name)values(%d,'%s')"
        create_table_command = "create table "+ table_name +" "+ table_type
        
        if self.connection:
            with self.cursor as my_cursor:
                my_cursor.execute(create_table_command)
                my_cursor.execute(insert_command %(int(1),'QQ'))
                my_cursor.execute(insert_command %(int(2),'Kugou'))
                my_cursor.execute(insert_command %(int(3),'Kuwo'))
                my_cursor.execute(insert_command %(int(4),'NetEase'))
        self.connection.commit()
        self.cursor = self.connection.cursor()
