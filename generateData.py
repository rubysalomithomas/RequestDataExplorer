import requests
import pandas as pd
from datetime import datetime

def fetch_data_for_year(api_key, start_year, end_year, variables, base_url="https://api.census.gov/data"):
    months = ['jan']
    for year in range(start_year, end_year + 1):
        all_data = []
        for month in months:
            url = f"{base_url}/{year}/cps/basic/{month}?get={variables}&for=state:*&key={api_key}"
            print(url)
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 1:
                    df = pd.DataFrame(data[1:], columns=data[0])
                    # Convert necessary columns to numeric
                    if 'PWSSWGT' in df.columns:
                        df['PWSSWGT'] = pd.to_numeric(df['PWSSWGT'])
                        # Calculate total weight per state
                        total_weight = df.groupby('state')['PWSSWGT'].sum().reset_index().rename(columns={'PWSSWGT': 'TotalWeight'})
                        # Merge total weights back to the original dataframe
                        df = df.merge(total_weight, on='state')
                        # Calculate the proportion for each row
                        df['Proportion'] = df['PWSSWGT'] / df['TotalWeight']
                    all_data.append(df)
                else:
                    print(f"No valid data returned for {year} {month}")
            else:
                print(f"Failed to retrieve data for {year} {month}: {response.status_code}")

        # Save the combined yearly data to a CSV file
        if all_data:
            full_data = pd.concat(all_data)
            full_data.to_csv(f"demographic_data_{year}.csv", index=False)
            print(f"Data for {year} saved successfully in CSV format.")

# API Key and Variables Setup
api_key = 'abb48a2a48c7e5ae0598fd4d22daeedfc42ba874'
variables = "PELKAVL,PELKDUR,PELKFTO,PELKLL1O,PELKLL2O,PELKLWO,PELKM1"

# Fetch and process data from 2010 to the most recent complete year
current_year = datetime.now().year - 1
fetch_data_for_year(api_key, 2010, current_year, variables)
