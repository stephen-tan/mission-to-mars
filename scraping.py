# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    hemisphere_image_urls = hemisphere(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemisphere(browser),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def hemisphere(browser):
    # Visit URL
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    hemisphere_image_urls = []

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

    parent_url = "https://astrogeology.usgs.gov/"

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
        full_size_img_url = parent_url + image_page_partial_url
        
        # Add the image url to a dictionary    
        hemisphere["img_url"] = full_size_img_url
        
        # Add the dictionary to the list
        hemisphere_image_urls.append(hemisphere)
        
        # Go back to the main page
        browser.back()

    return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())