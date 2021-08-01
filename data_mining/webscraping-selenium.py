from selenium import webdriver

url = 'https://bazar.bg/obiavi/gradski-velosipedi/varna?condition=2'
driver = webdriver.Chrome()
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

#driver.quit()
