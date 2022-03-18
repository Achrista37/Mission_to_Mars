#!/usr/bin/env python
# coding: utf-8
def scrape_all():
   # Initiate headless driver for deployment
   browser = Browser("chrome", executable_path="chromedriver", headless=True)
   news_title, news_paragraph = mars_news(browser)
   # Run all scraping functions and store results in a dictionary
   data = {
       "news_title": news_title,
       "news_paragraph": news_paragraph,
       "featured_image": featured_image(browser),
       "facts": mars_facts(),
       "hemispheres": hemispheres(browser),
       "last_modified": dt.datetime.now()
   }
   # Stop webdriver and return data
   browser.quit()
   return data
def mars_news(browser):
   # Scrape Mars News
   # Visit the mars nasa news site
   url = 'https://mars.nasa.gov/news/'
   browser.visit(url)
   # Optional delay for loading the page
   browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
   # Convert the browser html to a soup object and then quit the browser
   html = browser.html
   news_soup = soup(html, 'html.parser')
   # Add try/except for error handling
   try:
       slide_elem = news_soup.select_one("ul.item_list li.slide")
       # Use the parent element to find the first 'a' tag and save it as 'news_title'
       news_title = slide_elem.find("div", class_="content_title").get_text()
       # Use the parent element to find the paragraph text
       news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
   except AttributeError:
       return None, None
   return news_title, news_p (edited) 

if __name__=="__main__":
    print(scrape())
