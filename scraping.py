# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    news_title, news_paragraph = mars_news(executable_path)
    # Run other two scraping functions, and store all results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(executable_path),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }
    return data


# I got weird "stale" something, "not attached to document" errors running this
# then commented everything out, uncommented one line at a time,
# and now no errors. mega-confusels.
def hemis_test_wrap():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    print("i really made a path")
    print( hemis(executable_path) )


# # Get 4 pretty pictures, or at least urls to them
# returns list of dicts, all have keys 'img_url", 'title'
def hemis(exepath):
    # start browser
    browser = Browser('chrome', **exepath, headless=False)
    print("i made a browser")
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    print("i visited top url")
    clic_pic = 'a[class="itemLink product-item"]'
    link_objects = browser.find_by_css(clic_pic)
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []
    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    for i in range(4):
        print("going to", link_objects[2*i+1]['href'])
        link_objects[2*i+1].click()
        img_url = browser.find_by_text('Sample')['href']
        title = browser.find_by_tag('h2').text
        #  print("going back")
        browser.back()
        hemisphere_image_urls.append({'img_url': img_url, 'title': title})
    browser.quit()
    return hemisphere_image_urls


# Get the most recent news bit from one webpage, using splinter and soup
# output: news_title and news_p strings.
def mars_news(exepath):
    # start browser
    browser = Browser('chrome', **exepath, headless=True)
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page, checking whether tag exists
    # beyond delay, i don't think we need the next line for the scrape
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    # real scrape
    html = browser.html
    news_soup = soup(html, 'html.parser')
     # Add try/except for error handling
    try:   
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    # quit and restart browser between webpages, because i get crashes otherwise
    browser.quit()
    return news_title, news_p


# Get Featured Image from second website, , using splinter and soup again.
# output: img_url string
def featured_image(exepath):
    browser = Browser('chrome', **exepath, headless=True)
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None 
    # Use the base URL to create an absolute URL
    # f'{url}/{img_url_rel}'    should also work
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    browser.quit()
    return img_url


#  Get a table from third website with pandas.
# output: string containing html table
def mars_facts():
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    return df.to_html()

# if __name__ == "__main__":
#     # If running as script, print scraped data
#     print(scrape_all())



