import base64
import json

import pandas as pd
import requests
import streamlit as st

st.title('Test simple API')

option = st.sidebar.selectbox(
    "Year",
    ("2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019","2020", "2021", "2022", "2023"))

st.write("You selected:", option)
# Web scraping of Request data
# https://api.census.gov/data/2021/cps/basic/jan?get=PELKAVL,PELKDUR,PELKFTO,PELKLL1O,PELKLL2O,PELKLWO,PELKM1&for=state:51&PEEDUCA=39
@st.cache(allow_output_mutation=True)
def load_data(option):
    all_tx_url = "https://jsonplaceholder.typicode.com/todos/" + option
    st.write(all_tx_url)
    st.write(option)
    json =  requests.get(all_tx_url)
    return json


reqdata = load_data(option)

st.json(reqdata.text)
