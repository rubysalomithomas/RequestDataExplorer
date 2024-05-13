import base64
import json

import pandas as pd
import requests
import streamlit as st

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

#dataframe = pd.DataFrame(response)
#dd= dataframe.sum()
#st.write(dataframe)
if response.status_code == 200:
# Convert the response to JSON
 data = response.json()

# Convert the JSON data to a DataFrame
# The first element of the list contains the headers, the rest are the data rows
 df = pd.DataFrame(data[1:], columns=data[1])

# Display the DataFrame
 st.write(df)
else:
 st.write("Failed to retrieve data:", response.status_code)

