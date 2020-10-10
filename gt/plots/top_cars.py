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
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from IPython.display import Image, display

from gt.paths import DATA_DIR, IMAGE_DIR

mpl.rcParams['figure.dpi'] = 300
# -

df = pd.read_csv(DATA_DIR / 'cars-clean-v2.csv', index_col=0)

len(df)

df.columns.tolist()

filename = df.loc[0, 'ImagePath']
filepath = IMAGE_DIR / filename
display(Image(filepath))

columns = ['Name', 'Max Power', 'Weight', 'Power/Weight Ratio']
top = df.sort_values(by='Power/Weight Ratio').head(12)
top = top.reset_index()
top.drop('index', axis=1, inplace=True)
top.index += 1
with open('max-power.md', 'w') as handle:
    top[columns].to_markdown(handle)

# +
fig, axes = plt.subplots(nrows=4, ncols=3, figsize=(12, 12))

for n, (_, car) in enumerate(top.iterrows()):
    i = n // 3
    j = n % 3
    ax = axes[i, j]

    filepath = IMAGE_DIR / car['ImagePath']
    image = plt.imread(filepath)
    ax.imshow(image)
    ax.text(10, 30, f'{n+1}', color='white', size=24)
    ax.axis('off')

plt.tight_layout()
# -

for country in df['Country'].unique():
    filter_country = df['Country'] == country
    id_best = df[filter_country]['Power/Weight Ratio'].idxmin()
    id_worst = df[filter_country]['Power/Weight Ratio'].idxmax()
    
    for car_id, car_type in zip([id_best, id_worst], ['Best', 'Worst']):
        car = df.loc[car_id]
        print(f'==============================================================')
        print(f'{car_type} car in terms of power / weight ratio from {country}')
        print(f'Name: {car["Name"]}')
        print(f'Power / Weight ratio: {car["Power/Weight Ratio"]} kg per bhp')
        print(f'Power: {car["Max Power"]} bhp')
        print(f'Weight: {car["Weight"]} kg')
        print(f'Drivetrain: {car["Drivetrain"]}')
        filepath = IMAGE_DIR / car['ImagePath']
        display(Image(filepath))


