import pandas as pd

# Please change the file path to the location where you stored the data.
# You may copy it from the previous task.
df = pd.read_csv('type here')

# As usual, print the first 5 rows in df to have a glance of its structure.
type here

# select rows in which Obama won, and load the rows to obama_df
obama_df = df[type here]

#print obama_df to check if the selection is correct.
obama_df

# print the shape of obama_df.
# The output would tell you the number of rows and columns in obama_df.
# Then you know how many counties did Obama win in PA.
obama_df.shape

# add a new column in df to store the difference of vote percentages between Obama and Romney
df['diff_pct'] = df[type here]- df[type here]

# select rows in which Obama won Romney by at least 10%.
obama_win_big = df[df['diff_pct']>10]

# print only the county names in obama_win_big
obama_win_bigtype here

# Calculate the turnout of counties where Obama won
# First, get the counties where Obama won (obama_eligible_voters)
obama_counties = type here

# Next, calculate the total eligible voters in obama_counties (obama_total_voters)
obama_total_voters = type here

# Then, calculate actual voters in counties where Obama won.
obama_actual_voters = type here

# Finally, calculate the turnout ratio in counties where Obama won.
# Think about why you need float(). Try what if not using float()
obama_county_tournout = float(obama_actual_voters)/float(obama_total_voters)

# Print obama_county_tournout
