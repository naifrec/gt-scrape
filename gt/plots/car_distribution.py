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
# -

df = pd.read_csv(DATA_DIR / 'cars-clean-v2.csv', index_col=0)

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


# +
# taken from https://stackoverflow.com/a/51535326/5317241

def show_values_on_bars(axs):
    def _show_on_single_plot(ax):
        num_patches = len(ax.patches)
        for p in ax.patches:
            _x = p.get_x() + 4 * p.get_width() / 5
            _y = p.get_y() + p.get_height() / 2 + 0.03
            value = '{:.0f}'.format(p.get_width())
            if value == '1':
                _x += .055
            ax.text(_x, _y, value, ha="center", fontsize=14, color='white', weight='bold', fontname='Roboto')
    if isinstance(axs, np.ndarray):
        for idx, ax in np.ndenumerate(axs):
            _show_on_single_plot(ax)
    else:
        _show_on_single_plot(axs)


# +
fig, ax = plt.subplots(figsize=(8, 8))
sns.set_theme(font='Roboto')

log = True
# bar plot
sns.barplot(y='Manufacturing Country', x='# cars featured', data=data_cars, color=palette[0], label='All', log=log)
sns.barplot(y='Manufacturing Country', x='# cars featured', data=data_prize_cars, color=palette[1], label='Prize', log=log)
show_values_on_bars(ax)

# title
ax.text(x=0.0, y=1.05, s='Distribution of cars per country of origin in GT2', fontsize=18, weight='bold', ha='left', va='bottom', transform=ax.transAxes)
ax.text(x=0.0, y=1.01, s='Japanese cars are over represented in both categories', fontsize=16, alpha=0.75, ha='left', va='bottom', transform=ax.transAxes)
ax.text(x=0.3, y=-0.12, s='Source: Gran Turismo Wiki | Data viz: @gsautiere', fontsize=14, weight='medium', alpha=1.0, ha='left', va='bottom', transform=ax.transAxes)

# prettify
sns.despine(bottom=True, left=True)  # remove borders of plot
plt.xlabel('')
plt.ylabel('')
plt.yticks(fontsize=14)
plt.xticks(fontsize=14)
plt.legend(fontsize=16)
plt.show()
# -
