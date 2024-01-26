import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def scroll_to_bottom(driver, max_clicks=3):
    for _ in range(max_clicks):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

def scrape_events(driver, url, selectors):
    driver.get(url)
    driver.implicitly_wait(30)
    scroll_to_bottom(driver)

    page_content = driver.page_source
    webpage = BeautifulSoup(page_content, 'html.parser')

    events = webpage.find_all(selectors['event']['tag'], class_=selectors['event'].get('class'))
    event_list = []

    for event in events:
        event_info = {}
        for key, selector in selectors.items():
            if key != 'event':
                element = event.find(selector['tag'], class_=selector.get('class'))
                event_info[key] = element.text.strip() if element else None
                if key == 'Image URL':
                    event_info[key] = element['src'] if element and 'src' in element.attrs else None

        event_list.append(event_info)

    return event_list

def main():
    sources = [
        {
            'name': 'Facebook',
            "loadingTime": 10,
            'url': 'https://www.facebook.com/events/explore/montreal-quebec/102184499823699/',
            'selectors': {
                'event': {'tag': 'div', 'class': 'x78zum5 x1n2onr6 xh8yej3'},
                'Event': {'tag': 'span', 'class': 'x4k7w5x x1h91t0o x1h9r5lt x1jfb8zj xv2umb2 x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k xedcshv x1lytzrv x1t2pt76 x7ja8zs x1qrby5j'},
                'Date': {'tag': 'div', 'class': 'xu06os2 x1ok221b'},
                'Location': {'tag': 'span', 'class': 'x4k7w5x x1h91t0o x1h9r5lt x1jfb8zj xv2umb2 x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k xedcshv x1lytzrv x1t2pt76 x7ja8zs x1qrby5j'},
                'Image URL': {'tag': 'img', 'class': 'x1rg5ohu x5yr21d xl1xv1r xh8yej3'}
            }
        },
        {
            'name': 'Ticketmaster',
            'url': 'https://www.ticketmaster.ca/discover/concerts/montreal',
            'selectors': {
                'event': {'tag': 'div', 'class': 'Flex-sc-145abwg-0 bWTqsV accordion__item event-listing__item'},
                'Event': {'tag': 'div', 'class': 'sc-fFeiMQ bCvzDL text text--dark text--primary sc-6jnhqk-0 kGOLzf event-tile__title'},
                'Date': {'tag': 'div', 'class': 'sc-fFeiMQ dBYlim text text--accent text--accent01 text-tm sc-17ev1tv-0 cnj20n-0 firocR iZsGLV event-tile__date-title'},
                'Location': {'tag': 'div', 'class': 'sc-fFeiMQ iIgzpz text text--dark text--secondary sc-1s3i3gy-0 hbRPym event-tile__sub-title'},
                'Image URL': {'tag': 'img', 'class': 'event-listing__thumbnail'}
            }
        },
        {
            'name': 'Eventbrite',
            'url': 'https://www.eventbrite.com/d/canada--montreal/events/',
            'selectors': {
                'event': {'tag': 'div', 'class': 'Stack_root__1ksk7'},
                'Event': {'tag': 'h2', 'class': 'Typography_root__487rx #3a3247 Typography_body-lg__487rx event-card__clamp-line--two Typography_align-match-parent__487rx'},
                'Date': {'tag': 'p', 'class': 'Typography_root__487rx #3a3247 Typography_body-md-bold__487rx Typography_align-match-parent__487rx'},
                'Location': {'tag': 'p', 'class': 'Typography_root__487rx #585163 Typography_body-md__487rx event-card__clamp-line--one Typography_align-match-parent__487rx'},
                'Image URL': {'tag': 'img', 'class': 'event-card-image'}
            }
        }
    ]

    all_events = []

    for source in sources:
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        events = scrape_events(driver, source['url'], source['selectors'])
        driver.quit()

        source_data = {
            'source_name': source['name'],
            'events': events
        }

        all_events.append(source_data)

    json_data = json.dumps(all_events, indent=2)
    print(json_data)

if __name__ == "__main__":
    main()
