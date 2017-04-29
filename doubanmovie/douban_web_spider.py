#!/usr/bin/env python
#-*-coding: utf-8 -*-


'''
    @Author: Soyn.
    @Brief: A web spider to get the page.
    @CreatedTime: 23/7/16.
    All rights reserved.
'''
import re
from collections import defaultdict


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
        self.movies_info = defaultdict(list)
        self.current_page_content = ''
        self.top_num = 1
        self.movies_links = []
        self.movies_names = []
        self.movies_rates = []
        self.movies_distribute_countries = []

    def get_page(self):
        '''
        @Brief: Get the contents of specified url.
        :param url: The url
        :return: the contents of url
        '''
        try:
            import requests

            self.current_page_content = requests.get(self.seed.format(
                page = (self.current_page_number - 1) * 25)).text
        except:
            print "import requests failed!"
            return ""


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
        movies_item = re.findall(r'<span class="title">(.*?)</span>',
                                self.current_page_content, re.S)
        for index, item in enumerate(movies_item):
            if item.find('&nbsp') == -1:
                self.movies_names.append(item)

    def get_movies_rate(self):
        """
        @Brief: Get the movies rate
        :return: the movie rate
        """
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            from BeautifulSoup import BeautifulSoup

        soup = BeautifulSoup(self.current_page_content, 'lxml')

        for span in soup.findAll('span', attrs={'property':'v:average'}):
            self.movies_rates.append(span.string)

    def get_movies_distribute_country(self):
        """
        Get the distribute country of movie
        :return:
        """
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            from BeautifulSoup import BeautifulSoup

        soup = BeautifulSoup(self.current_page_content, 'lxml')

        movies_div = soup.findAll('div', attrs={'class': 'bd'})

        for div in movies_div:
            element = div.find('p', attrs = {'class': ''})
            if element:
                string_element = str(element.text.encode('utf8'))
                index_list = []
                for i in range(2):
                    index = string_element.rfind('/')
                    string_element = string_element[0 : index]
                    index_list.insert(0, index)
                country = str(element.text.encode('utf8'))[index_list[0] + 1: index_list[1]]
                self.movies_distribute_countries.append(country[0 : country.find(' ')])


    def merge_names_and_urls(self):
        """
        @Brief: Merge the movie info
        :return: void
        """
        for movie_name, movie_rate, movie_url, movies_distribute_country in zip(self.movies_names,
                self.movies_rates, self.movies_links, self.movies_distribute_countries):
            self.movies_info[self.top_num].append(movie_name)
            self.movies_info[self.top_num].append(movie_rate)
            self.movies_info[self.top_num].append(movie_url)
            self.movies_info[self.top_num].append(movies_distribute_country)
            self.top_num += 1



    def start_spider(self, max_page_number = 0):
        '''
        @Brief: Start the spider
        :param max_page_number:
        :return: return the movies info
        '''
        if max_page_number < 0:
            max_page_number = 0  # If maximum page number less than 0, default value is 0
        if max_page_number > 10:
            max_page_number = 10 # Alternatively above

        while self.current_page_number <= max_page_number:
            self.get_page()
            self.get_links()
            self.get_movie_names()
            self.get_movies_rate()
            self.get_movies_distribute_country()
            self.current_page_number += 1
        self.merge_names_and_urls()
        return_movies_info = self.movies_info
        return return_movies_info



        

