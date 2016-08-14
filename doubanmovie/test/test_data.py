#!usr/bin/env python
#-*-coding:utf-8-*-

import sys
sys.path.append('..')

"""
    @Author: Soyn
    @Brief: The test for data
    @CreatedTime: 14/8/16
"""
from data import DBProcess

def test():
    test = DBProcess()
    test.create_table()
    test.insert_data()

if __name__ == '__main__':
    test()