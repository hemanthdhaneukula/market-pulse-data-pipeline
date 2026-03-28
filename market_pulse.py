import streamlit as st
import pandas as pd
import time
import requests
from datetime import datetime
from dotenv import load_dotenv
import os
from supabase import create_client
load_dotenv()
URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(URL, KEY) 
options={"schema": "public"}

st.set_page_config(page_title= "Market Pulse AI", layout= "wide")
st.title("Marlet Pulse: Real-time Crypto Imtelligence")
st.write("Fetching live data from CoinGenko API...")

#Fetching Data
def get_crypto_data():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true"
    response= requests.get(url)
    data= response.json()
    return data['bitcoin']['usd'], data['bitcoin']['usd_24h_change']

#The Transformation layer (logic)
if 'price_history' not in st.session_state:
    st.session_state.price_history=[]
price, change= get_crypto_data()
timestamp = datetime.now().strftime("%H:%M:%S")

try:
    data_to_save = {"price": price, "symbol": "BTC"}
    supabase.table("market_pulse_data").insert(data_to_save).execute()
except Exception as e:
    st.error(f"Database Error: {e}")

#Store the data point
st.session_state.price_history.append({"Time":timestamp, "Price":price})

#Keep only last 20 points for the chart
df= pd.DataFrame(st.session_state.price_history).tail(20)

#THE ANALYTICS ENGINE
sma= df["Price"].mean()
status= "BREAKOUT" if price>sma else "STABLE" 

#The VISUALIZATION LAYER (Frontend)

col1, col2, col3= st.columns(3)
col1.metric("Bitcoin price", f"${price:,}", f"{change:.2f}%")
col2.metric("20-period average", f"${sma:.2f}")
col3.metric("Market signal", status)

st.subheader("Real-time Price Volatility")
st.line_chart(df.set_index("Time"))

time.sleep(30)
st.rerun()
