# Import Dependencies
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt

def scrape():
    
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser)
    hemisphere_image_urls = mars_hemis(browser)

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image_url": featured_image(browser),
        "mars_facts": mars_facts(),
        "hemispheres": hemisphere_image_urls,
        "last_modified": dt.datetime.now()
    }
    browser.quit()
    return data


def mars_news(browser):
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html = browser.html
    news_soup = bs(html, 'html.parser')

    try:
        site_elem = news_soup.select_one('div.list_text')
        news_title = site_elem.find("div", class_='content_title').get_text()
        news_p = site_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    full_image_btn = browser.find_by_tag('button')[1]
    full_image_btn.click()

    html = browser.html
    mars_img_soup = bs(html, 'html.parser')

    try:
        mars_img_rel_url = mars_img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    featured_image_url = f'https://spaceimages-mars.com/{mars_img_rel_url}'
    return featured_image_url

def mars_facts():
    try:
        mars_facts_df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    mars_facts_df.columns=['Description', 'Mars', 'Earth']
    mars_facts_df.set_index('Description', inplace=True)

    return mars_facts_df.to_html()


def mars_hemis(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    hemisphere_image_urls = []

    for hemi in range(4): 
        browser.links.find_by_partial_text('Hemisphere')[hemi].click()  
    
        html = browser.html
        hemisphere_soup = bs(html, 'html.parser')
    
        title = hemisphere_soup.find('h2', class_='title').text
        img_url = hemisphere_soup.find('li').a.get('href')
    
        hemispheres = {}
        hemispheres['img_url'] = f'https://marshemispheres.com/{img_url}'
        hemispheres['title'] = title
        hemisphere_image_urls.append(hemispheres)
        browser.back()
    return hemisphere_image_urls

if __name__=="__main__":
    print(scrape())
