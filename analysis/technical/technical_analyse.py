import os
import pandas as pd
from ta import add_all_ta_features

# Define the data folder and the folders for the processed data
data_folder = 'data'

# List all the directories in the data folder
directories = [f.path for f in os.scandir(data_folder) if f.is_dir()]

# Loop through all the directories
for directory in directories:
    crypto = directory.split('/')[-1]
    crypto_processed_folder = os.path.join(data_folder, crypto)

    # Create the processed folder for the crypto if it doesn't exist
    if not os.path.exists(crypto_processed_folder):
        os.makedirs(crypto_processed_folder)

    # List all the files in the crypto folder
    files = os.listdir(directory)

    # Loop through all the files
    for file in files:
        # Check if the file is a JSON file
        if file.endswith('_historical_data.json'):
            # Load the data
            df = pd.read_json(os.path.join(directory, file))

            # convert timestamps to datetime format
            df['timeOpen'] = pd.to_datetime(df['timeOpen'])
            df['timeClose'] = pd.to_datetime(df['timeClose'])
            df['timeHigh'] = pd.to_datetime(df['timeHigh'])
            df['timeLow'] = pd.to_datetime(df['timeLow'])

            # split 'quote' column into separate columns
            df = pd.concat([df.drop('quote', axis=1), df['quote'].apply(pd.Series)], axis=1)

            # add technical indicators as features
            df = add_all_ta_features(df, "open", "high", "low", "close", "volume")

            # save the updated data to a new JSON file
            crypto_name = file.split('_')[0]
            new_file_name = f'{crypto_name}_technical_data.json'
            df.to_json(os.path.join(data_folder, crypto_name, new_file_name))
