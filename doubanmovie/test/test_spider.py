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

def test_case():
    test = DoubanSpider()
    movies_info = test.start_spider(12)

if __name__ == '__main__':
    start = time.time()
    test_case()
    end = time.time()
    print "Running Time: ", end - start
