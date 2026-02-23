import streamlit as st
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

st.title("Supply Chain Analytics Model")
st.subheader("EOQ with Safety Stock & Reorder Point")

# --- INPUT SECTION ---
st.sidebar.header("Input Parameters")

D = st.sidebar.number_input("Annual Demand (D)", value=10000)
S = st.sidebar.number_input("Ordering Cost per Order (S)", value=500)
C = st.sidebar.number_input("Unit Cost (C)", value=50)
h_rate = st.sidebar.number_input("Holding Cost Rate (%)", value=20)/100
lead_time = st.sidebar.number_input("Lead Time (periods)", value=5)
mean_demand = st.sidebar.number_input("Mean Demand per Period", value=40)
std_dev = st.sidebar.number_input("Std Dev of Demand per Period", value=10)
service_level = st.sidebar.slider("Service Level", 0.80, 0.99, 0.95)

# --- CALCULATIONS ---
H = h_rate * C
EOQ = np.sqrt((2 * D * S) / H)
orders_per_year = D / EOQ
average_inventory = EOQ / 2

Z = norm.ppf(service_level)
sigma_LT = std_dev * np.sqrt(lead_time)
safety_stock = Z * sigma_LT
ROP = (mean_demand * lead_time) + safety_stock

total_cost = (D/EOQ)*S + (EOQ/2)*H

# --- OUTPUT SECTION ---
st.header("Results")

col1, col2 = st.columns(2)

col1.metric("EOQ", round(EOQ,2))
col1.metric("Reorder Point (ROP)", round(ROP,2))
col1.metric("Safety Stock", round(safety_stock,2))

col2.metric("Total Annual Cost", round(total_cost,2))
col2.metric("Orders per Year", round(orders_per_year,2))
col2.metric("Average Inventory", round(average_inventory,2))

# --- COST GRAPH ---
st.subheader("Total Cost Curve")

Q = np.linspace(EOQ*0.2, EOQ*2, 100)
TC = (D/Q)*S + (Q/2)*H

fig, ax = plt.subplots()
ax.plot(Q, TC)
ax.axvline(EOQ, linestyle="--")
ax.set_xlabel("Order Quantity")
ax.set_ylabel("Total Cost")
ax.set_title("Total Cost vs Order Quantity")

st.pyplot(fig)
