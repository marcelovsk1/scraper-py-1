import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def scroll_to_bottom(driver, max_clicks=3):
    for _ in range(max_clicks):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

def scrape_facebook_events(driver):
    scroll_to_bottom(driver)

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

    return event_list

def scrape_ticketmaster_events(driver):
    scroll_to_bottom(driver)

    page_content = driver.page_source
    webpage = BeautifulSoup(page_content, 'html.parser')

    events = webpage.find_all('div', class_='Flex-sc-145abwg-0 bWTqsV accordion__item event-listing__item')

    event_list = []

    for event in events:
        event_name = event.find('div', class_='sc-fFeiMQ bCvzDL text text--dark text--primary sc-6jnhqk-0 kGOLzf event-tile__title').text
        event_date = event.find('div', class_='sc-fFeiMQ dBYlim text text--accent text--accent01 text-tm sc-17ev1tv-0 cnj20n-0 firocR iZsGLV event-tile__date-title').text.strip()
        event_location = event.find('div', class_='sc-fFeiMQ iIgzpz text text--dark text--secondary sc-1s3i3gy-0 hbRPym event-tile__sub-title').text.strip()
        event_image = event.find('img', class_='event-listing__thumbnail')

        image_url = event_image['src'] if event_image else None

        event_info = {
            'Event': event_name,
            'Date': event_date,
            'Location': event_location,
            'Image URL': image_url
        }

        event_list.append(event_info)

    return event_list

def scrape_eventbrite_events(driver):
    scroll_to_bottom(driver)

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

    return event_list

def main():
    # Facebook
    facebook_url = 'https://www.facebook.com/events/explore/montreal-quebec/102184499823699/'
    facebook_options = Options()
    facebook_options.headless = True
    facebook_driver = webdriver.Chrome(options=facebook_options)
    facebook_driver.get(facebook_url)
    facebook_driver.implicitly_wait(10)
    facebook_events = scrape_facebook_events(facebook_driver)
    facebook_driver.quit()

    # Ticketmaster
    ticketmaster_url = 'https://www.ticketmaster.ca/discover/concerts/montreal'
    ticketmaster_options = Options()
    ticketmaster_options.headless = True
    ticketmaster_driver = webdriver.Chrome(options=ticketmaster_options)
    ticketmaster_driver.get(ticketmaster_url)
    ticketmaster_driver.implicitly_wait(10)
    ticketmaster_events = scrape_ticketmaster_events(ticketmaster_driver)
    ticketmaster_driver.quit()

    # Eventbrite
    eventbrite_url = 'https://www.eventbrite.com/d/canada--montreal/events/'
    eventbrite_options = Options()
    eventbrite_options.headless = True
    eventbrite_driver = webdriver.Chrome(options=eventbrite_options)
    eventbrite_driver.get(eventbrite_url)
    eventbrite_driver.implicitly_wait(10)
    eventbrite_events = scrape_eventbrite_events(eventbrite_driver)
    eventbrite_driver.quit()

    all_events = facebook_events + ticketmaster_events + eventbrite_events

    # Convert to JSON
    json_data = json.dumps(all_events, indent=2)

    #with open('events_data.json', 'w') as file:
        #file.write(json_data)

    print(json_data)

if __name__ == "__main__":
    main()
