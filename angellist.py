
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup


# In[2]:


import time


# In[3]:


import random


# In[4]:


import openpyxl


# In[5]:


import json


# In[6]:


import requests


# In[7]:


from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException


# In[8]:


book = openpyxl.load_workbook(r'C:\Users\windows\Desktop\Bigdata dataset\angellist.xlsx')
sheet=book.get_sheet_by_name("Sheet1")


# In[9]:


option = webdriver.ChromeOptions()
option.add_argument('— incognito')
option.add_argument('headless')


# In[10]:


browser=webdriver.Chrome(chrome_options=option)


# In[11]:


browser.get('https://angel.co/bangalore')


# In[12]:


user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]


# In[13]:


from itertools import cycle
import traceback
from lxml.html import fromstring
from requests.exceptions import ProxyError
from urllib3.exceptions import MaxRetryError
from http.client import HTTPException
def get_proxies():
#     url='https://raw.githubusercontent.com/a2u/free-proxy-list/master/free-proxy-list.txt'
#     response = requests.get(url)
#     proxies=set((response.text.split('\n'))[:-1])
    url = 'https://free-proxy-list.net/'
    print('getting proxies')
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies=set()
    for i in parser.xpath('//tbody/tr')[:60]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies


# In[ ]:


import traceback


# In[ ]:


def getDetails(url):
    print('current page:',url)
    proxies = get_proxies()
    proxy_pool = cycle(proxies)
    k=0
    while(True):
        if(k>30):
            break
        try:
            time.sleep(40) ##some delay between requests
            last_proxy=list(proxies)[-1]
            user_agent = random.choice(user_agent_list)
            proxy = next(proxy_pool)
            if(proxy==last_proxy):
                proxies=get_proxies()
                proxy_pool=cycle(proxies)
            r=requests.get(url,headers={'User-Agent': user_agent},proxies={"http": proxy, "https": proxy})
           # r=requests.get(url,headers={'User-Agent':user_agent})
            r.encoding='utf-8'
            soup = BeautifulSoup(r.content,'lxml')
            CompName=None
            MetaName=soup.find('meta',attrs={'property':'og:title'})
            if(MetaName!=None):
                CompName=MetaName.get('content',None)
            elif(soup.find('h1',attrs={'class':'u-fontWeight500 s-vgBottom0_5'})):
                CompName=soup.find('h1',attrs={'class':'u-fontWeight500 s-vgBottom0_5'}).text.strip()

            test=soup.find('li',attrs={'class':'role'})
            
            ContactName=None
            Designation=None
            
            if(soup.find('div',attrs={'class':'g-lockup larger top'})!=None):
                test=soup.find('div',attrs={'class':'g-lockup larger top'})
                if(test.find('div',attrs={'class':'name'})!=None):
                    ContactName=test.find('div',attrs={'class':'name'}).text.strip()
                if(test.find('div',attrs={'class':'bio'})!=None):
                    Designation=test.find('div',attrs={'class':'bio'}).text.strip().split(' ')[0]
            
            if(soup.find('div',attrs={'class':'g-lockup top larger'})!=None):
                test=soup.find('div',attrs={'class':'g-lockup top larger'})
                if(test.find('div',attrs={'class':'name'})!=None):
                    ContactName=test.find('div',attrs={'class':'name'}).text.strip()
                if(test.find('div',attrs={'class':'bio'})!=None):
                    Designation=test.find('div',attrs={'class':'bio'}).text.strip().split(' ')[0]
            
            Esize=None
            Website=None
            City=None

            Esize=soup.find('span',attrs={'class':'js-company_size'}).text.strip()
            Website=soup.find('a',attrs={'class':'u-uncoloredLink company_url'}).text.strip()


            City=soup.find('span',attrs={'class':'js-location_tags'}).text.strip().split('.')[0].split('-')[0].split('·')[0]
            if(City=='Bengaluru'):
                State='Karnataka'
            else:
                State=None
            StreetAddress=None
            Pincode=None
            Email=None
            Phone=None
            Mobile=None
            tupl=(CompName,ContactName,Designation,StreetAddress,City,State,Pincode,Email,Phone,Mobile,Website,Esize)        
            sheet.append(tupl)
            k=k+1
        except AttributeError as e:
            if(soup.find('h3',attrs={'class':'s-h3'})):
                print(soup.find('h3',attrs={'class':'s-h3'}).text.strip())
            else:
                traceback.print_exc()
            continue
        except ProxyError:
            print('connection error')
            continue
        except MaxRetryError:
            print('retry error')
            continue
        except OSError:
            print('OSError')
            continue
        except HTTPException:
            print('RemoteDisconnected')
            continue
        except TimeoutError:
            print('TimeoutError')
            continue
        except UnboundLocalError:
            continue
        book.save(r'C:\Users\windows\Desktop\Bigdata dataset\angellist.xlsx')
        if(Website):
            print(Website)
        break


# In[ ]:

## retry this block if you get an error about companies[0].find_elements_by_tag_name('a'):
i=0
while(True):
    print('page:',i)
    
    page=browser.find_elements_by_xpath("//div[@data-_tn='tags/show/results']")
    companies=[0]
    for x,y in enumerate(page):
        companies[0]=y
    print(companies)
    for urls in companies[0].find_elements_by_tag_name('a'):
        if(urls.get_attribute('title')):
            getDetails(urls.get_attribute('href'))
    more=browser.find_element_by_css_selector(".more.hidden")
    more.click()
    time.sleep(10)
    i=i+1
        
    
##sample Output

##page: 0
##[<selenium.webdriver.remote.webelement.WebElement (session="2da60857e4f8a42841deafc02e4b074f", element="0.13806904629619554-1")>]
##current page: https://angel.co/lookupto
##getting proxies
##lookup.to
##current page: https://angel.co/springrole
##getting proxies
##springrole.com
##current page: https://angel.co/semantics3
##getting proxies
