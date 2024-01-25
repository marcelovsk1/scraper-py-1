import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

url = 'https://www.facebook.com/events/explore/montreal-quebec/102184499823699/'

options = Options()
options.headless = True

driver = webdriver.Chrome(options=options)
driver.get(url)
driver.implicitly_wait(10)

time.sleep(5)

# Scroll Func
def scroll_to_bottom():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

for _ in range(3):
    scroll_to_bottom()


page_content = driver.page_source
webpage = BeautifulSoup(page_content, 'html.parser')

events = webpage.find_all('div', class_='x78zum5 x1n2onr6 xh8yej3')

event_list = []

for event in events:
    event_name_elem = event.find('span', class_='x4k7w5x x1h91t0o x1h9r5lt x1jfb8zj xv2umb2 x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k xedcshv x1lytzrv x1t2pt76 x7ja8zs x1qrby5j')
    event_name = event_name_elem.text if event_name_elem else None

    event_date_elem = event.find('div', class_='xu06os2 x1ok221b')
    event_date = event_date_elem.text.strip() if event_date_elem else None

    event_location_elem = event.find('span', class_='x4k7w5x x1h91t0o x1h9r5lt x1jfb8zj xv2umb2 x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k xedcshv x1lytzrv x1t2pt76 x7ja8zs x1qrby5j')
    event_location = event_location_elem.text.strip() if event_location_elem else None

    event_image = event.find('img', class_='x1rg5ohu x5yr21d xl1xv1r xh8yej3')
    image_url = event_image['src'] if event_image and 'src' in event_image.attrs else None

    event_info = {
        'Event': event_name,
        'Date': event_date,
        'Location': event_location,
        'image_url': image_url
    }

    event_list.append(event_info)

driver.quit()

# Convert the list of dictionaries to a JSON string
json_data = json.dumps(event_list, indent=2)

print(json_data)
