# -*- coding:utf-8 -*-

import MySQLdb

class MySQL:
    '''
    数据库操作：连接、建表、插入数据
    '''

    def __init__(self):
        try:
            self.db = MySQLdb.connect('localhost', 'root', 'password', 'douban', charset = 'utf8')
            try:
                self.cur = self.db.cursor()
            except MySQLdb.Error, e:
                print '获取操作游标失败%d：%s' % (e.args[0], e.args[1])
        except MySQLdb.Error, e:
            print '连接数据库失败%d：%s' % (e.args[0], e.args[1])

    def createTable(self, db, cursor):
        '''
        建立数据表：doubanmovie
        :param db: 数据库
        :param cursor: 游标
        :return:
        '''
        try:
            cursor.execute('DROP TABLE IF EXISTS DOUBANMOVIE;')
            sql = '''
            CREATE TABLE DOUBANMOVIE(
            NAME VARCHAR(200) NOT NULL,
            DIRECTOR VARCHAR(200),
            ACTOR VARCHAR(200),
            YEARS VARCHAR(50) NOT NULL,
            COUNTRY VARCHAR(100),
            CATEGORY VARCHAR(100),
            RATING FLOAT NOT NULL,
            QUOTE VARCHAR(200)
            );
            '''
            cursor.execute(sql)
        except MySQLdb.Error, e:
            db.rollback()
            print '创建数据表失败%d：%s' % (e.args[0], e.args[1])

    def insertData(self, dic):
        '''
        传入字典，根据字典内容，插入数据
        :param dic: 包含数据的字典
        :return:
        '''
        cols = ', '.join(dic.keys())
        values = '", "'.join(dic.values())
        sql = 'INSERT INTO DOUBANMOVIE (%s) VALUES (%s);' % (cols, '"'+values+'"')
        try:
            self.cur.execute(sql)
        except MySQLdb.Error, e:
             print '插入数据失败%d：%s' % (e.args[0], e.args[1])