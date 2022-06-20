import requests
from bs4 import BeautifulSoup 
import time
from unidecode import unidecode
import numpy as np
import random
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import threading
# -*- coding: latin2 -*-

### Get random user agent 
software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]   
user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
user_agents = user_agent_rotator.get_user_agents()

def product(URL,size):
    '''

    Parameters
    ----------
    URL : str
        url to product.
    size : str
        example: 'S'.

    Returns
    -------
    state_text : str
        returns string with state, size and product name.

    '''
    ### Random user agent
    user_agent = user_agent_rotator.get_random_user_agent()
    ### Send requests
    data = requests.get(URL, headers = {'User-Agent': user_agent})
    if data.status_code == 200:
        ### Parsing data
        soup = BeautifulSoup(data.text, 'html.parser')
        ### Get product size-selector and info__header
        containers = soup.find_all('div', class_ = 'product-detail-size-selector__size-list-wrapper product-detail-size-selector__size-list-wrapper--open')
        containers2 = soup.find_all('div', class_ = 'product-detail-info__header')
        ### Get containers
        first_element = containers[0]
        first_element2 = containers2[0]
        ### Find all sizes elements
        li = first_element.ul.find_all('li')
        ### look for disabled element in li
        dis = []
        for i in range(len(li)):
            disable_check = li[i].prettify()
            if 'disabled' in disable_check:
                txt= 'size: ' + li[i].span.text + ' Disabled'
                dis.append(txt)
            else:
                txt= 'size: ' + li[i].span.text + ' Enabled'
                dis.append(txt)
        ### Get size intrested in
        monit = []        
        for i in range(len(dis)):
            if size in dis[i]:
                monit.append((dis[i]))
        ### Get state of product availability
        if "Disabled" in monit[0]:
            state_text = unidecode('There is no the ' + size.upper()+ ' size from ' + first_element2.h1.text)
        else:
            state_text = unidecode('There is the ' + size.upper()+ ' size from ' + first_element2.h1.text)
            
        return state_text

URL = 'https://www.zara.com/pl/pl/sukienka-z-drapowaniem-p07385356.html?v1=186723196&v2=2026296'
def monit(URL):
    while True:
        state_text = product(URL, 'S')
        print(state_text)
monit(URL)   
                
   