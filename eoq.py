import streamlit as st
import numpy as np
from scipy.stats import norm

st.title("EOQ & Reorder Point Calculator")

D = st.number_input("Annual Demand (D)", value=10000)
S = st.number_input("Ordering Cost (S)", value=500)
C = st.number_input("Unit Cost (C)", value=50)
h_rate = st.number_input("Holding Cost Rate (%)", value=20)/100
lead_time = st.number_input("Lead Time (periods)", value=5)
mean_demand = st.number_input("Mean Demand per Period", value=40)
std_dev = st.number_input("Std Deviation of Demand", value=10)
service_level = st.number_input("Service Level (0-1)", value=0.95)

H = h_rate * C
EOQ = np.sqrt((2 * D * S) / H)

Z = norm.ppf(service_level)
sigma_LT = std_dev * np.sqrt(lead_time)
safety_stock = Z * sigma_LT
ROP = (mean_demand * lead_time) + safety_stock

st.subheader("Results")
st.write("EOQ:", round(EOQ,2))
st.write("Safety Stock:", round(safety_stock,2))
st.write("Reorder Point:", round(ROP,2))
