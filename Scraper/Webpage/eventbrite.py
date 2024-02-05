# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from bs4 import BeautifulSoup

# url = 'https://www.eventbrite.com/d/canada--montreal/events/'

# options = Options()
# options.headless = True

# driver = webdriver.Chrome(options=options)
# driver.get(url)
# driver.implicitly_wait(10)

# page_content = driver.page_source
# webpage = BeautifulSoup(page_content, 'html.parser')

# events = webpage.find_all('div', class_='Stack_root__1ksk7')

# for event in events:
#     event_name = event.find('h2').text if event.find('h2') else None
#     event_date = event.find('p').text.strip() if event.find('p') else None
#     event_location_element = event.find('p', class_='Typography_root__487rx #585163 Typography_body-md__487rx event-card__clamp-line--one Typography_align-match-parent__487rx')
#     event_location = event_location_element.text.strip() if event_location_element else None
#     event_image = event.find('a', class_='event-card-link')
#     image_url = event_image['href'] if event_image else None

#     print(f"{event_name}")
#     print(f"{event_date}")
#     print(f"{event_location}")
#     print(f"Image URL: {image_url}")

# driver.quit()

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json

url = 'https://www.eventbrite.com/d/canada--montreal/events/'

options = Options()
options.headless = True

driver = webdriver.Chrome(options=options)
driver.get(url)
driver.implicitly_wait(10)

page_content = driver.page_source
webpage = BeautifulSoup(page_content, 'html.parser')

events = webpage.find_all('div', class_='Stack_root__1ksk7')

event_list = []

for event in events:
    event_name = event.find('h2').text if event.find('h2') else None
    event_date = event.find('p').text.strip() if event.find('p') else None
    event_location_element = event.find('p', class_='Typography_root__487rx #585163 Typography_body-md__487rx event-card__clamp-line--one Typography_align-match-parent__487rx')
    event_location = event_location_element.text.strip() if event_location_element else None
    event_image = event.find('a', class_='event-card-link')
    image_url = event_image['href'] if event_image else None

    event_data = {
        'Event': event_name,
        'Date': event_date,
        'Location': event_location,
        'image_url': image_url
    }

    event_list.append(event_data)

driver.quit()

json_data = json.dumps(event_list, indent=2)

print(json_data)
