from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import time
import pandas as pd

def init_browser():
    executable_path = {"executable_path":"chromedriver.exe"}
    return Browser('chrome', **executable_path, headless=False)

# ## NASA Mars News
def scrape_info():
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    time.sleep(2)
    response = browser.html
    soup = bs(response, 'html.parser')
    results = soup.find_all('li', class_="slide")
    headers = []
    for result in results:
        try:
            title = result.find('div', class_="content_title").text
            content =  result.find('div', class_="article_teaser_body").text
            head_dict={}
            head_dict["title"] = title
            head_dict["content"] = content
            headers.append(head_dict)
        except:
            pass


    # ## JPL Mars Space Images - Featured Image
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2) 
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')
    time.sleep(2)
    response_jpl = browser.html
    soup = bs(response_jpl, 'html.parser')
    featured_image = soup.find('img', class_="main_image")['src']
    featured_image_url = f'https://www.jpl.nasa.gov{featured_image}'


    # ## Mars Weather
    url3 = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url3)
    time.sleep(5)
    response_twr = browser.html
    soup = bs(response_twr, 'html.parser')
    tweet = soup.find("div", {"data-testid": "tweet"})
    timeline =tweet.find_all("span")
    mars_weather = timeline[4].text


    # ## Mars Facts
    url4= "https://space-facts.com/mars/"
    tables = pd.read_html(url4)
    mars_data = tables[0]
    mars_data.columns=['Data', 'Value']
    mars_table = mars_data.to_html(index=False)


    # ## Mars Hemispheres
    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url5)
    hemisphere_image_urls = []
    hemispheres = ['Cerberus Hemisphere', 'Schiaparelli Hemisphere', 'Syrtis Major Hemisphere', 'Valles Marineris Hemisphere']
    for hemisphere in hemispheres:
        browser.click_link_by_partial_text(hemisphere)
        time.sleep(1)
        response = browser.html
        soup = bs(response, 'html.parser')
        type(soup)
        link = soup.find("div", class_="downloads")
        list_link = link.find_all("a")
        image = list_link[0]['href']
        hemisphere_dict={}
        hemisphere_dict["title"] = hemisphere
        hemisphere_dict["img_url"] = image
        hemisphere_image_urls.append(hemisphere_dict)
        browser.visit(url5)

    all_mars_data = {
    "news_title" : headers[0]["title"],
    "news_content": headers[0]["content"],
    "feat_img": featured_image_url,
    "weather": mars_weather,
    "hem_imgs":hemisphere_image_urls,
    "data": mars_table
    }

    return all_mars_data
