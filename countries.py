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
    dict = cfg['countries']
    name_transformations = cfg['IUCN_name_transform']

    for region_name in dict:
        for country_name in dict[region_name]:
            if country_name in list(name_transformations.keys()):
                dict[region_name].remove(country_name)
                dict[region_name].append(name_transformations[country_name])

    return dict


def rename_country_from_IUCN(country_name):
    name_transformations = cfg['IUCN_name_transform']
    if country_name in list(name_transformations.values()):
        key_list = list(name_transformations.keys())
        val_list = list(name_transformations.values())
        new_name = key_list[val_list.index(country_name)]
        return new_name
    return country_name


if __name__ == '__main__': 
    print('list of all countries:')
    print(get_country_list())

    print('dictionary of regions and countries')
    print(get_for_IUCN())

    print(rename_IUCN('Czechia'))
