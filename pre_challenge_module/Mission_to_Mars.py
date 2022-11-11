# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd

from time import sleep

# Set up chrome driver, once.
executable_path = {'executable_path': ChromeDriverManager().install()}


#       Get the most recent news bit from one webpage, using splinter and soup
#       Key output: news_title and news_p strings.

# start browser
browser = Browser('chrome', **executable_path, headless=False)
# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page, checking whether tag exists
# beyond delay, i don't think we need the next line for the scrape
browser.is_element_present_by_css('div.list_text', wait_time=100)

# the wait above doesn't seem to work, let's try mimiths
sleep(50)

# real scrape
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
# news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
# news_p

# quit and restart browser between webpages, because i get crashes otherwise
browser.quit()


#       Get Featured Image from second website, , using splinter and soup again.
#       Key output: img_url string

browser = Browser('chrome', **executable_path, headless=False)
# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
# img_url_rel

# Use the base URL to create an absolute URL
# f'{url}/{img_url_rel}'    should also work
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
# img_url

browser.quit()


#       Get a table from third website with pandas.
#       Key output: mars_fact_table html string

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
# df
mars_fact_table = df.to_html()
# mars_fact_table

print(news_title)
print(news_p)
print( img_url)
# print(mars_fact_table)




