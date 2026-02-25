import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

st.set_page_config(page_title="Inventory Order Quantity Optimisation Toolkit", layout="wide")

st.title("📦 Inventory Optimization Toolkit")
st.markdown("Built for Supply Chain Analytics")

# ---- Z VALUE TABLE ----
z_table = {
    0.80: 0.84,
    0.85: 1.04,
    0.90: 1.28,
    0.95: 1.65,
    0.97: 1.88,
    0.98: 2.05,
    0.99: 2.33
}

# ---- MODEL SELECTION ----
model = st.sidebar.selectbox(
    "Select Inventory Model",
    ["EOQ (Deterministic)",
     "EOQ with Safety Stock",
     "EOQ with Stock Out",
     "EOQ with Back Order",
     "Newsvendor Model"]
)

# ============================================================
# EOQ MODEL 1
# ============================================================

if model == "EOQ (Deterministic)":

    st.header("Economic Order Quantity (EOQ)")

    D = st.sidebar.number_input("Annual Demand (D)", value=24000)
    S = st.sidebar.number_input("Ordering Cost per Order (S)", value=1200)
    C = st.sidebar.number_input("Unit Cost (C)", value=500)
    h_rate = st.sidebar.number_input("Holding Cost Rate (%)", value=18)/100

    H = h_rate * C
    EOQ = np.sqrt((2 * D * S) / H)
    total_cost = (D/EOQ)*S + (EOQ/2)*H
    orders_per_year = D / EOQ

    col1, col2 = st.columns(2)

    col1.metric("EOQ", round(EOQ,2))
    col1.metric("Orders per Year", round(orders_per_year,2))
    col2.metric("Total Annual Cost", round(total_cost,2))

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

# ============================================================
# EOQ WITH SAFETY STOCK
# ============================================================

elif model == "EOQ with Safety Stock":

    st.header("EOQ with Safety Stock & Reorder Point")

    D = st.sidebar.number_input("Annual Demand (D)", value=24000)
    S = st.sidebar.number_input("Ordering Cost per Order (S)", value=1200)
    C = st.sidebar.number_input("Unit Cost (C)", value=500)
    h_rate = st.sidebar.number_input("Holding Cost Rate (%)", value=18)/100

    lead_time = st.sidebar.number_input("Lead Time (periods)", value=2)
    mean_demand = st.sidebar.number_input("Mean Demand per Period  (d)", value=460)
    std_dev = st.sidebar.number_input("Std Dev of Demand per Period (Std)", value=120)

    service_level = st.sidebar.selectbox(
        "Service Level",
        options=list(z_table.keys()),
        index=3
    )

    Z = z_table[service_level]

    H = h_rate * C
    EOQ = np.sqrt((2 * D * S) / H)

    sigma_LT = std_dev * np.sqrt(lead_time)
    safety_stock = Z * sigma_LT
    ROP = (mean_demand * lead_time) + safety_stock

    total_cost = (D/EOQ)*S + (EOQ/2)*H

    col1, col2 = st.columns(2)

    col1.metric("EOQ", round(EOQ,2))
    col1.metric("Safety Stock", round(safety_stock,2))
    col1.metric("Reorder Point (ROP)", round(ROP,2))

    col2.metric("Total Annual Cost", round(total_cost,2))

# ============================================================
# EOQ WITH STOCK OUT
# ============================================================

elif model == "EOQ with Stock Out":

    st.header("EOQ with Stock Out")

    D = st.sidebar.number_input("Annual Demand (D)", value=24000)
    S = st.sidebar.number_input("Ordering Cost per Order (S)", value=1200)
    C = st.sidebar.number_input("Unit Cost (C)", value=500)
    h_rate = st.sidebar.number_input("Holding Cost Rate (%)", value=18)/100
    pi = st.sidebar.number_input("Stock Out Cost per cycle (g)", value=250)

    lead_time = st.sidebar.number_input("Lead Time (periods)", value=2)
    std_dev = st.sidebar.number_input("Std Dev of Demand (Std)", value=120)

    service_level = st.sidebar.selectbox(
        "Service Level",
        options=list(z_table.keys()),
        index=3
    )

    Z = z_table[service_level]
    sigma_LT = std_dev * np.sqrt(lead_time)

    H = h_rate * C

    phi = norm.pdf(Z)
    Phi = norm.cdf(Z)
    Ez = phi - Z * (1 - Phi) 
    g = sigma_LT * Ez
        
    EOQ = np.sqrt((2 * D * (S+g*pi)) / H)
   
   
    total_cost = (D/EOQ)*S + (EOQ/2)*H + (D/EOQ)*g*pi
    G = g * pi
    col1, col2 = st.columns(2)

    col1.metric("EOQ", round(EOQ,2))
    col1.metric("Shortage per cycle", round(g,2))

    col2.metric("Total Annual Cost", round(total_cost,2))
    col2.metric("Shortage Cost per cycle, G", round(G,2))

# ============================================================
# EOQ WITH BACK ORDER
# ============================================================

elif model == "EOQ with Back Order":

    st.header("EOQ with back Order")

    D = st.sidebar.number_input("Annual Demand (D)", value=24000)
    S = st.sidebar.number_input("Ordering Cost per Order (S)", value=1200)
    C = st.sidebar.number_input("Unit Cost (C)", value=500)
    h_rate = st.sidebar.number_input("Holding Cost Rate (%)", value=18)/100
    pi = st.sidebar.number_input("Back Order Cost per cycle (π)", value=250)

    service_level = st.sidebar.selectbox(
        "Service Level",
        options=list(z_table.keys()),
        index=3
    )

    H = h_rate * C  
    EOQ = (np.sqrt((2 * D * S) / H)) * (np.sqrt((H + pi) / pi))
    B = EOQ * (H/(H+pi))
    M = EOQ - B

    back_order_cost = (B/2)*((B/EOQ)*pi)
    total_cost = (D/EOQ)*S + (M/2)*(M/EOQ)*H + (B/2)*((B/EOQ)*pi)
    
    col1, col2 = st.columns(2)

    col1.metric("EOQ", round(EOQ,2))
    col1.metric("Backorder Quantity per cycle, B", round(B,2))
    col1.metric("Maximum Inventory per cycle, M", round(M,2))

    col2.metric("Total Annual Cost", round(total_cost,2))
    col2.metric("Backorder Cost per cycle, G", round(back_order_cost,2))

# ============================================================
# NEWSVENDOR MODEL
# ============================================================

elif model == "Newsvendor Model":

    st.header("Newsvendor (Single-Period) Model")

    mean_demand = st.sidebar.number_input("Mean Demand (d)", value=1000)
    std_dev = st.sidebar.number_input("Std Deviation of Demand (Std)", value=200)
    selling_price = st.sidebar.number_input("Selling Price per Unit", value=50)
    cost_price = st.sidebar.number_input("Cost per Unit", value=30)
    salvage_value = st.sidebar.number_input("Salvage Value per Unit", value=10)

    Cu = selling_price - cost_price  # Underage cost
    Co = cost_price - salvage_value  # Overage cost

    critical_ratio = Cu / (Cu + Co)

    # Find closest Z from table
    closest_service = min(z_table.keys(), key=lambda x: abs(x - critical_ratio))
    Z = z_table[closest_service]

    optimal_Q = mean_demand + Z * std_dev

    col1, col2 = st.columns(2)

    col1.metric("Critical Ratio", round(critical_ratio,3))
    col1.metric("Optimal Order Quantity", round(optimal_Q,2))

    col2.metric("Underage Cost (Cu)", round(Cu,2))
    col2.metric("Overage Cost (Co)", round(Co,2))

    st.markdown(f"Closest Service Level Used: **{closest_service}**")
