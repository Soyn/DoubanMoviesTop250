#!/use/bin/env python
#-*-coding:utf-8-*-

import os
import sys
import time
import random


def set_time_interval(start, end):
    '''
    Set the sleep N time, such start <= N <= end
    :param start:
    :param end:
    :return:
    '''
    time.sleep(random.randint(start, end))