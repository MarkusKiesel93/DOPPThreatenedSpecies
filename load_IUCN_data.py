import pandas as pd
from pathlib import Path

from countries import rename_country_from_IUCN


def load_IUCN_data():
    DATA_PATH = Path('./data/IUCN/scraped/')
    file_paths = DATA_PATH.glob('*.csv')

    all_countries = []
    for file_path in file_paths:
        df = pd.read_csv(file_path)
        country_name = file_path.stem.replace('_', ' ').split(',')[0]
        country_name = rename_country_from_IUCN(country_name)
        df['country'] = country_name
        df['kingdom_class'] = df.apply(lambda row: row['kingdom_class'].split()[-1], axis=1)
        df = df.rename(columns={'kingdom_class': 'class'})
        all_countries.append(df)

    data = pd.concat(all_countries)
    return data


if __name__ == '__main__':
    data = load_IUCN_data()
    print('SHAPE:')
    print(data.shape)
    print('HEAD:')
    print(data.head())
    print('TAIL:')
    print(data.tail())
