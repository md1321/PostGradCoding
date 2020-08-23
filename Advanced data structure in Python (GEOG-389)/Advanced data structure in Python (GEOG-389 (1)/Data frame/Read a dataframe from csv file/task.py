# import pandas as an abbreviation pd
type here as pd
# change the setting to print more rows
pd.set_option('display.expand_frame_repr', False)

# Read the spreadsheet (election.csv) and assign the data inside to df.
# Please change the file path to the location where you stored the data.
df = pd.read_csv('C:\Users\yi\Documents\UH_work\Teaching\GEOG389\labs\lab2_data\election.csv')


# Get the first 5 rows of df
df.head()

# Get the first 5 rows using index
df[type here]

# Get the column 'total'
df[type here]

# Use another method to get the column of total.
df.total

# Calculate the summation of numbers in the column 'total'
type here.sum()

# Get three columns from df, including total, voters, and turnout. Group them into a new data frame sub_df
sub_df=df[type here]

# Print the first 5 rows in sub_df
sub_df.type here
