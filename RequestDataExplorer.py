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
state = st.sidebar.selectbox(
    "State",
    ("1", "2", "3", "4", "5", "6", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21"))
variable = st.sidebar.selectbox(
    "Variables",
    ("PELKAVL", "PELKDUR", "PELKFTO", "PELKLL1O", "PLKLL2O", "PELKLWO", "PELKM1"))
CHOICES = {1: "dataset a", 2: "dataset b", 3: "dataset c"}


def format_func(option):
    return CHOICES[option]


option = st.selectbox("Select option", options=list(CHOICES.keys()), format_func=format_func)
st.write(f"You selected option {option} called {format_func(option)}")

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
