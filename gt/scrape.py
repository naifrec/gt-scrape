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

import pandas as pd
import requests
from bs4 import BeautifulSoup

URL_DOMAIN = 'https://gran-turismo.fandom.com'
URL_CAR_LIST = URL_DOMAIN + '/wiki/Gran_Turismo_2/Car_List'

page = requests.get(URL_CAR_LIST)
soup = BeautifulSoup(page.content, 'html.parser')
# -

# ## 1. Scrape the list of cars from GT Wiki

results = soup.find(id='mw-content-text')

manufacturers_raw = results.find_all('span', class_='mw-headline')
manufacturers =[]
for i, manufacturer in enumerate(manufacturers_raw):
    if 'NTSC-U version only' in manufacturer.text or 'PAL English only' in manufacturer.text:
        print(f'Skipping {manufacturer.text}')
        continue
    link = manufacturer.find('a')
    if link is None:
        continue
    manufacturers.append(link['title'])

len(manufacturers)

manufacturers

cars_raw = results.find_all('li')
cars_raw = cars_raw[:-2]  # removing the two side notes
cars = []
for i, car in enumerate(cars_raw):
    link = car.find('a')
    if 'Acura' in link.text or 'Vauxhall' in link.text:
        print(f'Skipping {link.text}')
        continue

    print(i, link['title'])
    cars.append(link)


# Mazda and Nissan will require cleaning as I am counting some cars double

def get_car_info(href):
    page = requests.get(URL_DOMAIN + car['href'])
    soup_car = BeautifulSoup(page.content, 'html.parser')
    labels = soup_car.find_all('h3', class_='pi-data-label')
    values = soup_car.find_all('div', class_='pi-data-value')
    assert len(labels) == len(values)
    return {label.text: value.text for label, value in zip(labels, values)}


get_car_info(cars[0])

car_infos = []
for i, car in enumerate(cars):
    print(f'Retrieving info for car {i+1}/{len(cars)}: {car.text}')
    try:
        car_infos.append(get_car_info(car['href']))
    except Exception as e:
        print(f'Failed to retrieve info, skipping, exception {e}')

len(car_infos)

len(cars)

for i, car in enumerate(cars):
    car_infos[i]['Name'] = car.text

for i, car in enumerate(cars):
    for manufacturer in manufacturers:
        if manufacturer.lower() in car.text.lower():
            car_infos[i]['ManufacturerWiki'] = manufacturer

df = pd.DataFrame(car_infos)

df

df.to_csv('cars.csv')

# ls -lh

df[['Name', 'Manufacturer', 'Max Power', 'Drivetrain']].sample(10)

df.sample(5)

sorted(df['Name'].unique().tolist())

# ## 2. Scrape the list of prize cars

# +
URL_PRIZE_CAR_LIST = 'https://www.ign.com/articles/2000/01/05/complete-gt2-prize-list'

# see https://stackoverflow.com/questions/38489386/python-requests-403-forbidden
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:80.0) Gecko/20100101 Firefox/80.0'}
page = requests.get(URL_PRIZE_CAR_LIST, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')
# -

table = soup.find('table')

rows = table.find_all('tr')

prize_cars = []
for i, row in enumerate(rows[2:]):  # skipping header columns
    columns = row.find_all('td')
    cars = columns[-1].text
    if cars:  # sometimes empty string due to empty rows used as separators
        prize_cars.extend(cars.split(','))
prize_cars = sorted(list(set(prize_cars)))
prize_cars = [name.strip() for name in prize_cars]

df_prize_cars = pd.DataFrame({'Name': prize_cars})

df_prize_cars.to_csv('prize_cars.csv')


