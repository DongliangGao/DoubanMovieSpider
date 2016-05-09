# -*- coding:utf-8 -*-

import urllib2
import re
import tool
import mysql

class Douban:

    def __init__(self):
        self.start_url = 'https://movie.douban.com/top250'
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0'
        self.headers = { 'User_Agent': self.user_agent }
        self.sql = mysql.MySQL()
        self.tool = tool.Tool()

    def getPage(self, URL):
        '''
        传入URL,提取页面信息
        :param URL:
        :return:
        '''
        request = urllib2.Request(URL, headers = self.headers)
        response = urllib2.urlopen(request)
        page =  response.read().decode('utf-8')
        if page:
            return page
        else:
            print '获取页面信息失败'
            return None

    def getURL(self, page):
        '''
        传入页面信息，提取下一页的URL
        :param page:
        :return:
        '''
        parrent = re.compile('<link rel="next" href="(.*?)"/>', re.S)
        items = re.findall(parrent, page)
        pattern1 = re.compile('&amp;')
        if items:
            url = re.sub(pattern1, "&", items[0])
            return url

    def writeData(self, page):
        '''
        将提取的电影信息写入数据库
        :param page:
        :return:
        '''
        parrent = re.compile(u'<span class="title">([^&nbsp].*?)</span>.*?<p class="">(.*?)&nbsp;&nbsp;&nbsp;(.*?)<br>(.*?)&nbsp;/&nbsp;(.*?)&nbsp;/&nbsp;(.*?)</p>.*?<span class="rating_num" property="v:average">(.*?)</span>.*?<span class="inq">(.*?)</span>', re.S)
        items = re.findall(parrent, page)
        for item in items:
            item1 = self.tool.replace1(item[1])
            item3 = self.tool.replace1(item[3])
            item5 = self.tool.replace2(item[5])
            # 用[3:]去除“导演：”和“演员：”
            dic = {'NAME': item[0], 'DIRECTOR':item1[3:], 'ACTOR': item[2][3:], 'YEARS': item3, 'COUNTRY': item[4], 'CATEGORY': item5, 'RATING': item[6], 'QUOTE': item[7]}
            self.sql.insertData(dic)

    def main(self):
        self.sql.createTable(self.sql.db, self.sql.cur)
        url = '?start=0&filter='
        while url:
            URL = self.start_url + url
            page = self.getPage(URL)
            self.writeData(page)
            url = self.getURL(page)
        self.sql.db.commit()
        self.sql.db.close()


douban = Douban()
douban.main()