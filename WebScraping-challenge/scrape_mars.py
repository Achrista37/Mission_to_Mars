#!/usr/bin/env python
# coding: utf-8

# In[58]:


#Load dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import os
import re
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt


# In[59]:

def scrape():
    #set up splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    # ####NASA MARS NEWS


    url = "https://redplanetscience.com/"
    browser.visit(url)



    #Convert to a beautiful soup object
    html = browser.html
    mars_soup = bs(html, 'html.parser')
    print(mars_soup.prettify())


# In[62]:


    #get all lines with div with class = content_title
    newstitle_list = mars_soup.select('div.content_title')

    #create a list to contain the titles
    newstitle_list_notag = []

    #create a for loop to take off the html tags from the titles and put clean titles into the list
    for n in newstitle_list:
        newstitle_list_notag.append(n.text)
    newstitle_list_notag
    

# In[63]:


    #get all lines with div with class = article_teaser_body
    newsp_list = mars_soup.select('div.article_teaser_body')

    #create a list to contain the news paragraphs
    newsp_list_notag = []

    #create a for loop to take off the html tags from the news paragraphs and put clean texts into the list
    for p in newsp_list:
        newsp_list_notag.append(p.text)
    newsp_list_notag

    news_list = list(zip(newsp_list_notag, newstitle_list_notag))
# JPL Mars Space Images - Featured Image

# In[64]:


    url2 = "https://spaceimages-mars.com"
    browser.visit(url2)
    html2 = browser.html
    marsimg_soup = bs(html2, 'html.parser')


# In[65]:


    browser.find_by_tag('button')[1].click()


    # In[66]:


    relative_image_url = browser.find_by_css('img.fancybox-image')
    featured_image = relative_image_url["src"]


    # Mars Facts

    # In[67]:


    url3 = "https://galaxyfacts-mars.com"


    # In[68]:


    marsfact_tb = pd.read_html(url3)[1]
    marsfact_tb.rename({0: 'Mars_Features', 1: 'Mars_Facts'}, axis=1, inplace=True)
    


    # In[69]:


    mars_content = marsfact_tb.to_html(index = False)
    #marsfact_str = marsfact_tb.to_string()

    # Mars Hemispheres

# In[70]:


    url3 = "https://marshemispheres.com/"
    browser.visit(url3)
    


# In[71]:


    import time

    links = browser.find_by_css('a.product-item img')
    hemisphere_image_urls2 = []


# Next, loop through those links, click the link, find the sample anchor, return the href
    for i in range(1,5):
        hemisphere2 = {}
        xpathlink = '//*[@id="product-section"]/div[2]/div[' + str(i) +']/a/img'
    
    
    # We have to find the elements on each loop to avoid a stale element exception
        browser.find_by_xpath(xpathlink).click()
        time.sleep(2)
    # Next, we find the Sample image anchor tag and extract the href
        sample_elem2 = browser.find_by_xpath('//*[@id="wide-image"]/div/ul/li[1]/a')
        hemisphere2['img_url'] = sample_elem2['href']
    
    # Get Hemisphere title
        hemisphere2['title'] = browser.find_by_xpath('//*[@id="results"]/div[1]/div/div[3]/h2').text
    
    # Append hemisphere object to list
        hemisphere_image_urls2.append(hemisphere2)
    
    # Finally, we navigate backwards
        browser.back()
        time.sleep(2)


# In[72]:


    hemisphere_image_urls2 

    MARS_DICT = {
        "news_list" : news_list,
        "newsp_list_notag" : newsp_list_notag,
        "featured_image" : featured_image,
        "mars_content" : mars_content,
        "hemisphere_image_urls2 ": hemisphere_image_urls2 
    }
    print(MARS_DICT)
    browser.quit()

    return MARS_DICT

if __name__=="__main__":
    print(scrape())
