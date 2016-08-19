#!usr/bin/env python
#-*-coding:utf-8-*-

'''
    @Author: Soyn
    @Brief: Storage the data from web sider in database
    @CreatedTime: 14/8/16
'''
import sqlite3
import douban_web_spider

class DBProcess(object):
    def __init__(self, db_file = 'dou_ban_movies_info.sqlite'):
        self.db_file = db_file
        self.table_name = 'dou_ban_movies_info'
        self.name = 'Name'
        self.rate = 'Rate'
        self.rank = 'Rank'
        self.distribute_country = 'DistributeCountry'

    def create_table(self):
        """
        @Brief: Create the database table in current work path
        :return: No return
        """
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("""
                DROP TABLE IF EXISTS dou_ban_movies_info
            """)
            cursor.execute("""
                CREATE TABLE {table_name} (
                    {Rank} {RankType},
                    {Name} {NameType} PRIMARY KEY,
                    {Rate} {RateType},
                    {DistributeCountry} {DistributeCountryType}
                );
            """.format(table_name=self.table_name, Rank =self.rank, RankType
                ='INTEGER', Name=self.name, NameType='TEXT',
                    Rate=self.rate, RateType='TEXT',
                    DistributeCountry = self.distribute_country, DistributeCountryType = 'TEXT'))
            conn.commit()
            conn.close()
            print "------Create table successfully!------"

        except sqlite3.Error:
            print "Connect database failed!"
            return

    def insert_data(self):
        """
        @Brief: Insert data into table
        :return:
        """
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        spider = douban_web_spider.DoubanSpider()
        movies_info = spider.start_spider(12)
        for key in movies_info:
            params = (key, movies_info[key][0], movies_info[key][1], movies_info[key][3])
            print movies_info[key][3]
            cursor.execute("""
                INSERT INTO dou_ban_movies_info (Rank, Name, Rate, DistributeCountry) VALUES
                (?, ?, ?, ?)
            """, params)
        conn.commit()
        conn.close()
        print "----Insertion completes!----"

