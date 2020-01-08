# coding: utf-8

import requests
from bs4 import BeautifulSoup
import html5lib

class Scraper():

    def __init__(self):
        pass

    def set_url(self, url):
        """Set url to be getted"""
        self.url = url

    def get_url(self):
        """Get the page with requests"""
        self.response = requests.get(self.url)
        self.text = self.response.text
        #self.urlList.append(response)

    def decode(self, encode="latin1", decode="utf-8"):
        """Encode and decode when there are encoding bugs"""
        self.text = self.response.text.encode(encode).decode(decode)

    def soup(self, parser="html5lib"):
        """Parse the requests result"""
        self.soup = BeautifulSoup(self.text, parser)

    def get_soup(self):
        """Return soup object"""
        return self.soup
