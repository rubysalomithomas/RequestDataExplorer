import streamlit as st
import pandas as pd

# Title of the app
st.title("CSV File to DataFrame")

VARIABLES =  {"PELKAVL":"Unemployed available for work last week", "PELKDUR":"Unemployed Number of weeks on job search", "PELKFTO":"Unemployed looking-full-time work wanted",
     "PELKLL1O":"Unemployed looking-activity before search", "PLKLL2O":"Unemployedlooking-lost/quit job", "PELKLWO":"Unemployed looking-when last worked", "PELKM1":"Unemployed looking-search methods"}
def displayVariables(option):
    return VARIABLES[option]
    
variable = st.sidebar.selectbox(
    "Select Variables",
    options=list(VARIABLES.keys()), format_func=displayVariables)
# File uploader allows user to add their own CSV
uploaded_file = st.file_uploader("Upload your input CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the CSV data into a pandas DataFrame
    data = pd.read_csv(uploaded_file)
    if variable == "PELKM1":
        # Mapping dictionary for PELKM1
        job_search_methods = {
            1: "Contacted Employer Directly/Interview",
            2: "Contacted Public Employment Agency",
            3: "Contacted Private Employment Agency",
            4: "Contacted Friends Or Relatives",
            5: "Contacted School/University Employment Center",
            6: "Sent Out Resumes/Filled Out Application",
            7: "Checked Union/Professional Registers",
            8: "Placed Or Answered Ads",
            9: "Other Active",
            10: "Looked At Ads",
            11: "Attended Job Training Programs/Courses",
            12: "Nothing",
            13: "Other Passive",
        }
        df = pd.DataFrame(data)
        df = df[['PELKM1']]
        df["PELKM1"] = df["PELKM1"].map(job_search_methods)
        test = pd.DataFrame(df["PELKM1"])
        test["count"] = 1
        grouped_data =test.groupby('PELKM1').sum()
        # Display the plot
        st.write(f"### Unemployed looking-search methods", grouped_data)
    elif variable =="PELKAVL":
        job_search_methods = {"1": "Yes", "2": "No"}
        df["PELKAVL"] = df["PELKAVL"].map(job_search_methods)
        test = pd.DataFrame(df["PELKAVL"])
        test["count"] = 1
        # Perform grouping
        # grouped_data =test.groupby('PELKAVL').sum()
        test.groupby("PELKAVL").sum().rename(columns={"PELKAVL": "test1"})
        # Display the plot
        st.write(f"### Unemployed available for work last week", test)
    elif variable == "PELKDUR":
        st.write("not ready yet")
    elif variable == "PELKFTO":
        st.write("not ready yet")
    elif variable == "PELKLL1O":
        st.write("not ready yet")
    elif variable == "PLKLL2O":
        st.write("not ready yet")
    elif variable == "PELKLWO":
        st.write("not ready yet")
    else:
        st.write("Column 'PELKM1' does not exist in DataFrame.")
else:
    st.write("Received data is empty or malformed.")
