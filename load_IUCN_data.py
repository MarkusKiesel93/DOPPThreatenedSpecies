import pandas as pd
from pathlib import Path


def load_data():
    DATA_PATH = Path('./data/IUCN/scraped/')
    file_paths = DATA_PATH.glob('*.csv')

    all_countries = []
    for file_path in file_paths:
        df = pd.read_csv(file_path)
        country_name = file_path.stem.replace('_', ' ').split(',')[0]
        df['country'] = country_name
        df = df.rename(columns={'kingdom_class': 'kingdom'})
        df['kingdom'] = df.apply(lambda row: row['kingdom'].split()[-1], axis=1)
        all_countries.append(df)

    data = pd.concat(all_countries)
    return data


if __name__ == '__main__':
    data = load_data()
    print('SHAPE:')
    print(data.shape)
    print('HEAD:')
    print(data.head())
    print('TAIL:')
    print(data.tail())
