# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
# from bs4 import BeautifulSoup
# import time

# url = 'https://www.ticketmaster.ca/discover/concerts/montreal'

# options = Options()
# options.headless = True

# driver = webdriver.Chrome(options=options)
# driver.get(url)
# driver.implicitly_wait(10)

# # Load More Func
# from selenium.webdriver.common.keys import Keys

# click_count = 0
# max_clicks = 5

# def click_load_more():
#     global click_count
#     while click_count < max_clicks:
#         try:
#             load_more_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Load More')]")
#             ActionChains(driver).move_to_element(load_more_button).perform()
#             load_more_button.click()
#             time.sleep(3)  # Aguarde tempo suficiente para o carregamento da página
#             click_count += 1
#         except Exception as e:
#             print(f"Não foi possível encontrar ou clicar no botão Load More: {e}")
#             break

# click_load_more()

# # EVENT DATA
# page_content = driver.page_source
# webpage = BeautifulSoup(page_content, 'html.parser')

# events = webpage.find_all('div', class_='Flex-sc-145abwg-0 bWTqsV accordion__item event-listing__item')

# for event in events:
#     event_name = event.find('div', class_='sc-fFeiMQ bCvzDL text text--dark text--primary sc-6jnhqk-0 kGOLzf event-tile__title').text
#     event_date = event.find('div', class_='sc-fFeiMQ dBYlim text text--accent text--accent01 text-tm sc-17ev1tv-0 cnj20n-0 firocR iZsGLV event-tile__date-title').text.strip()
#     event_location = event.find('div', class_='sc-fFeiMQ iIgzpz text text--dark text--secondary sc-1s3i3gy-0 hbRPym event-tile__sub-title').text.strip()
#     event_image = event.find('img', class_='event-listing__thumbnail')

#     image_url = event_image['src'] if event_image else None

#     print(f"Event: {event_name}")
#     print(f"Date: {event_date}")
#     print(f"Location: {event_location}")
#     print(f"Image URL: {image_url}")
#     print("=" * 100)

# driver.quit()


#JSON

import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time

url = 'https://www.ticketmaster.ca/discover/concerts/montreal'

options = Options()
options.headless = True

driver = webdriver.Chrome(options=options)
driver.get(url)
driver.implicitly_wait(10)

# Load More Func
click_count = 0
max_clicks = 5

def click_load_more():
    global click_count
    while click_count < max_clicks:
        try:
            load_more_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Load More')]")
            ActionChains(driver).move_to_element(load_more_button).perform()
            load_more_button.click()
            time.sleep(3)
            click_count += 1
        except Exception as e:
            print(f"Unable to find or click the 'Load More' button: {e}")
            break

click_load_more()

# List to store event information
event_list = []

# EVENT DATA
page_content = driver.page_source
webpage = BeautifulSoup(page_content, 'html.parser')

events = webpage.find_all('div', class_='Flex-sc-145abwg-0 bWTqsV accordion__item event-listing__item')

for event in events:
    event_name = event.find('div', class_='sc-fFeiMQ bCvzDL text text--dark text--primary sc-6jnhqk-0 kGOLzf event-tile__title').text
    event_date = event.find('div', class_='sc-fFeiMQ dBYlim text text--accent text--accent01 text-tm sc-17ev1tv-0 cnj20n-0 firocR iZsGLV event-tile__date-title').text.strip()
    event_location = event.find('div', class_='sc-fFeiMQ iIgzpz text text--dark text--secondary sc-1s3i3gy-0 hbRPym event-tile__sub-title').text.strip()
    event_image = event.find('img', class_='event-listing__thumbnail')

    image_url = event_image['src'] if event_image else None

    # Create a dictionary for the event and append it to the list
    event_info = {
        'Event': event_name,
        'Date': event_date,
        'Location': event_location,
        'Image URL': image_url
    }
    event_list.append(event_info)

# Convert the list of dictionaries to a JSON-formatted string
json_data = json.dumps(event_list, indent=2)

# Print or save the JSON data as needed
print(json_data)

driver.quit()
