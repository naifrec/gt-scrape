import re
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

URL_DOMAIN = 'https://gran-turismo.fandom.com'
URL_CAR_LIST = URL_DOMAIN + '/wiki/Gran_Turismo_2/Car_List'
URL_PRIZE_CAR_LIST = 'https://www.ign.com/articles/2000/01/05/complete-gt2-prize-list'
# see https://stackoverflow.com/questions/38489386/python-requests-403-forbidden
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:80.0) Gecko/20100101 Firefox/80.0',
}


def scrape_cars(root=None):
    page = requests.get(URL_CAR_LIST)
    soup = BeautifulSoup(page.content, 'html.parser')

    manufacturers = parse_manufacturers_from(soup)
    cars = parse_cars_from(soup)

    car_infos = []
    for i, car in enumerate(cars):
        print(f'Retrieving info for car {i+1}/{len(cars)}: {car.text}')
        try:
            car_infos.append(scrape_car_info(car, manufacturers))
        except Exception as e:
            print(f'Failed to retrieve info, skipping, exception {e}')

    # create dataframe and save to CSV
    df = pd.DataFrame(car_infos)
    root = root or '.'
    filepath = str(root / 'cars.csv')
    df.to_csv(filepath)
    print(f'Saved cars table to {filepath}')
    return df


def parse_manufacturers_from(soup):
    results = soup.find(id='mw-content-text')
    manufacturers_raw = results.find_all('span', class_='mw-headline')
    manufacturers =[]
    for i, manufacturer in enumerate(manufacturers_raw):
        if 'NTSC-U version only' in manufacturer.text or 'PAL English only' in manufacturer.text:
            print(f'Skipping {manufacturer.text} because exclusive to NTSC-U or PAL English')
            continue
        link = manufacturer.find('a')
        if link is None:
            continue
        manufacturers.append(link['title'])
    return manufacturers


def parse_cars_from(soup):
    results = soup.find(id='mw-content-text')
    cars_raw = results.find_all('li')
    cars_raw = cars_raw[:-2]  # removing the two side notes
    cars = []
    for i, car in enumerate(cars_raw):
        link = car.find('a')
        if 'Acura' in link.text or 'Vauxhall' in link.text:
            print(f'Skipping {link.text} because exclusive to NTSC-U or PAL English')
            continue
        cars.append(link)
    return cars


def scrape_car_info(car, manufacturers):
    page = requests.get(URL_DOMAIN + car['href'])
    soup_car = BeautifulSoup(page.content, 'html.parser')
    labels = soup_car.find_all('h3', class_='pi-data-label')
    values = soup_car.find_all('div', class_='pi-data-value')
    assert len(labels) == len(values)
    car_info = {'Name': car.text, 'href': car['href']}
    for manufacturer in manufacturers:
        if manufacturer.lower() in car.text.lower():
            car_info['ManufacturerWiki'] = manufacturer
    car_info.update({label.text: value.text for label, value in zip(labels, values)})
    return car_info


def scrape_prize_cars(root=None):
    page = requests.get(URL_PRIZE_CAR_LIST, headers=HEADERS)
    soup = BeautifulSoup(page.content, 'html.parser')

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

    # create dataframe and save to CSV
    df = pd.DataFrame({'Name': prize_cars})
    root = root or '.'
    filepath = str(root / 'prize_cars.csv')
    df.to_csv(filepath)
    print(f'Saved prize cars table to {filepath}')
    return df


def scrape_is_race_modifiable(href):
    page = requests.get(URL_DOMAIN + href)
    soup_car = BeautifulSoup(page.content, 'html.parser')
    result = soup_car.find('li', **{'data-name': 'Race Modifiable Vehicles'})
    return result is not None


def scrape_date_from_description(href):
    """
    Assumes that of all years present in the text, the largest is the
    manufacturing year.

    """
    page = requests.get(URL_DOMAIN + href)
    soup_car = BeautifulSoup(page.content, 'html.parser')

    years = []
    for paragraph in soup_car.find('div', class_='mw-content-text').find_all('p'):
        years.extend(re.findall(r' ([0-9]{4})[ ,\.]', paragraph.text))
    years = [int(year.strip()) for year in years]
    years = [year for year in years if (1960 < year < 2000)]
    if years:
        year = max(years)
        return year
    else:
        return None


def main(root=None):
    scrape_cars(root)
    scrape_prize_cars(root)


if __name__ == '__main__':
    import fire

    fire.Fire(main)
