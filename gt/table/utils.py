import numpy as np
import pandas as pd

from gt.table import mappings, regex, scrape


def clean_manufacturers(df):
    # use clean manufacturer names
    df['Manufacturer'] = df['ManufacturerWiki']
    df.drop(columns='ManufacturerWiki', inplace=True)
    return df


def add_country_and_continent(df):
    df['Country'] = df['Manufacturer'].apply(
        lambda manufacturer: mappings.MANUFACTURER2COUNTRY[manufacturer]
    )
    df['Continent'] = df['Country'].apply(
        lambda country: mappings.COUNTRY2CONTINENT[country]
    )
    return df


def add_is_prize_car(df, path):
    # load list from IGN which suffers from bad formatting
    df_prize_car = pd.read_csv(path, index_col=0)
    # instantitate with False
    df['IsPrizeCar'] = False
    # add all cars that can be automatically matched
    prize_cars_not_found = []
    for prize_car in df_prize_car['Name']:
        prize_car = prize_car.lower().strip()
        found = False
        for i, car in enumerate(df['Name']):
            car = car.lower().strip()
            if prize_car in car:
                df.loc[i, 'IsPrizeCar'] = True
                found = True
                break
        if not found:
            prize_cars_not_found.append(prize_car)
    # add manually all cars that could not be matched
    for prize_cars in mappings.IGNNAME2WIKINAME.values():
        if isinstance(prize_cars, list):
            for prize_car in prize_cars:
                for i, car in enumerate(df['Name']):
                    if prize_car == car:
                        df.loc[i, 'IsPrizeCar'] = True
        else:
            for i, car in enumerate(df['Name']):
                if prize_cars == car:
                    df.loc[i, 'IsPrizeCar'] = True
                    break
    return df


def clean_max_power(df):
    df['Max Power'] = df['Max Power'].apply(regex.get_power_from)
    # only car that slipped by the regex has the following string
    # '306 PS @ 6400 rpm (race)300 PS @ 6000 rpm (menu)'
    df.loc[516, 'Max Power'] = 300
    df['Max Power'] = df['Max Power'].astype(np.int32)
    return df


def add_manufacturing_date(df):
    df['Date'] = df['Name'].apply(regex.get_date_from)
    for i, row in df[df['Date'].isna()].iterrows():
        year = scrape.scrape_date_from_description(row['href'])
        if year is not None:
            print(f'Found {year} as manufacturing date for {row["Name"]}')
            df.loc[i, 'Date'] = year
        else:
            print(f'Could not find a manufacturing date for {row["Name"]}')
    return df


def add_is_race_modifiable(df):
    """Careful requires scraping"""
    df['IsRaceModifiable'] = df['href'].apply(scrape.scrape_is_race_modifiable)
    return df


def clean_drivetrain(df):

    def _clean_drivetrain(drivetrain):
        if drivetrain in mappings.DRIVETRAIN_MAPPING:
            drivetrain = mappings.DRIVETRAIN_MAPPING[drivetrain]
        return drivetrain

    df['Drivetrain'].apply(_clean_drivetrain)
    return df


def clean_displacement(df):
    df['Displacement'] = df['Displacement'].apply(regex.get_displacement_from)
    return df


def clean_weight(df):
    df['Weight'] = df['Weight'].apply(regex.get_weight_from)
    return df


def clean_dimensions(df):
    for dimension in ['Length', 'Width', 'Height']:
        df[dimension] = df[dimension].apply(regex.get_dimension_from)
    return df


def clean_power_weight_ratio(df):
    df['Power/Weight Ratio'] = df['Power/Weight Ratio'].apply(regex.get_power_weight_ratio_from)
    return df
