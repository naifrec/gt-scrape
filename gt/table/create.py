from pathlib import Path

import pandas as pd

from gt.table import mappings, scrape, utils


def create_table(root=None):
    root = root or '.'
    root = Path(root)
    df = pd.read_csv(str(root / 'cars.csv'), index_col=0)

    print('Clean existing fields')
    df = utils.clean_dimensions(df)
    df = utils.clean_displacement(df)
    df = utils.clean_drivetrain(df)
    df = utils.clean_manufacturers(df)
    df = utils.clean_max_power(df)
    df = utils.clean_power_weight_ratio(df)
    df = utils.clean_weight(df)

    print('Add new fields')
    df = utils.add_country_and_continent(df)
    df = utils.add_is_prize_car(df, path=str(root / 'prize_cars.csv'))
    df = utils.add_is_race_modifiable(df)
    df = utils.add_manufacturing_date(df)

    print('Download images for cars')
    df = scrape.scrape_car_images(df)

    print('Remove empty fields')
    df.drop(mappings.COLUMNS_TO_DISCARD, axis=1, inplace=True)

    # save
    filepath = str(root / 'cars-clean.csv')
    df.to_csv(filepath)
    print(f'Saved clean car list to {filepath}')


if __name__ == '__main__':
    import fire

    fire.Fire(create_table)
