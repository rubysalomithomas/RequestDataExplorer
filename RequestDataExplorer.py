import base64
import json

import pandas as pd
import requests
import streamlit as st

st.title('Test simple API')

st.sidebar("Filters")
option = st.selectbox(
    "Year",
    ("2019", "2020", "2021"))

st.write("You selected:", option)
# Web scraping of Request data
@st.cache(allow_output_mutation=True)
def load_data():
    all_tx_url = "https://jsonplaceholder.typicode.com/todos/1"
    json =  requests.get(all_tx_url)
    return json


reqdata = load_data()

st.json(reqdata.text)
