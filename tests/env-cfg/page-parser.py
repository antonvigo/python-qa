#!/usr/bin/env python3
# This module is just for studying only!

import requests
import uuid

from bs4 import BeautifulSoup
from robobrowser import RoboBrowser

## Main function
if __name__ == '__main__':
#    web_page = requests.post('http://unoume-qa12.devops.rebrain.srwx.net/calc', 
#        data={'operation':'3,+,18'}).text
#    web_page = requests.post('http://unoume-qa12.devops.rebrain.srwx.net/calc', 
#        data={'operation':'49,-,17'}).text
#    web_page = requests.get('http://unoume-qa12.devops.rebrain.srwx.net').text
#    web_page = requests.post('http://unoume-qa12.devops.rebrain.srwx.net/cleanup').text
#    web_page = requests.get('http://unoume-qa12.devops.rebrain.srwx.net/results_secret').text

#    soup = BeautifulSoup(web_page, 'html.parser')

#    print(str(soup.find(id = "operation").string) == '3,+,18')
#    print(str(soup.find(id = "result").string))

#    print(soup.find('input', {'name':'operation'}).nextSibling.nextSibling.get('value') == 'Посчитать')
#    print(soup.find('input', {'name':'operation'}).get('type') == 'text' and 
#        soup.find('input', {'value':'Посчитать'}).get('type') == 'submit')

#    print(web_page == 'Database cleared')

#    for child in soup.findAll("tr")[2].children:
##        if child.next_element.name != 'a':
#            print(child.string)
