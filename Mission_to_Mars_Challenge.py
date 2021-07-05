#!/usr/bin/env python
# coding: utf-8


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# ### Visit the NASA Mars News Site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# ### JPL Space Images Featured Image
# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup

# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# ### Mars Facts
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()

df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df

df.to_html()

# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
# Parse the html with soup
html = browser.html
home_page_soup = soup(html, 'html.parser')

# Inspecting the webpage shows that each image title is within the collapsible results class
results = home_page_soup.find_all("div", class_="item")

# Calculate how many images there are on the main page
num_hemispheres = len(home_page_soup.find_all("img", class_="thumb"))

# Create empty lists to store the data
hemi_titles = []
hemi_hyperlinks = []
jpg_images = []

base_url = "https://astrogeology.usgs.gov/"

# Find the image link and title based off of how many hemispheres there are on the website
for result in results:
    
    # Create a dictionary to hold values
    hemisphere = {}
    
    # Get the title tag from <h3 />
    image_title = result.find("h3").text.strip()
    
    # Add the title to a dictionary
    hemisphere["title"] = image_title
    
    # Get the relative link from the thumbnail <a />
    main_page_image_partial_url = result.find("a")["href"]
    
    # Create a hyperlink with the full url
    hyperlink = parent_url + main_page_image_partial_url
    
    # Visit the new page
    browser.visit(hyperlink)
    html = browser.html
    image_soup = soup(html, 'html.parser')
    
    # Scrape the new webpage
    results = image_soup.find_all("img", class_="wide-image")
    
    # Get the full size source image link
    image_page_partial_url = results[0]["src"]
    full_size_img_url = base_url + image_page_partial_url
    
    # Add the image url to a dictionary    
    hemisphere["img_url"] = full_size_img_url
    
    # Add the dictionary to the list
    hemisphere_image_urls.append(hemisphere)

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()

