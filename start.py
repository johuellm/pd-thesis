# -*- coding: utf-8 -*-
"""The purpose of this module is solely to implement start"""

import time
import random
from random import randint
from configparser import SafeConfigParser
from selenium import webdriver
import pickle
import liker
from liker import *
from Support import *
from PriceWebScraper import priceWebScraper

class start():
    """
    This class implements start(), which
    automatically executes all specified liker-methods
    for each specified user/profile and the priceWebScraper
    """
    def start():

        """
        Consists of two loops:
        -The outer loop uses the profile names, locations and proxy-data of the firefox profiles to create
        a selenium driver for each user.
        -The inner loop executes the specified methods by reading them
        from the liker-folder

        Args:
            all external arguments are strings from the config.ini
        """

        _config = SafeConfigParser()
        _config.read('config.ini')

        _methods = _config.get('methods', 'liker').split()
        _scraperUsed = _config.get('methods', 'scraper')
        _user = _config.get('user', 'used').split()

        _cookieDirectory = _config.get('directories', 'cookieDirectory')
        _profileDirectory = _config.get('directories', 'profileDirectory')

        _driverArray = []

        for _usr in _user:
            print(_usr)
            _tmpProfile = webdriver.FirefoxProfile(_profileDirectory +
                                                    _config.get('profiles', _usr))

            _driver = webdriver.Firefox(firefox_profile=_tmpProfile)
                #,capabilities=support.proxy(_config.get('proxy', _usr)))

            for _mthd in _methods:
                _page = _mthd.replace('Liker', '')
                print(_mthd)
                support.loader(_driver, _usr, _page, _cookieDirectory)
                #the getattr functions navigate through the folder structure
                _tmp = getattr(liker, _mthd)    #_tmp equals liker._mthdLiker
                _tmp2 = getattr(_tmp, _mthd)    #_tmp2 equals liker._mthdLiker._mthdLiker
                _tmp3 = getattr(_tmp2, _mthd)   #_tmp3 equals liker._mthdLiker._mthdLiker._mthdLiker
                _tmp3(_driver, _config.get('interests', _usr).split())
                _page = _page.title()
                support.dumper(_driver, _usr, _page, _cookieDirectory)

            _driverArray.append(_driver)

        #quit all drivers
        if (_scraperUsed == "True"):
            priceWebScraper.scrapePrices(_driverArray)
            #for _driver in _driverArray:
              #_driver.quit()

    start()
