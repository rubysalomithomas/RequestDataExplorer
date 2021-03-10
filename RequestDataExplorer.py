import base64
import json

import pandas as pd
import requests
import streamlit as st

st.title('Request Transaction and Data Explorer')

st.markdown("""
This app performs simple webscraping of Request Network transcations and the associtated IPFS data.
* **Data source:** [REQ Burner Contract](https://etherscan.io/address/0x7b3c4d90e8af6030d66c07f8f815f9505e379d6f#internaltx), [Custom IPFS node](http://requestipfsdata.switzerlandnorth.azurecontainer.io:8080/ipfs).
""")

st.sidebar.header('User Input Features')


# Web scraping of Request data
@st.cache(allow_output_mutation=True)
def load_data():
    all_tx_url = "https://api.etherscan.io/api?module=account&action=txlistinternal&address=0x7b3c4d90e8af6030d66c07f8f815f9505e379d6f&startblock=0&endblock=999999999&sort=desc&apikey=A37KV8A3HWW2PSUG3K2EF6BCJVNWCPKDP8"
    json = pd.read_json(all_tx_url)
    df = pd.json_normalize(json['result'])
    dtformat = pd.to_datetime(df['timeStamp'], unit='s')
    df['year'] = pd.DatetimeIndex(dtformat).year
    df['month'] = pd.DatetimeIndex(dtformat).month_name()
    df['week'] = pd.DatetimeIndex(dtformat).week
    df['day'] = pd.DatetimeIndex(dtformat).day
    df['day_name'] = pd.DatetimeIndex(dtformat).day_name()
    df['utc_time'] = pd.DatetimeIndex(dtformat).time
    df = df.drop(
        columns=['timeStamp', 'value', 'contractAddress', 'input', 'type', 'gas', 'gasUsed', 'traceId', 'isError',
                 'errCode'])
    df = df[['blockNumber', 'year', 'month', 'week', 'day', 'day_name', 'utc_time', 'hash']]
    df['tx_url'] = "https://api.etherscan.io/api?module=proxy&action=eth_getTransactionReceipt&txhash=" + df[
        'hash'] + "&apikey=A37KV8A3HWW2PSUG3K2EF6BCJVNWCPKDP8"

    return df[:10]


reqdata = load_data()


# get ipfs hash
def load_ipfs(tx_url):
    response = requests.get(tx_url)
    json2 = json.loads(response.content)
    hashstr = json2['result']['logs'][0]['data']
    ipfs_hash = bytearray.fromhex(hashstr[258:350]).decode()

    dataresponse = requests.get("http://requestipfsdata.switzerlandnorth.azurecontainer.io:8080/ipfs/" + ipfs_hash)
    json2 = pd.json_normalize(json.loads(dataresponse.content))

    return ipfs_hash


ipfslist = []
txlist = reqdata['tx_url'].tolist()

for tx in txlist:
    ipfslist.append(load_ipfs(tx))


# get ipfs hash
def load_ipfs_data(ipfs_hash):
    dataresponse = requests.get("http://requestipfsdata.switzerlandnorth.azurecontainer.io:8080/ipfs/" + ipfs_hash)
    json2 = json.loads(dataresponse.content)

    return json2


ipfsdatalist = []

for ipfs_hash in ipfslist:
    ipfsdatalist.append(load_ipfs_data(ipfs_hash))

reqdata['ipfs_hash'] = ipfslist
reqdata['ipfs_data'] = ipfsdatalist
reqdata = reqdata.drop(columns=['tx_url'])

# Sidebar - Year selection
ycontainer = st.sidebar.beta_container()
sorted_unique_year = sorted(reversed(reqdata.year.unique()))
year_all = st.sidebar.checkbox("Select all", key=1)

if year_all:
    selected_year = ycontainer.multiselect("Year:",
                                           sorted_unique_year, sorted_unique_year)
else:
    selected_year = ycontainer.multiselect("Year:",
                                           sorted_unique_year, default=sorted_unique_year[-1])

# Sidebar - Month selection
mcontainer = st.sidebar.beta_container()
unique_month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                'November', 'December']
month_all = st.sidebar.checkbox("Select all", key=2)
if month_all:
    selected_month = mcontainer.multiselect("Month:",
                                            unique_month, unique_month)
else:
    selected_month = mcontainer.multiselect("Month:",
                                            unique_month, default=unique_month[2])

# Sidebar - Day Name selection
dncontainer = st.sidebar.beta_container()
sorted_unique_day_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
# selected_day_name = st.sidebar.multiselect('Day Name', sorted_unique_day_name, sorted_unique_day_name)
dn_all = st.sidebar.checkbox("Unselect all", key=3)
if dn_all:
    selected_day_name = dncontainer.multiselect("Day Name:",
                                                sorted_unique_day_name)
else:
    selected_day_name = dncontainer.multiselect("Day Name:",
                                                sorted_unique_day_name, sorted_unique_day_name)

# Sidebar - Week selection
wcontainer = st.sidebar.beta_container()
sorted_unique_week = sorted(reqdata.week.unique())
# selected_week = st.sidebar.multiselect('Week', sorted_unique_week, sorted_unique_week)
w_all = st.sidebar.checkbox("Unselect all", key=4)
if w_all:
    selected_week = wcontainer.multiselect("Week:",
                                           sorted_unique_week)
else:
    selected_week = wcontainer.multiselect("Week:",
                                           sorted_unique_week, sorted_unique_week)

# Sidebar - Day selection
dcontainer = st.sidebar.beta_container()
sorted_unique_day = sorted(reqdata.day.unique())
# selected_day = st.sidebar.multiselect('Day', sorted_unique_day, sorted_unique_day)
d_all = st.sidebar.checkbox("Unselect all", key=5)
if d_all:
    selected_day = dcontainer.multiselect("Day:",
                                          sorted_unique_day)
else:
    selected_day = dcontainer.multiselect("Day:",
                                          sorted_unique_day, sorted_unique_day)

# Filtering data
df_reqdata = reqdata[(reqdata.year.isin(selected_year)) & (reqdata.month.isin(selected_month)) & (
    reqdata.day_name.isin(selected_day_name)) & (reqdata.week.isin(selected_week)) & (reqdata.day.isin(selected_day))]

st.header('Transactions for the selected criteria')
# st.write('Data Dimension: ' + str(df_reqdata.shape[0]) + ' rows and ' + str(df_reqdata.shape[1]) + ' columns.')
st.dataframe(df_reqdata, width=2500, height=600)


# Download data
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="reqtxipfsdata.csv">Download data as CSV file</a>'
    return href


st.markdown(filedownload(df_reqdata), unsafe_allow_html=True)
