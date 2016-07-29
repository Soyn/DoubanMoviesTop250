#!/usr/bin/env python
#-*-coding: utf-8 -*-

'''
    @Author: Soyn
    @Brief: The test for douban web spider
    @CreatedTime: 28/7/16
'''
import sys
sys.path.append("..")
from douban_web_spider import DoubanSpider
import time

def TestCase():
    test = DoubanSpider()
    movies_info = test.start_spider(12)
    for name in sorted(movies_info):
        print name + ' ' + movies_info[name]

if __name__ == '__main__':
    start = time.time()
    TestCase()
    end = time.time()
    print "Running Time: ", end - start
