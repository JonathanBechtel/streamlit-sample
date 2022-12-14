"""Base file for the streamlit app.  To run, navigate to command line and 
run command `streamlit run app.py` in this file's directory"""
import streamlit as st
from sqlalchemy import create_engine
from datetime import date
import pandas as pd
import numpy as np
import plotly.express as px
import pickle
import json
import requests

### Helper Functions to load in data
### @st.cache stores values returned from function calls with same argument values
def load_engine():
    return create_engine('sqlite:///data/data.db')


@st.cache
def load_data(ticker, start_date, end_date):
    """Function load data from database"""
    if ticker == 'All':
        query = f"""SELECT ticker, date, value, prediction, error, data FROM preds WHERE date >= '{start_date}' AND date <= '{end_date}'"""
    else:
        query = f"""SELECT ticker, date, value, prediction, error, data FROM preds WHERE ticker = '{ticker}' AND 
        date >= '{start_date}' AND date <= '{end_date}'"""
        
    # load in data according to engine
    engine = load_engine()
    with engine.connect() as connection:
        data = pd.read_sql_query(query, con = connection, parse_dates = ['date'])
        
    return data


@st.cache(allow_output_mutation = True)
def chart_predictions(ticker, data):
    """Function to display chart of predictions vs actual results for validation & test data"""
    title = f"""Predicted vs. Actual values for: {ticker} 
    from: {data.date.min().strftime('%Y-%m-%d')} to {data.date.max().strftime('%Y-%m-%d')}"""
    
    if ticker != 'All':
        return px.line(data, x = 'date', y = ['value', 'prediction'], title = title)
    return px.line(data, x = 'date', 
                   y = ['value', 'prediction'], 
                   title = title,
                   height = 750,
                   width = 900,
                   facet_row = 'ticker')

@st.cache
def calc_metrics(res_df):
    res = {}
    
    # calc r-squared
    mean = np.mean((res_df['value'] - res_df['value'].mean())**2)
    mod  = np.mean((res_df['value'] - res_df['prediction'])**2)
    res['r_square'] = 1 - (mod / mean)
    
    # mape
    abs_err          = (np.abs(res_df['value'] - res_df['prediction'])) / np.abs(res_df['value'])
    res['mape']      = abs_err[abs_err < np.inf].mean()
    
    # rmse
    res['rmse']      = np.sqrt(mod)
    
    # sign
    res['direction'] = np.mean(np.sign(res_df['value']) == np.sign(res_df['prediction']))
    
    return res

@st.cache
def format_table(data):
    """Calculates four different error metrics for training & validation data"""
    index = []
    rows  = []
    val_d  = data.loc[data.data == 'validation'].copy()
    test_d = data.loc[data.data == 'test'].copy()
    if len(val_d) > 0:
        rows.append(calc_metrics(val_d))
        index.append('validation')
    if len(test_d) > 0:
        rows.append(calc_metrics(test_d))
        index.append('test')
        
    return pd.DataFrame(rows, index = index)

@st.cache
def load_model():
    with open('models/mod.pickle', 'rb') as mod:
        gbm = pickle.load(mod)
        
    return gbm


# sidebar inputs for user inputs
st.title("Data Application for Monthly Market Returns")
section = st.sidebar.selectbox("Section", ['Model Explorer', 'Live Model', 'API'])

# load in the data from the inputs
if section == 'Model Explorer':
    ticker = st.sidebar.selectbox("Select Ticker", ['All', 'MSFT', 'GOOG', 'FB', 'AAPL', 'AMZN'])
    start  = st.sidebar.date_input("Start Date", date(2010, 1, 1))
    end    = st.sidebar.date_input("End Date", date.today())
    data           = load_data(ticker, start, end)
    chart          = chart_predictions(ticker, data)
    results_table  = format_table(data) 
    st.write(data)
    st.plotly_chart(chart)
    st.text("Model Results")
    st.write(results_table)
    
elif section == 'Live Model':
    file = st.file_uploader('Upload File With Model Predictions Here')
    if file is not None:
        st.text("Uploaded File Contents")
        inputs = pd.read_csv(file)
        st.write(inputs)
        
        # way to check if a button is clicked or not
        if st.button("Get Predictions"):
            url     =  'http://127.0.0.1:5000/.com:5000/predict'
            payload = json.dumps(inputs.values.tolist())
            resp    = requests.post(url, json = {'arr': payload})
            try:    
                st.write(np.array(resp.json()))
            except Exception as e:
                st.text(f"Could not process request because: {e}")
                
else:
    st.header("Connect to the Model API")
    st.text("You can connect to the model API at the following URL:")
    st.code("http://ec2-44-200-166-44.compute-1.amazonaws.com:5000/predict")
    st.text("Example code you can use can be seen here: ")
    code = """
    sample = [['AMZN', 0.17, -.21, -.1, .06, .04, .091, 1]]
    url = 'http://ec2-44-200-166-44.compute-1.amazonaws.com:5000/predict'
    json_sample = json.dumps(sample)
    payload     = {'arr': json_sample}
    resp        = requests.post(url, json = payload)
    """
    st.code(code, language = "python")