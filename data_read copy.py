import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

metadata = pd.read_excel('metadata.xlsx')

full_data = pd.read_csv('RBDS001runT35markers.txt', delimiter='\t')

# remove duplicate rows
metadata = metadata.drop_duplicates(subset=metadata.columns[0])

metadata.to_csv('metadata_actual.csv', index=False)

# Pull the forefoot, midfoot, and rearfoot strike patterns from the right foot for running at 3.5 m/s

# Create empty lists

forefoot = []
midfoot = []
rearfoot = []


# check if 'RFSI35' is in metadata's columns
if 'RFSI35' in metadata.columns:

    # append FileName to the list where RFSI35 is 'Forefoot'
    forefoot.extend(metadata.loc[metadata['RFSI35'] == 'Forefoot', 'FileName'].tolist())

    # append FileName to the list where RFSI35 is 'Midfoot'
    midfoot.extend(metadata.loc[metadata['RFSI35'] == 'Midfoot', 'FileName'].tolist())

    # append FileName to the list where RFSI35 is 'Rearfoot'
    rearfoot.extend(metadata.loc[metadata['RFSI35'] == 'Rearfoot', 'FileName'].tolist())

    # Replace the static portion in the file name with runT35markers to correspond to the markers text file from the run at 3.5 m/s

forefoot = [name.replace('static', 'runT35markers') for name in forefoot]
midfoot = [name.replace('static', 'runT35markers') for name in midfoot]
rearfoot = [name.replace('static', 'runT35markers') for name in rearfoot]

def data_read_full(path):
    
    data = pd.read_csv(path, delimiter='\t')

    # data_labels_old = ['Time', 'R.Heel.BottomX', 'R.Heel.BottomY', 'R.Heel.BottomZ', 'R.Heel.TopX', 'R.Heel.TopY', 'R.Heel.TopZ', 'R.Heel.LateralX', 'R.Heel.LateralY', 'R.Heel.LateralZ','R.MT1X', 'R.MT1Y', 'R.MT1Z', 'R.MT5X', 'R.MT5Y', 'R.MT5Z', 'R.ASISX', 'R.ASISY', 'R.ASISZ', 'R.Shank.Bottom.LateralX', 'R.Shank.Bottom.LateralY', 'R.Shank.Bottom.LateralZ', 'R.Shank.Bottom.MedialX', 'R.Shank.Bottom.MedialY', 'R.Shank.Bottom.MedialZ', 'R.Shank.Top.LateralX', 'R.Shank.Top.LateralY', 'R.Shank.Top.LateralZ', 'R.Shank.Top.MedialX', 'R.Shank.Top.MedialY', 'R.Shank.Top.MedialZ']

    data_labels = ['Time', 'R.Heel.BottomX', 'R.Heel.BottomY', 'R.Heel.TopX', 'R.Heel.TopY','R.MT1X', 'R.MT1Y']

    data_new = data[data_labels]

    out = pd.concat([data_new], ignore_index=True)

    out = out.apply(lambda x: x/100 if x.name != 'Time' else x)
    
    return out

def data_read_partial(path):
    
    data = pd.read_csv(path, delimiter='\t')

    # data_labels_old = ['Time', 'R.Heel.BottomX', 'R.Heel.BottomY', 'R.Heel.BottomZ', 'R.Heel.TopX', 'R.Heel.TopY', 'R.Heel.TopZ', 'R.Heel.LateralX', 'R.Heel.LateralY', 'R.Heel.LateralZ','R.MT1X', 'R.MT1Y', 'R.MT1Z', 'R.MT5X', 'R.MT5Y', 'R.MT5Z', 'R.ASISX', 'R.ASISY', 'R.ASISZ', 'R.Shank.Bottom.LateralX', 'R.Shank.Bottom.LateralY', 'R.Shank.Bottom.LateralZ', 'R.Shank.Bottom.MedialX', 'R.Shank.Bottom.MedialY', 'R.Shank.Bottom.MedialZ', 'R.Shank.Top.LateralX', 'R.Shank.Top.LateralY', 'R.Shank.Top.LateralZ', 'R.Shank.Top.MedialX', 'R.Shank.Top.MedialY', 'R.Shank.Top.MedialZ']

    data_labels = ['Time', 'R.Heel.BottomX', 'R.Heel.BottomY', 'R.Heel.TopX', 'R.Heel.TopY','R.MT1X', 'R.MT1Y']

    data_new = data[data_labels]

    out = pd.concat([data_new], ignore_index=True)


    out = out.apply(lambda x: x/100 if x.name != 'Time' else x)

    def closest_time(target_time):
        # Find the absolute difference between the target time and each time in the DataFrame
        absolute_differences = out['Time'].apply(lambda x: abs(x - target_time))
        # Find the index of the smallest difference
        closest_index = absolute_differences.idxmin()
        # Return the row with this index
        return out.loc[[closest_index]]

    times = [0, 5, 10, 15, 20, 25, 30]

    out_filtered = pd.concat([closest_time(time) for time in times])

    # out_filtered = out[out['Time'].isin(times)]

    # out_filtered.iat[-1, out_filtered.columns.get_loc('Time')] = 30
    
    return out_filtered

def format_data(df, col1, col2, filename):
    formatted_data = []
    for _, row in df.iterrows():
        formatted_data.append(f"<pt>{row[col1]},{row[col2]}</pt>")
    
    with open(filename, 'w') as f:
        f.write('\n'.join(formatted_data))

    print(f'Points written to file: {filename}')


## Section to write the full data to processed_full directory

# Create an empty dictionary to store the DataFrames
forefoot_dfs = {}
midfoot_dfs = {}
rearfoot_dfs = {}

columns = ['R.Heel.BottomX', 'R.Heel.BottomY', 'R.Heel.TopX', 'R.Heel.TopY','R.MT1X', 'R.MT1Y']

for path in forefoot:
    # Extract the number before "run" in the filename
    number = path.split('run')[0][-1]

    # Read the data and store the DataFrame in the dictionary
    df = data_read_full(path)
    forefoot_dfs[f'forefoot_{number}'] = df

    # Write the data to a file for each column
    for col in columns:
        format_data(df, 'Time', col, f'processed_full/forefoot/forefoot_{number}_{col}_full')

for path in midfoot:
    # Extract the number before "run" in the filename
    number = path.split('run')[0][-1]

    # Read the data and store the DataFrame in the dictionary
    df = data_read_full(path)
    forefoot_dfs[f'midfoot{number}'] = df

    # Write the data to a file for each column
    for col in columns:
        format_data(df, 'Time', col, f'processed_full/midfoot/midfoot{number}_{col}_full')

for path in rearfoot:
    # Extract the number before "run" in the filename
    number = path.split('run')[0][-1]

    # Read the data and store the DataFrame in the dictionary
    df = data_read_full(path)
    forefoot_dfs[f'rearfoot{number}'] = df

    # Write the data to a file for each column
    for col in columns:
        format_data(df, 'Time', col, f'processed_full/rearfoot/rearfoot_{number}_{col}_full')


## Section to write data every 0, 5, 10, 15, 20, 25, and 30 seconds to processed_partial directory

# Create an empty dictionary to store the DataFrames
forefoot_dfs = {}
midfoot_dfs = {}
rearfoot_dfs = {}

columns = ['R.Heel.BottomX', 'R.Heel.BottomY', 'R.Heel.TopX', 'R.Heel.TopY','R.MT1X', 'R.MT1Y']

for path in forefoot:
    # Extract the number before "run" in the filename
    number = path.split('run')[0][-1]

    # Read the data and store the DataFrame in the dictionary
    df = data_read_partial(path)
    forefoot_dfs[f'forefoot_{number}'] = df

    # Write the data to a file for each column
    for col in columns:
        format_data(df, 'Time', col, f'processed_partial/forefoot/forefoot_{number}_{col}_partial')

for path in midfoot:
    # Extract the number before "run" in the filename
    number = path.split('run')[0][-1]

    # Read the data and store the DataFrame in the dictionary
    df = data_read_partial(path)
    forefoot_dfs[f'midfoot{number}'] = df

    # Write the data to a file for each column
    for col in columns:
        format_data(df, 'Time', col, f'processed_partial/midfoot/midfoot{number}_{col}_partial')

for path in rearfoot:
    # Extract the number before "run" in the filename
    number = path.split('run')[0][-1]

    # Read the data and store the DataFrame in the dictionary
    df = data_read_partial(path)
    forefoot_dfs[f'rearfoot{number}'] = df

    # Write the data to a file for each column
    for col in columns:
        format_data(df, 'Time', col, f'processed_partial/rearfoot/rearfoot_{number}_{col}_partial')