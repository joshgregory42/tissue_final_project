'''
Description:

This code takes the strain written to the Models/Forefoot, Models/Midfoot, and Models/Rearfoot CSV files and calculates the maximum strain for each patient (i.e. takes the range of each column of the CSV file that corresponds to each patient). It then runs an ANOVA test with the entire dataset and then a t-test with only the midfoot and rearfoot datasets. 
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats


def strain_calcs(path):

    data = pd.read_csv(path)

    ranges = []

    # Iterate over the columns, skipping the first one
    for col in data.columns[1:]:
        # Calculate the range of the column
        col_range = data[col].max() - data[col].min()

        # Append the range to the list
        ranges.append(col_range)

    return ranges


fore_long = strain_calcs("Models/Forefoot/Graph_Data/long_forefoot_graph.csv")
fore_short = strain_calcs("Models/Forefoot/Graph_Data/short_forefoot_graph.csv")

mid_long = strain_calcs("Models/Midfoot/Graph_Data/Longmidfoot.csv")
mid_short = strain_calcs("Models/Midfoot/Graph_Data/Shortmidfoot.csv")

rear_long = strain_calcs("Models/Rearfoot/Graph_Data/long_rearfoot_graph.csv")
rear_short = strain_calcs("Models/Rearfoot/Graph_Data/short_rearfoot_graph.csv")


# Run ANOVA on long datsets

_, pval_long = stats.f_oneway(fore_long, mid_long, rear_long) # first output is f-value
_, pval_short = stats.f_oneway(fore_short, mid_short, rear_short)


print(f'p-value for long dataset: {pval_long}')
print(f'p-value for short dataset: {pval_short}')

# Perform a t-test with just the midfoot and rearfoot data

tvalue_long, pvalue_long = stats.ttest_ind(mid_long, rear_long)
tvalue_short, pvalue_short = stats.ttest_ind(mid_short, rear_short)

print(f'p-value for long dataset: {pvalue_long}')
print(f'p-value for short dataset: {pvalue_short}')

print('\n')
print(f't-value for long dataset: {tvalue_long}')
print(f't-value for short dataset: {tvalue_short}')