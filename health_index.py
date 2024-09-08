# This is a sample Python script.
import os

import imageio
import netCDF4 as nc
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
from paths import data_dir
from fragmentation_indices import run_fragmentation
from utils import random_discrete_cmap
import matplotlib.colors as mcolors


def calculate_one_three_five_day_deltas(ocean_area, dates):
    print(dates)
    years = list(set([date[:4] for date in dates]))
    deltas = []

    #zip ocean are and years, if the year is different from the previous, set deltas to 0
    for i, (area, date) in enumerate(zip(ocean_area, dates)):
        if i == 0:
            deltas.append([0, 0, 0])
            continue

        if date[:4] != dates[i - 1][:4]:
            deltas.append([0, 0, 0])
            continue

        one_day_delta = area - ocean_area[i - 1]
        try:
            three_day_delta = area - ocean_area[i - 3] # i dont like this approach so i will not be using it
        except IndexError:
            three_day_delta = 0

        try:
            five_day_delta = area - ocean_area[i - 5] # i dont like this approach so i will not be using it
        except IndexError:
            five_day_delta = 0

        deltas.append([one_day_delta, three_day_delta, five_day_delta])


    deltas = np.abs(deltas)

    return deltas


def make_animation(img_list, label_list, dates):
    #plot a gif of label_list
    os.makedirs("frames", exist_ok=True)
    cmap=random_discrete_cmap(200)

    for i, (img, array, date) in enumerate(zip(img_list, label_list, dates)):
        plt.imshow(img, cmap='gray')
        plt.imshow(array, cmap=cmap, alpha=0.4)
        plt.colorbar()
        plt.title(f'{date}')
        plt.axis('off')
        plt.savefig(f'frames/{date}')  # Save each frame as a PNG
        plt.close()

    frames = []
    for i, date in enumerate(dates):
        image_path = f'frames/{date}.png'
        frames.append(imageio.imread(image_path))

    # Save the frames as a GIF
    imageio.mimsave('animation.gif', frames, duration=0.5)


def get_date(filepath):
    date = os.path.basename(filepath).split('_')[0]
    print(date)
    date = date.split('-')[3]
    return date


class HealthIndex:
    def __init__(self, filepath):
        self.filepath = filepath
        self.date = get_date(filepath)

    def get_array(self):
        ds = nc.Dataset(self.filepath, 'r')

        var_name = list(ds.variables.keys())[0]
        variable = ds.variables[var_name]

        print(f"\nVariable: {var_name}")
        print("Shape:", variable.shape)
        print("Data type:", variable.dtype)

        data = variable[:]

        data = np.array(data)

        return data

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    file_path = os.path.join(data_dir, os.listdir(data_dir)[2])
    test_ = HealthIndex(file_path)
    test_array = test_.get_array()
    test_dict = run_fragmentation(test_array, plot=True)

    return_dicts = []
    dates = []

    my_files = os.listdir(data_dir)

    for file in my_files:
        file_path = os.path.join(data_dir, file)
        test_ = HealthIndex(file_path)
        test_array = test_.get_array()

        fragmentation_data = run_fragmentation(test_array, plot=False)

        dates.append(test_.date)
        return_dicts.append(fragmentation_data)

    #deltas must be restricted to specific years!


    deltas = calculate_one_three_five_day_deltas([d['total_ocean_area'] for d in return_dicts], dates)

    #lineplot of deltas
    df_deltas = pd.DataFrame(deltas, columns=['one_day', 'three_day', 'five_day'])

    #smooth out the data
    df_deltas['fragmentation_mobility'] = df_deltas['one_day'].rolling(window=5).mean()

    df_deltas['date'] = dates

    plt.figure(figsize=(16, 7))
    sns.lineplot(data=df_deltas, x='date', y='fragmentation_mobility', label='One Day Delta')
    #change y label
    plt.ylabel('5-day Rolling Fragment Mobility')

    plt.xticks(ticks=np.arange(0, len(dates), 92), labels=dates[::92], rotation=45)
    plt.tight_layout()
    plt.savefig('lineplot.png', dpi=300)
    plt.show()




    df_keys = ['total_ocean_area', 'fragmentation_perimeter', 'fragmentation_index', 'average_ocean_fragment_area', 'fragment_skewness', 'ratio_largest_to_rest']
    df_return_dicts = [{key: value for key, value in d.items() if key in df_keys} for d in return_dicts]

    df = pd.DataFrame(df_return_dicts, index=dates)
    df['year'] = df.index.str[:4]

    #add one day deltas to df without it ending up as nan
    df['fragmentation_mobility'] = df_deltas['fragmentation_mobility'].values.tolist()
    df_keys.append('fragmentation_mobility')

    print(df)
    #scale data between 0 and 1 for numeric columns

    df[df_keys] = (df[df_keys] - df[df_keys].min()) / (df[df_keys].max() - df[df_keys].min())

    #plot heatmap of 'total_areas' by rank by date, rows by year, cols by date

    def random_discrete_cmap(n):
        """Create a random discrete colormap with `n` colors."""
        colors = plt.cm.get_cmap('tab20', n)  # Use tab20 for a qualitative colormap with `n` colors
        return colors


    # Sort the DataFrame by index
    df = df.sort_index()

    # Extract the year and drop it from the main DataFrame
    year = df['year'].astype('str')
    df = df.drop(columns=['year'])

    # Plot the heatmap
    plt.figure(figsize=(13, 7))
    sns.heatmap(df.T, cmap='viridis', cbar=True)

    mid_point = int(92/2)
    #only show 1 xtick per every 31, label derived from 'year', starting at index 15
    plt.xticks(ticks=np.arange(mid_point, len(df), 92), labels=year[mid_point::92], rotation=0)
    #draw vertical red lines ever 92 days
    for i in range(0, len(df), 92):
        plt.axvline(i, color='white', linewidth=2)
    plt.title('June, July, August Fragmentation Indices 2013-2024')
    # Ensure enough space for labels
    plt.tight_layout()
    plt.savefig('heatmap.png', dpi=300)
    plt.show()
    #save




