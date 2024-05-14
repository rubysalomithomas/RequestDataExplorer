import streamlit as st
import pandas as pd

# Function to map ranges using dictionary
def map_score_to_category(score):
    if score > 0 and score < 6:
        return 'Less than 5 weeks'
    elif score > 6 and score < 10:
        return 'Less than 10 Weeks'
    elif score > 10:
        return 'greather than 10 weeks'


# Title of the app
st.title("CSV File to DataFrame")

VARIABLES =  {"PELKAVL":"Unemployed available for work last week", "PELKDUR":"Unemployed Number of weeks on job search", "PELKFTO":"Unemployed looking-full-time work wanted",
     "PELKLL1O":"Unemployed looking-activity before search", "PELKLL2O":"Unemployedlooking-lost/quit job", "PELKLWO":"Unemployed looking-when last worked", "PELKM1":"Unemployed looking-search methods"}
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
        df1 = df[['PELKM1']]
        df1["PELKM1"] = df1["PELKM1"].map(job_search_methods)
        test = pd.DataFrame(df1["PELKM1"])
        test["count"] = 1
        grouped_data =test.groupby('PELKM1').sum()
        # Display the plot
        st.write(f"### Unemployed looking-search methods", grouped_data)
    elif variable =="PELKAVL":
        job_search_methods = {1: "Yes", 2: "No"}
        df = pd.DataFrame(data)
        df2 = df[['PELKAVL']]
        df2["PELKAVL"] = df2["PELKAVL"].map(job_search_methods)
        test = pd.DataFrame(df2["PELKAVL"])
        test["count"] = 1
        # Perform grouping
        grouped_data =test.groupby('PELKAVL').sum()
        
        # Display the plot
        st.write(f"### Unemployed available for work last week", grouped_data)
    elif variable == "PELKDUR":
         df = pd.DataFrame(data)
         df2 = df[['PELKDUR']]
         test = pd.DataFrame(df2["PELKDUR"])
         test['Mapped_Category'] = test['PELKDUR'].apply(map_score_to_category)
         test["count"] = 1
         grouped_data =test.groupby('Mapped_Category').sum()
         st.write(f"### Unemployed no of weeks on job search", grouped_data)
    elif variable == "PELKFTO":
         method = {2: "No",
                              3: "Doesn't Matter",
                              1: "Yes"}
         df = pd.DataFrame(data)
         df2 = df[['PELKFTO']]
         df2["PELKFTO"] = df2["PELKFTO"].map(method)
         test = pd.DataFrame(df2["PELKFTO"])
         test["count"] = 1
        # Perform grouping
         grouped_data =test.groupby('PELKFTO').sum()
        
        # Display the plot
         st.write(f"### Unemployed Full time work wanted", grouped_data)
    elif variable == "PELKLL1O":
         method = {4: "Something Else",
                  2: "School",
                  1: "Working",
                  3: "Left Military Service"}
         df = pd.DataFrame(data)
         df2 = df[['PELKLL1O']]
         df2["PELKLL1O"] = df2["PELKLL1O"].map(method)
         test = pd.DataFrame(df2["PELKLL1O"])
         test["count"] = 1
        # Perform grouping
         grouped_data =test.groupby('PELKLL1O').sum()
        
        # Display the plot
         st.write(f"### Unemployed Looking activity before search", grouped_data)
    elif variable == "PELKLL2O":
         method = {2: "Quit Job",
                  1: "Lost Job",
                  3: "Temporary Job Ended"}
         df = pd.DataFrame(data)
         df2 = df[['PELKLL2O']]
         df2["PELKLL2O"] = df2["PELKLL2O"].map(method)
         test = pd.DataFrame(df2["PELKLL2O"])
         test["count"] = 1
        # Perform grouping
         grouped_data =test.groupby('PELKLL2O').sum()
        
        # Display the plot
         st.write(f"### Lost/quit job", grouped_data)
    elif variable == "PELKLWO":
         method = { 1: "Within The Last 12 Months",
                  3: "Never Worked",
                  2: "More Than 12 Months Ago"}
         df = pd.DataFrame(data)
         df2 = df[['PELKLWO']]
         df2["PELKLL2O"] = df2["PELKLWO"].map(method)
         test = pd.DataFrame(df2["PELKLWO"])
         test["count"] = 1
        # Perform grouping
         grouped_data =test.groupby('PELKLWO').sum()
        
        # Display the plot
         st.write(f"### Last worked", grouped_data)
    else:
         st.write("Column 'PELKM1' does not exist in DataFrame.")
else:
     st.write("Received data is empty or malformed.")
