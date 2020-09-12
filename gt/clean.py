# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.6.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# -

df = pd.read_csv('cars.csv', index_col=0)

np.random.seed(0)
df.sample(5)

df.columns

# ## 1. Clean up manufacturers and map them to country

df['Manufacturer'] = df['ManufacturerWiki']

df.drop(columns='ManufacturerWiki', inplace=True)

manufacturers = df['Manufacturer'].unique()

sorted(manufacturers)

MANUFACTURER2COUNTRY = {
    'Alfa Romeo': 'Italy',
    'Aston Martin': 'United Kingdom',
    'Audi': 'Germany',
    'BMW': 'Germany',
    'Chevrolet': 'USA',
    'Chrysler': 'USA',
    'Citroën': 'France',
    'Daihatsu': 'Japan',
    'Dodge': 'USA',
    'Fiat': 'Italy',
    'Ford': 'USA',
    'Honda': 'Japan',
    'Jaguar': 'United Kingdom',
    'Lancia': 'Italy',
    'Lister': 'United Kingdom',
    'Lotus': 'United Kingdom',
    'MG': 'United Kingdom',
    'Mazda': 'Japan',
    'Mercedes-Benz': 'Germany',
    'Mercury': 'USA',
    "Mine's": 'Japan',
    'Mini': 'United Kingdom',
    'Mitsubishi': 'Japan',
    'Mugen': 'Japan',
    'Nismo': 'Japan',
    'Nissan': 'Japan',
    'Opel': 'Germany',
    'Peugeot': 'France',
    'Plymouth': 'USA',
    'RE Amemiya': 'Japan',
    'RUF': 'Germany',
    'Renault': 'France',
    'Saleen': 'USA',
    'Shelby': 'USA',
    'Spoon': 'Japan',
    'Subaru': 'Japan',
    'Suzuki': 'Japan',
    'TRD': 'Japan',  # Toyota Racing Development
    'TVR': 'United Kingdom',
    "Tom's": 'Japan',
    'Tommy Kaira': 'Japan',
    'Toyota': 'Japan',
    'Vector': 'USA',
    'Venturi': 'France',
    'Volkswagen': 'Germany',
}

df['Country'] = df['Manufacturer'].apply(lambda manufacturer: MANUFACTURER2COUNTRY[manufacturer])

df['Country']

countries = df['Country'].unique()
sorted(countries)

COUNTRY2CONTINENT = {
    'France': 'Europe',
    'Germany': 'Europe',
    'Italy': 'Europe',
    'Japan': 'Asia',
    'USA': 'America',
    'United Kingdom': 'Europe',
}

df['Continent'] = df['Country'].apply(lambda country: COUNTRY2CONTINENT[country])

df['Country'].value_counts()

plt.figure()
df['Country'].value_counts().plot.bar()
plt.xlabel('Manufacturing Country')
plt.ylabel('# cars featured')
plt.title('Distribution of cars per country of origin in GT2')
plt.show()

df[df['Name'].str.contains('\(')]['Name']

(df['Name'] == 'Mugen Accord SiR-T').sum()

df['Name'] = df['Name'].apply(lambda string: string.strip())

df[df['Name'].str.contains('Mugen')]['Name']

# ## 2. Put prize car information in table

df_prize_car = pd.read_csv('prize_cars.csv', index_col=0)

df_prize_car.sample(5)

# Problem: prize cars were listed inconsistently with or without manufacturer, and with different lower/upper case format.

df[df['Name'].str.contains('Mugen')]['Name']

df['IsPrizeCar'] = False
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
        print(f'{prize_car:53} was not found.')
print(f'Total of {len(prize_cars_not_found)}/{len(df_prize_car)} cars not found')

83-51

df['IsPrizeCar'].sum()

IGNNAME2WIKINAME = {
    "bp trueno gt '99": "Toyota BP APEX KRAFT Trueno GT (JGTC) '99",
    'mx-5 miata c spec': "Mazda MX-5 C-Spec",
    'momocorse mr2': "Toyota Momo Corse Apex MR2 GT (JGTC) '99",
    "mugen nsx gt '99": "Honda Castrol Mugen NSX GT (JGTC) '99",
    "r390 gt1 lm race car '97": "Nissan R390 GT1 Race Car '97",
    "r390 gt1lm race car'98": "Nissan R390 GT1 Race Car '98",
    'spoon civic type-r': "Spoon CIVIC TYPE R (EK) '00",
    'trd3000gt': "TRD 3000GT",
    'chaser trd sports x3': "TRD Chaser Sports X30",
    "cobra 427 '67": "Shelby Cobra 427 '66",
    "denso supra gt '99": "Toyota Denso Sard Supra GT (JGTC) '99",
    "gt-one race car '98": "Toyota GT-ONE Race Car (TS020) '98",
    'impreza wagon sti ver. v': "Subaru IMPREZA Sport Wagon WRX STi Version V '98",
    'kure r33 gt': "Nissan Kure R33 Skyline GT (JGTC) '97",
    'legacy wagon gt-b': "Subaru LEGACY Touring Wagon GT-B '96",
    'mx-5 miata a spec': "Mazda MX-5 A-Spec",
    'mugen cr-x ii': "Mugen CR-X Pro.2",
    'mugen cr-x iii': "Mugen CR-X Pro.3",
    'mugen civic type-r': "Mugen Civic Type R",
    'mugen ferio': "Mugen Civic Ferio",
    'mugen integra type-$': "Mugen Integra Type R",
    'nissan 300zx gt': "Nissan 300ZX-GTS GT (JGTC) '97",
    'plymouth spyder': "Plymouth PT Spyder",
    'spoon integra type-r': "Spoon INTEGRA TYPE R (DC2) '99",
    "supra gt '99": ["Toyota cdma One CERUMO Supra GT (JGTC) '99", "Toyota Denso Sard Supra GT (JGTC) '99 "],
    'trd2000gt': "TRD 2000GT",
    "tom's t020": "Tom’s (Toyota) T020",
    "tom's t111": "Tom’s (Toyota) T111",
    'unisia gt-r gt': "Nissan Unisia Jecs Skyline GT (JGTC) '99",
    'zz iii': "Tommy Kaira ZZ-III",
    'zzii': "Tommy Kaira ZZ-II '99",
}

for prize_cars in IGNNAME2WIKINAME.values():
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

df['IsPrizeCar'].sum()

len(df_prize_car)

plt.figure()
df['Country'].value_counts().plot.bar(label='all')
df[df['IsPrizeCar']]['Country'].value_counts().plot.bar(label='prize', color='red')
plt.xlabel('Manufacturing Country')
plt.xticks(rotation=45)
plt.ylabel('# cars featured')
plt.title('Distribution of cars per country of origin in GT2')
plt.legend()
plt.show()

data_cars = df['Country'].value_counts().reset_index().rename(
    {'index': 'Manufacturing Country',
     'Country': '# cars featured',
    }, axis=1)
data_cars

data_prize_cars = df[df['IsPrizeCar']]['Country'].value_counts().reset_index().rename(
    {'index': 'Manufacturing Country',
     'Country': '# cars featured',
    }, axis=1)
data_prize_cars

palette = sns.color_palette("husl", 8)

plt.figure(figsize=(8, 8))
sns.set_style(style="whitegrid")
sns.barplot(x='Manufacturing Country', y='# cars featured', data=data_cars, color=palette[0], label='all')
sns.barplot(x='Manufacturing Country', y='# cars featured', data=data_prize_cars, color=palette[1], label='prize')
plt.xticks(rotation=45)
plt.legend()
plt.title('Distribution of cars per country of origin in GT2')
plt.show()

plt.figure(figsize=(8, 8))
df['Country'].value_counts().plot.pie()


