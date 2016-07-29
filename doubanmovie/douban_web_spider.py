#!/usr/bin/env python
#-*-coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
'''
    @Author: Soyn.
    @Brief: A web spider to get the page.
    @CreatedTime: 23/7/16.
    All rights reserved.
'''
import re

class ExtractData(object):
    '''
    @Brief: Extract data
    '''

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
        self.current_page_number = 1
        self.seed = "https://movie.douban.com/top250?start={page}&filter="
        self.movies_info = {}
        self.current_page_content = ''
        self.top_num = 1
        self.movies_links = []
        self.movies_names = []
        self.top_num = 1


    def get_page(self):
        '''
        @Brief: Get the contents of specified url.
        :param url: The url
        :return: the contents of url
        '''
        try:
            import requests
            self.current_page_content = requests.get(self.seed.format(page
                        =(self.current_page_number - 1) * 25)).text
        except:
            return ''

    def get_links(self):
        '''
        @Brief: Get the links from content
        :param contents: The contents of the specified url
        :return: links
        '''
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            from BeautifulSoup import BeautifulSoup
        soup = BeautifulSoup(self.current_page_content, 'lxml')

        # Extract the contents to get all the movies url
        for text in soup.find_all(attrs = {'class': 'item'}):
            for link in text.find_all('a'):
                self.movies_links.append(link.get("href"))

    def get_movie_names(self):
        """
        @Brief: Get the movie's name from content of current web page
        :return:
        """
        movies_item = re.findall(r'<span class="title">(.*?)</span>',self.current_page_content, re.S)
        for index, item in enumerate(movies_item):
            if item.find('&nbsp') == -1:
                self.movies_names.append('Top ' + str(self.top_num) + ' ' + item)
                self.top_num += 1

    def merge_names_and_urls(self):
        for movie_name, movie_url in zip(self.movies_names, self.movies_links):
            self.movies_info[movie_name] = movie_url


    def start_spider(self, max_page_number):
        '''
        @Brief: Start the spider
        :param max_page_number:
        :return: return the movies info
        '''
        if max_page_number < 0:
            max_page_number = 0
        if max_page_number > 10:
            max_page_number = 10
        while self.current_page_number <= max_page_number:
            self.get_page()
            self.get_links()
            self.get_movie_names()
            self.merge_names_and_urls()
            self.current_page_number += 1

        return_movies_info = self.movies_info
        return return_movies_info





        

