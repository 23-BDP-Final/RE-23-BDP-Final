import pandas as pd

file_paths = ["backend_listing.csv", "frontend_listing.csv", "data_listing.csv","mobile_listing.csv"]

dataframes = [pd.read_csv(file) for file in file_paths]

combined_dataframe = pd.concat(dataframes, ignore_index=True)

combined_dataframe.to_csv("combined_list.csv", index=False)
