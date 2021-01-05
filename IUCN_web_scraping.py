from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from pathlib import Path
from time import sleep
import pandas as pd


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
    x_offset = 100
    ac = ActionChains(driver)
    ac.move_to_element(filter_region).move_by_offset(x_offset, 0).click().perform()
    sleep(2)


# click filter for a country
def click_country_filter(filters, country_name):
    filter_country = filters.find_element_by_xpath(f"//*[text()='{country_name}']")
    filter_country.click()
    sleep(2)


# click the "Land Regions" button to return to all filters
def click_return_regions(filters):
    # select second element with name "Land Regions"
    filter_region = filters.find_elements_by_xpath("//*[text()='Land Regions']")[1]
    filter_region.click()
    sleep(2)


# clickst the "show all" button on the bottom of the main content as long as all species are loaded
def load_whole_content(driver):
    main_content = driver.find_element_by_class_name('layout-page__major')
    try:
        show_all_button = main_content.find_element_by_class_name('section__link-out')
        show_all_button.click()
        sleep(10)  # todo: find better method to wait for loaded content
        load_whole_content(driver)  # recursive call
    # exceiption if "show all button is not found"
    except Exception:
        sleep(10)  # todo: find better method to wait for loaded content


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
    DRIVER = Path('./geckodriver').absolute()
    URL = 'https://www.iucnredlist.org/search/list'
    OUTPUT_PATH = Path('./data/IUCN/scraped')
    COUNTRY_LEGEND_FILTERS = ['Extant & Reintroduced',
                              'Extinct',
                              'Extinct & Reintroduced',
                              'Possibly Extinct',
                              'Possibly Extinct & Reintroduced']
    OECD_COUNTRIES = {
        'Europe': [
            'Austria', 'Belgium', 'Czechia', 'Denmark', 'Finland', 'France', 'Germany', 'Greece', 'Hungary',
            'Iceland', 'Ireland', 'Italy', 'Luxembourg', 'Netherlands', 'Norway', 'Poland', 'Portugal', 'Slovakia',
            'Spain', 'Sweden', 'Switzerland', 'United Kingdom'
        ],
        'Oceania': [
            'Australia', 'New Zealand',
        ],
        'North America': [
            'Canada', 'United States',
        ],
        'East Asia': [
            'Japan', 'Korea, Republic of',
        ],
        'Mesoamerica': [
            'Mexico',
        ],
    }

    # connect to browser with selenium
    driver = webdriver.Firefox(executable_path=DRIVER)
    driver.get(URL)
    # get filters
    filters = driver.find_element_by_class_name('filter')
    # filter only animals
    filter_animals(filters)
    # filter for country legends
    filter_country_legends(filters, COUNTRY_LEGEND_FILTERS)

    # go over all needed regions
    open_land_regions_section(filters)
    # iterate all regions
    for region_name in OECD_COUNTRIES:
        print(f'region: {region_name}')
        open_region_section(driver, filters, region_name)

        # iterate all countries
        for country_name in OECD_COUNTRIES[region_name]:
            print(f'loading data for country: {country_name}')
            click_country_filter(filters, country_name)

            load_whole_content(driver)

            content = extract_content(driver)

            file_path = (OUTPUT_PATH / country_name.replace(' ', '_')).with_suffix('.csv')
            content.to_csv(file_path, index=False)

            click_country_filter(filters, country_name)

        click_return_regions(filters)
