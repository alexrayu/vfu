from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_experimental_option('prefs', {'profile.managed_default_content_settings.javascript': 2})
driver = webdriver.Chrome('chromedriver', options=chrome_options)
url = 'https://bazar.bg/obiavi/gradski-velosipedi/varna?condition=2'
driver.get(url)
driver.implicitly_wait(1000)
css_selector = '.awrapper .listItemContainer .listItemLink'
items = driver.find_elements_by_css_selector(css_selector)
print(len(items))
i = 0
for item in items:
	i += 1
	title = item.find_element_by_css_selector('span.title').text
	price = item.find_element_by_css_selector('span.price').text
	if title and price:
		print(f'{i}: {title} ({price})')

driver.quit()
