import base64
import json

import pandas as pd
import requests
import streamlit as st

st.title('Request Transaction and Data Explorer')

st.sidebar.header('User Input Features')


# Web scraping of Request data
@st.cache(allow_output_mutation=True)
def load_data():
    all_tx_url = "https://api.etherscan.io/api?module=account&action=txlistinternal&address=0x7b3c4d90e8af6030d66c07f8f815f9505e379d6f&startblock=0&endblock=999999999&sort=desc&apikey=A37KV8A3HWW2PSUG3K2EF6BCJVNWCPKDP8"
    json = pd.read_json(all_tx_url)
   

    return json


reqdata = load_data()

st.json(reqdata)
