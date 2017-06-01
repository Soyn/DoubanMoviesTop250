#!/usr/bin/env python
#-*-coding: utf-8 -*-


'''
    @Author: Soyn.
    @Brief: A web spider to get the page.
    @CreatedTime: 23/7/16.
    All rights reserved.
'''
import sys
import re
from collections import defaultdict
from bs4 import BeautifulSoup
import requests
import json
import random
import os
from utils.util import set_time_interval
reload(sys)
sys.setdefaultencoding("utf-8")

class DoubanSpider(object):
    '''
    @Brief: This class is to get the info we want.
    '''
    def __init__(self):
        """
        :param seed: the seed web page
        :keyword movies_info: the dictionary re[resent the info of movie
        :keyword current_page_content: the current web page contents
        :keyword top_num: the order of movies
        :keyword movies_links: the movie's link
        :keyword movies_names: the movie's name
        """
        self._current_page_number = 1
        self._seed = "https://movie.douban.com/top250?start={page}&filter="
        self._movies_info = defaultdict(list)
        self._current_page_content = ''
        self._top_num = 1
        self._movies_links = []
        self._movies_names = []
        self._movies_rates = []
        self._movies_distribute_countries = []
        self._ip_proxies = []
        self._current_proxy_ip = ''
        self._headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.7 Safari/537.36'}

    def get_page_content(self):
        """
        :return: page content
        """
        return self._current_page_content

    def get_movies_info(self):
        """
        :return: movies info
        """
        return self._movies_info
    def get_movies_link(self):
        """
        :return: movies link
        """
        return self._movies_links

    def get_movies_name(self):
        """
        :return: movies name
        """
        return self._movies_links
    def select_random_ip_proxy(self):
        ip_proxies_file = 'ip_proxies.json'
        with open(ip_proxies_file, 'r') as ip_proxies:
            self._ip_proxies = json.load(ip_proxies)
        print len(self._ip_proxies)
        self._current_proxy_ip = {'http', 'http://' + self._ip_proxies[random.randint(0, len(self._ip_proxies))]}


    def fetch_page_content(self):
        '''
        @Brief: Get the contents of specified url.
        :param url: The url
        :return: the contents of url
        '''
        print self._current_proxy_ip
        self._current_page_content = requests.get(self._seed.format(
                page=(self._current_page_number - 1) * 25), proxies=self._current_proxy_ip, headers=self._headers).text


    def parse_content_to_get_link(self):
        '''
        @Brief: Get the links from content
        :param contents: The contents of the specified url
        :return: links
        '''
        if self._current_page_content:
            soup = BeautifulSoup(self._current_page_content, 'lxml')
            # Extract the contents to get all the movies url
            for text in soup.find_all(attrs={'class': 'info'}):
                for link in text.find_all('a'):
                    print 'Insert the movie link......'
                    self._movies_links.append(link.get("href"))
        else:
            print 'Page contents is blank!'


    def parse_content_to_get_movie_names(self):
        """
        @Brief: Get the movie's name from content of current web page
        :return:
        """
        if self._current_page_content:
            movies_item = re.findall(r'<span class="title">(.*?)</span>',
                                self._current_page_content, re.S)
            for index, item in enumerate(movies_item):
                if item.find('&nbsp') == -1:
                    print 'Insert the movie name'
                    self._movies_names.append(item)
        else:
            print 'Page Content is blank!'

    def parse_content_to_get_movie_rate(self):
        """
        @Brief: Get the movies rate
        :return: the movie rate
        """
        if self._current_page_content:
            soup = BeautifulSoup(self._current_page_content, 'lxml')

            for span in soup.findAll('span', attrs={'property': 'v:average'}):
                print "Insert the movie name"
                self._movies_rates.append(span.string)
        else:
            print 'Page content is blank!'

    def parse_content_to_get_movie_distribute_country(self):
        """
        get the movies distribure country
        """
        if not self._movies_links:
            self.parse_content_to_get_link()
        links = self._movies_links
        for link in links:
            set_time_interval(1, 2)
            print "Insert distribute country......"
            content = requests.get(link, proxies=self._current_proxy_ip, headers=self._headers).text.decode('utf-8')
            distribute_country = re.findall(u'<span class="pl">制片国家/地区:</span>(.*?)<br/>', content, re.S)
            if not distribute_country:
                print content
                print link
            country = ''
            for item in distribute_country:
                if country:
                    item = '+' + item
                country += item
            self._movies_distribute_countries.append(country)

    def merge_names_and_urls(self):
        """
        @Brief: Merge the movie info
        :return: void
        """
        for movie_name, movie_rate, movie_url, movies_distribute_country in zip(self._movies_names,
                self._movies_rates, self._movies_links, self._movies_distribute_countries):
            print "Merge all the data......"
            self._movies_info[self._top_num].append(movie_name)
            self._movies_info[self._top_num].append(movie_rate)
            self._movies_info[self._top_num].append(movie_url)
            self._movies_info[self._top_num].append(movies_distribute_country)
            print self._top_num
            self._top_num += 1



    def start_spider(self, max_page_number = 1):
        '''
        @Brief: Start the spider
        :param max_page_number:
        :return: return the movies info
        '''
        if max_page_number < 0:
            max_page_number = 0  # If maximum page number less than 0, default value is 0
        if max_page_number > 10:
            max_page_number = 10  # Alternatively above

        while self._current_page_number <= max_page_number:
            self.fetch_page_content()
            set_time_interval(1, 2)  # set suspend time to avoid block
            self.parse_content_to_get_link()
            self.parse_content_to_get_movie_names()
            self.parse_content_to_get_movie_rate()
            self.parse_content_to_get_movie_distribute_country()
            self._current_page_number += 1
        self.merge_names_and_urls()

        self.generate_json_data()

    def generate_json_data(self):
        print 'Generating movies info file......'
        if self._movies_info:
            with open('../db/movies_info.json', 'w') as fp:
                json.dump(self._movies_info, fp)
        else:
            print "Info is empty!"


