# -*- coding:utf-8 -*-

import re

class Tool:
    '''
    对提取的内容进行清洗，去除换行和空格
    '''

    def replace1(self, s):
        parrent = re.compile("\n                            ", re.S)
        s = re.sub(parrent, '', s)
        return s

    def replace2(self, s):
        parrent = re.compile("\n                        ", re.S)
        s = re.sub(parrent, '', s)
        return s