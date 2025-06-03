import streamlit as st
import plotly.express as px
from pandas import read_csv
import sqlite3
from functions import extract_data_db
from datetime import datetime

# 1. method using CSV file and data with data type lists
df = read_csv("fake_temp_data.csv", parse_dates=["date"], date_format="%y-%m-%d-%H-%M-%S")

dates, temp = df["date"], df["temperature"]
figure = px.line(x=dates, y=temp, labels={'x': 'Days', 'y': 'Temperature (C)'})
st.plotly_chart(figure, key="CSV")

# 2. method using DB file with and data with data type tuples
connection = sqlite3.connect("event_data.db")
cursor = connection.cursor()

data_db = extract_data_db("temperature")
dates2, temps2 = zip(*data_db)
date_formatted = [datetime.strptime(date, "%y-%m-%d-%H-%M-%S") for date in dates2]
figure2 = px.line(x=date_formatted, y=temps2, labels={'x': 'Days', 'y': 'Temperature (C)'})
st.plotly_chart(figure2, key="DB")
