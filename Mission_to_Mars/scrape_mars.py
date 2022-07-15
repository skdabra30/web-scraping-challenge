# Import Dependencies
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from splinter import Browser
from webdriver_manager.firefox import GeckoDriverManager

def scrape():
    
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    # NASA Mars News 
    url = "https://redplanetscience.com/"
    browser.visit(url)
    html=browser.html
    soup = bs(html, "html.parser")
    news_title = soup.body.find("div", class_="content_title").text.strip()
    news_p = soup.body.find("div", class_="article_teaser_body").text.strip()

    # JPL Mars Space Images - Featured Image 

    url = "https://spaceimages-mars.com/"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")
    featured_image = soup.body.find("img", class_="headerimage")["src"]
    featured_image_url = url + featured_image

    # Mars Facts

    url = "https://galaxyfacts-mars.com/"
    mars_facts = pd.read_html(url)
    mars_facts_df = mars_facts[0]
    mars_facts_df.columns = mars_facts_df.iloc[0]
    mars_facts_df = mars_facts_df.drop(mars_facts[0].index[0])
    mars_facts_df = mars_facts_df.set_index("Mars - Earth Comparison")
    mars_facts_html = mars_facts_df.to_html(classes="table table-striped table-dark")

    # Mars Hemispheres 
    base_url = "https://marshemispheres.com/"
    browser.visit(base_url)
    html = browser.html
    soup = bs(html, "html.parser")
    div_list = soup.body.find_all("div", class_="description")
    sites = []

    for div in div_list:
        
        site = div.find("a", class_="product-item")["href"]
        sites.append(site)

    hemisphere_image_urls = []

    for site in sites:
        try:
            url = base_url + site
            browser.visit(url)
            html = browser.html
            soup = bs(html, "html.parser")
            img_url_ending = soup.body.find("img", class_="wide-image")["src"]
            img_url = base_url + img_url_ending
            title = soup.body.find("h2", class_="title").text.strip()[:-9]
            hemisphere_image_urls.append({"title": title, "img_url": img_url})
        except Exception as e:
            print(e)


    browser.quit()


    # Create dictionary

    scraped_data = {
        "NewsTitle": news_title,
        "NewsParagraph": news_p,
        "FeaturedImage": featured_image_url,
        "MarsFactsTable": mars_facts_html, 
        "HemisphereImages": hemisphere_image_urls
    }

    return scraped_data