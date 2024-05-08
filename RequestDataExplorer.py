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

STATES =  {"1":'Alabama',"2":'Alaska',"3":'Arizona',"4":'Arkansas',"5":'California'}
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
    all_tx_url = "https://api.census.gov/data/" + year + "/cps/basic/"+month+"?get="+variable+"&for=state:"+state
    st.write(all_tx_url)
    st.write(year)
    json =  requests.get(all_tx_url)
    return json


reqdata = load_data(year,month,state,variable)

st.json(reqdata.text)
