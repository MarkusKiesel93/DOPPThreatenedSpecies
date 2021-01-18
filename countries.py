import yaml
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / 'countries.yml'


with open(CONFIG_PATH, 'r') as cfg_file:
    cfg = yaml.safe_load(cfg_file)


def get_country_list():
    countries = []
    for region in cfg['countries']:
        countries += cfg['countries'][region]
    return countries


def get_for_IUCN():
    region_country_list = []

    for region_name in cfg['countries']:
        for country_name in cfg['countries'][region_name]:
            country_dict = {}
            country_dict['region_name'] = region_name
            country_dict['country_name'] = country_name
            if country_name in list(cfg['IUCN_name_transform'].keys()):
                country_dict['country_iucn'] = cfg['IUCN_name_transform'][country_name]
            else:
                country_dict['country_iucn'] = country_name
            region_country_list.append(country_dict)

    return region_country_list


if __name__ == '__main__':
    print('list of all countries:')
    country_list = get_country_list()
    print(country_list)
    assert len(country_list) == 65

    print('dictionary of regions and countries')
    countries_iucn = get_for_IUCN()
    print(countries_iucn)
    assert len(country_list) == len(countries_iucn)
