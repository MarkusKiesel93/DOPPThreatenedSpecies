from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from pathlib import Path
from time import sleep
import pandas as pd
from countries import get_for_IUCN


def run_scraping(region_name, country_iucn, country_name, output_path):
    print(f'scraping data for region: {country_name} in {region_name}')

    DRIVER = Path('./geckodriver').absolute()
    URL = 'https://www.iucnredlist.org/search/list'
    COUNTRY_LEGEND_FILTERS = ['Extant (resident)',
                              'Extant & Reintroduced',
                              'Extinct',
                              'Extinct & Reintroduced',
                              'Possibly Extinct',
                              'Possibly Extinct & Reintroduced']

    # connect to browser with selenium
    driver = webdriver.Firefox(executable_path=DRIVER)
    driver.get(URL)
    # get filters
    filters = driver.find_element_by_class_name('filter')
    # filter only animals
    filter_animals(filters)
    # filter for country legends
    filter_country_legends(filters, COUNTRY_LEGEND_FILTERS)

    # select region
    open_land_regions_section(filters)
    open_region_section(driver, filters, region_name)

    # sect coutnry
    click_country_filter(filters, country_iucn)

    # extract data
    load_whole_content(driver)
    content = extract_content(driver)

    file_path = (output_path / country_name).with_suffix('.csv')
    content.to_csv(file_path, index=False)
    
    # close browser
    driver.close()


# filter for Taxonomy group Animalia
def filter_animals(filters):
    filter_taxonomy = filters.find_element_by_xpath("//*[text()='Taxonomy']")
    filter_taxonomy.click()  # click section
    sleep(2)
    filter_animals = filters.find_element_by_xpath("//*[text()='Animalia']")
    filter_animals.click()  # click animals section
    filter_taxonomy.click()  # collapse filter


# filter country legends
def filter_country_legends(filters, filter_items):
    filter_country_legends = filters.find_element_by_xpath("//*[text()='Country Legends']")
    filter_country_legends.click()  # click section
    sleep(2)
    for item in filter_items:
        element = filters.find_element_by_xpath(f"//*[text()='{item}']")
        element.click()   # click items in list
    filter_country_legends.click()  # collapse filter


# open filter section for land regions
def open_land_regions_section(filters):
    land_region = filters.find_element_by_xpath("//*[text()='Land Regions']")
    land_region.click()
    sleep(2)


def open_region_section(driver, filters, region_name):
    filter_region = filters.find_element_by_xpath(f"//*[text()='{region_name}']")
    # offset is needed to click the arrow on the right instead of the checkbox
    x_offset = 150
    ac = ActionChains(driver)
    ac.move_to_element(filter_region).move_by_offset(x_offset, 0).click().perform()
    sleep(2)


# click filter for a country
def click_country_filter(filters, country_name):
    filter_country = filters.find_element_by_xpath(f"//*[text()='{country_name}']")
    filter_country.click()
    sleep(2)


# clickst the "show all" button on the bottom of the main content as long as all species are loaded
def load_whole_content(driver):
    try:
        wait_loading(driver)
        main_content = driver.find_element_by_class_name('layout-page__major')
        show_all_button = main_content.find_element_by_class_name('section__link-out')
        show_all_button.click()
        load_whole_content(driver)  # recursive call
    # exceiption if "show all button is not found"
    except Exception:
        sleep(1)


def wait_loading(driver):
    try:
        driver.find_element_by_class_name('spinner')
        sleep(1)
        wait_loading(driver)
    except Exception:
        sleep(1)


# extract species info from html li items
def extract_content(driver):
    results = []

    # get main html content
    main_content = driver.find_element_by_class_name('layout-page__major')
    main_html = main_content.get_attribute('innerHTML')

    # get html with beautifulsoup
    soup = BeautifulSoup(main_html, 'html.parser')
    items = soup.find_all('li', class_='list-results__item')
    for item in items:
        result = {}
        result['kingdom_class'] = item.contents[0].string
        result['common_name'] = item.contents[1].text
        result['scientific_name'] = item.contents[2].text
        result['trend'] = item.contents[3].text
        result['region'] = item.contents[4].text
        result['threat_level'] = item.contents[5].get('title')
        results.append(result)
    return pd.DataFrame(results)


if __name__ == '__main__':
    OUTPUT_PATH = Path('./data/IUCN/scraped')
    # iterate all regions
    OECD_REGION_COUNTY_LIST = get_for_IUCN()
    for country_dict in OECD_REGION_COUNTY_LIST:
        run_scraping(country_dict['region_name'],
                     country_dict['country_iucn'],
                     country_dict['country_name'],
                     OUTPUT_PATH)
