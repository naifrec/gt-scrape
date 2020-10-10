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
import seaborn as sns

from gt.paths import DATA_DIR

# +
# to install new font and use it with seaborn / matplotlib, see
# - install font: https://stackoverflow.com/a/20276525/5317241
# - instruct matplotlib to use it: https://github.com/matplotlib/matplotlib/issues/17568#issuecomment-638714360

font_files = mpl.font_manager.findSystemFonts()
font_files_roboto = [f for f in font_files if 'Roboto' in f]
for font_file in font_files_roboto:
    mpl.font_manager.fontManager.addfont(font_file)
mpl.rcParams['font.family'] = 'Roboto'
mpl.rcParams['figure.dpi'] = 300
# -

df = pd.read_csv(DATA_DIR / 'cars-clean-v2.csv', index_col=0)

100 * df['Date'].isna().sum() / len(df)

df = df[~df['Date'].isna()]
countries = df['Country'].value_counts().index.tolist()

df['Date'] = df['Date'].astype(np.int32)

print(100 * ((df['Date'] >= 1990).sum() / len(df)))

df = df.groupby(by=['Date', 'Country']).count()
df = df[['Name']].rename({'Name': 'Count'}, axis=1)

years = list(range(1964, 2001))
for year in years:
    if year not in df.index.get_level_values(0):
        for country in countries:
            df.loc[(year, country), 'Count'] = 0
    else:
        for country in countries:
            if country not in df.loc[year].index:
                df.loc[(year, country), 'Count'] = 0

df = df.sort_index()

df = df.swaplevel().sort_index()

# +
palette = sns.color_palette("husl", 8)
fig, ax = plt.subplots(figsize=(10, 8))
sns.set_theme(style="whitegrid", font='Roboto')

plots = []
width = 0.5
bottom = np.zeros_like(df.loc['France', 'Count'].values)
for i, country in enumerate(countries):
    counts = df.loc[country, 'Count'].values
    p = plt.bar(
        years, counts, width,
        bottom=bottom,
        label=country,
        log=False,
        color=palette[i],
    )
    bottom += counts

# title
ax.text(x=0.0, y=1.05, s='Timeline of car manufacturing year in GT2', fontsize=18, weight='bold', ha='left', va='bottom', transform=ax.transAxes)
ax.text(x=0.0, y=1.01, s='90\'s cars are over represented, 70\'s almost absent', fontsize=16, alpha=0.75, ha='left', va='bottom', transform=ax.transAxes)
ax.text(x=0.43, y=-0.12, s='Source: Gran Turismo Wiki | Data viz: @gsautiere', fontsize=14, weight='medium', alpha=1.0, ha='left', va='bottom', transform=ax.transAxes)

# prettify
sns.despine(bottom=True, left=True)  # remove borders of plot
plt.legend(fontsize=16)
plt.show()
# -


