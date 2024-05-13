import base64
import json

import pandas as pd
import requests
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title('Test simple API')

year = st.sidebar.selectbox(
    "Year",
    ("2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019","2020", "2021", "2022", "2023"))
month = st.sidebar.selectbox(
    "Month",
    ("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct","nov", "dec"))

STATES =  {"1":'Alabama',"2":'Alaska',"3":'Arizona',"4":'Arkansas',"5":'California',"6":'Colorado',"7":'Connecticut',"8":'Delaware',"9":'Florida',"10":'Georgia',"11":'Hawaii',"12":'Idaho',"13":'Illinois',"14":'Indiana',"15":'Iowa',
           "16":'Kansas',"17":'Kentucky',"18":'Louisiana',"19":'Maine',"20":'Maryland',"21":'Massachusetts',"22":'Michigan',"23":'Minnesota',"24":'Mississippi',"25":'Missouri',"26":'Montana',"27":'Nebraska',"28":'Nevada',"29":'New Hampshire',
          "30":'New Jersey',"31":'New Mexico',"32":'New York',"33":'North Carolina',"34":'North Dakota',"35":'Ohio',"36":'Oklahoma',"37":'Oregon',"38":'Pennsylvania',"39":'Rhode Island',"40":'South Carolina',"41":'South Dakota',
           "42":'Tennessee',"43":'Texas',"44":'Utah',"45":'Vermont',"46":'Virginia',"47":'Washington',"48":'West Virginia',"49":'Wisconsin',"50":'Wyoming'}
def displayStates(option):
    return STATES[option]
    
state = st.sidebar.selectbox(
    "Select State",
    options=list(STATES.keys()), format_func=displayStates)

VARIABLES =  {"PELKAVL":"Unemployed available for work last week", "PELKDUR":"Unemployed Number of weeks on job search", "PELKFTO":"Unemployed looking-full-time work wanted",
     "PELKLL1O":"Unemployed looking-activity before search", "PLKLL2O":"Unemployedlooking-lost/quit job", "PELKLWO":"Unemployed looking-when last worked", "PELKM1":"Unemployed looking-search methods"}
def displayVariables(option):
    return VARIABLES[option]
    
variable = st.sidebar.selectbox(
    "Select Variables",
    options=list(VARIABLES.keys()), format_func=displayVariables)


st.write("You selected:", year,month,variable)
# Web scraping of Request data
# https://api.census.gov/data/2021/cps/basic/jan?get=PELKAVL,PELKDUR,PELKFTO,PELKLL1O,PELKLL2O,PELKLWO,PELKM1&for=state:51&PEEDUCA=39
@st.cache(allow_output_mutation=True)
def load_data(year,month,state,variable):
    URL = "https://api.census.gov/data/" + year + "/cps/basic/"+month+"?get="+variable+"&for=state:"+state
    st.write(URL)
    st.write(year)
    json =  requests.get(URL)
    return json


response = load_data(year,month,state,variable)

data = np.random.randn(100)

# Create a Matplotlib figure
fig, ax = plt.subplots()
ax.hist(data, bins=20, alpha=0.5, color='blue')
ax.set_title('Random Gaussian Data (Histogram)')
ax.set_xlabel('Values')
ax.set_ylabel('Frequency')

# Display the figure in Streamlit
st.pyplot(fig)

# Check response status and content
if response.status_code == 200 and response.text:
    try:
        data = response.json()
        if data and len(data) > 1:  # Check if data contains more than just headers
            st.write("Data Headers:", data[0])
            df = pd.DataFrame(data[1:], columns=data[0])

            # Verify if 'PELKM1' column exists before proceeding
            if 'PELKM1' in df.columns:
                # Mapping dictionary for PELKM1
                job_search_methods = {
                    "1": "Contacted Employer Directly/Interview",
                    "2": "Contacted Public Employment Agency",
                    "3": "Contacted Private Employment Agency",
                    "4": "Contacted Friends Or Relatives",
                    "5": "Contacted School/University Employment Center",
                    "6": "Sent Out Resumes/Filled Out Application",
                    "7": "Checked Union/Professional Registers",
                    "8": "Placed Or Answered Ads",
                    "9": "Other Active",
                    "10": "Looked At Ads",
                    "11": "Attended Job Training Programs/Courses",
                    "12": "Nothing",
                    "13": "Other Passive"
                }
                df['PELKM1'] = df['PELKM1'].map(job_search_methods)
                st.dataframe(df['PELKM1'])  # Show the first few rows of the DataFrame
                # Sidebar for user input
                group_column = st.sidebar.selectbox('Select column to group by:', df.columns)
                
                # Perform grouping
                grouped_data = df.groupby(group_column)['PELKM1'].sum()
                
                # Create a plot using Plotly
                fig = px.bar(grouped_data, x=group_column, y='PELKM1', title='Total Values by Category')
                
                # Display the plot
                st.write("### Grouped Data Bar Chart", fig)
            else:
                st.write("Column 'PELKM1' does not exist in DataFrame.")
        else:
            st.write("Received data is empty or malformed.")
    except json.JSONDecodeError as e:
        st.write("JSON decode error:", e)
else:
    st.write("Failed to fetch data or empty response received.")
