from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.options import Options
import re

chrome_options = Options()
chrome_options.add_experimental_option('prefs', {'profile.managed_default_content_settings.javascript': 2})
driver = webdriver.Chrome('chromedriver', options=chrome_options)
url = 'https://bazar.bg/obiavi/gradski-velosipedi/varna?condition=2'
css_selector = '.awrapper .listItemContainer .listItemLink'
driver.get(url)
driver.implicitly_wait(1)
count_pages = 5
data = []
for page in range(count_pages):
    items = driver.find_elements_by_css_selector(css_selector)
    i = 0
    for item in items:
        i += 1
        title = item.find_element_by_css_selector('span.title').text
        price = item.find_element_by_css_selector('span.price').text
        price = re.sub('[^0-9]', '', price)
        if not len(price):
            price = 0
        price = int(price)
        image = item.find_element_by_css_selector('img.cover').get_attribute('src')
        if title and price:
            data.append([title, price, image])
    try:
        link = driver.find_element_by_css_selector('.paging a.next')
        link.click()
    except:
        break

driver.quit()

df = pd.DataFrame(data, columns=['title', 'price', 'image'])
df.sort_values(by='price', inplace=True)
df.to_excel('bikes-selenium.xlsx')
df.head()
