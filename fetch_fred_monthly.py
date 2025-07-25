# THIS IS THE FILE THAT SHOULD BE EXECUTED TO UPDATE THE ECON DATA

import datetime
from code.FRED_API import fetch_fred_data
import pandas as pd

# Set full range. End data pulls todays date to catch the most uptodate data
start_date = "2000-01-01"
end_date = datetime.date.today().strftime("%Y-%m-%d")

# Pull and save to local file. Call the API function (fetch_fred_data in FRED_APY.py) and passes in the date range from above and then saves the df to csv
df = fetch_fred_data(start_date, end_date)

# Create derivative variables -------------------------------------------------------
df['Grocery Units'] = df['Grocery Sales']/df['CPI (Food at Home)']
df['Restaurant Units'] = df['Restaurant Sales']/df['CPI (Food away from Home)']

# save the csv to update the proper programs
df.to_csv("C:/Users/eric/Documents/Python/econ_dashboard/output/fetch_fred_data.csv") # need forward slashes!!!

print(f"✅ Data refreshed and saved on {datetime.datetime.now().isoformat()}")
