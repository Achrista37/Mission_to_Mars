#Load dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import os
import re
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt

#create the main function to execute subsequent functions

def scrape():
    #set up headless driver for deployment
    
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    latest_news_t, latest_news_p = mars_news(browser)
    
#connects main function to the subsequent functions and help them render

    MARS_DICT = {
        "latest_news_t" : latest_news_t,
        "latest_news_p" : latest_news_p,
        "featured_image" : featured_image(browser),
        "mars_table" : mars_table(),
        "mars_img_dict": mars_img_dict(browser) 
    }
    browser.quit()
    return MARS_DICT

#child function scraping mars news
def mars_news(browser):

    ####NASA MARS NEWS\

    #Convert to a beautiful soup object
    url = "https://redplanetscience.com/"

    #make splinter visit the first URL
    browser.visit(url)
    html = browser.html
    mars_soup = bs(html, 'html.parser')
    #try except and obtain the latest news title and paragraph by their X Code
    try:
        latest_news_t= browser.find_by_xpath('//*[@id="news"]/div[1]/div/div[2]/div/div[2]').text
        latest_news_p = browser.find_by_xpath('//*[@id="news"]/div[1]/div/div[2]/div/div[3]').text
    except AttributeError:
        return None, None
    return latest_news_t, latest_news_p 

#child function scraping the featured image from the second URL
def featured_image(browser):
    url2 = "https://spaceimages-mars.com"
    browser.visit(url2)
    html2 = browser.html

#create beautiful soup object and utilize html parser for this
    marsimg_soup = bs(html2, 'html.parser')
    #wrap the code with try-except
    try :
    #find image by CSS and get the source link
        browser.find_by_tag('button')[1].click()
        relative_image_url = browser.find_by_css('img.fancybox-image')
        featured_image = relative_image_url["src"]
    except AttributeError:
        return None
    return featured_image

#sub function to scrape table with Pandas

def mars_table(): 
    url3 = "https://galaxyfacts-mars.com"
    try:
        marsfact_tb = pd.read_html(url3)[0]
    except BaseException:
        return None
    marsfact_tb.rename({0: 'Features', 1: 'Mars', 2:'Earth'}, axis=1, inplace=True)
    #get Pandas to convert the scraped table into html 
    marsfact_content = marsfact_tb.to_html(classes='table table-striped text-center', justify='center', index=False)
    return marsfact_content

#sub function to scrape images of various mars hemispheres and their names

def mars_img_dict(browser):
    import time
    url4 = "https://marshemispheres.com/"
    browser.visit(url4)
    links = browser.find_by_css('a.product-item img')
    #wrap in try-except
    try:
    #set the list to store urls and titles
        hemisphere_image_urls2 = []
        # Looping through links
        for i in range(1,5):
            hemisphere2 = {}
        #get by xpath the initial link directing us to the sub-page
            xpathlink = '//*[@id="product-section"]/div[2]/div[' + str(i) +']/a/img'
        # Click the link
            browser.find_by_xpath(xpathlink).click()
            time.sleep(2)
    # get href by xpath and store in dictionary
            sample_elem2 = browser.find_by_xpath('//*[@id="wide-image"]/div/ul/li[1]/a')
            hemisphere2['img_url'] = sample_elem2['href']
    
    # Hemisphere title
            hemisphere2['title'] = browser.find_by_xpath('//*[@id="results"]/div[1]/div/div[3]/h2').text
    
    # Append hemisphere object to list
            hemisphere_image_urls2.append(hemisphere2)
    
    # Navigating backwards to the main page
            browser.back()
            time.sleep(2)
    except AttributeError:
        return None
    return hemisphere_image_urls2 
if __name__=="__main__":
    print(scrape_all())

    