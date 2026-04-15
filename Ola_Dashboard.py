import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# --------------------------
# FORMAT FUNCTION (INDIAN SYSTEM)
# --------------------------
def format_indian(num):
    num = int(num)
    s = str(num)
    if len(s) <= 3:
        return s
    else:
        last3 = s[-3:]
        rest = s[:-3]
        rest = ",".join([rest[max(i-2,0):i] for i in range(len(rest), 0, -2)][::-1])
        return rest + "," + last3

# --------------------------
# LOAD DATA
# --------------------------
df = pd.read_csv("Ola_data_Clean.csv")

df['Date'] = pd.to_datetime(df['Date'])
df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce')
df['Ride_Distance'] = pd.to_numeric(df['Ride_Distance'], errors='coerce')

# FIX DAY ORDER
day_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
df['Day'] = pd.Categorical(df['Day'], categories=day_order, ordered=True)

# --------------------------
# SIDEBAR
# --------------------------
st.sidebar.title("Filters")

vehicle = st.sidebar.multiselect("Vehicle", df['Vehicle_Type'].unique())
payment = st.sidebar.multiselect("Payment", df['Payment_Method'].unique())

filtered = df.copy()

if vehicle:
    filtered = filtered[filtered['Vehicle_Type'].isin(vehicle)]

if payment:
    filtered = filtered[filtered['Payment_Method'].isin(payment)]

# --------------------------
# NAVIGATION
# --------------------------
page = st.sidebar.radio("Navigation", [
    "Business Overview",
    "Revenue Drivers",
    "Risk & Quality"
])

# =====================================================
# PAGE 1
# =====================================================
if page == "Business Overview":

    st.title("Ola Business Performance")

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Revenue", f"₹ {format_indian(filtered['Revenue'].sum())}")
    c2.metric("Total Rides", format_indian(len(filtered)))
    c3.metric("Avg Distance", f"{filtered['Ride_Distance'].mean():.2f}")

    col1, col2 = st.columns(2)

    # Revenue Source
    st.subheader("Business Question: Where is revenue coming from?")

    payment_data = filtered.groupby('Payment_Method')['Revenue'].sum().reset_index()

    fig1 = px.pie(payment_data, names='Payment_Method', values='Revenue', hole=0.6)
    fig1.update_layout(template="plotly_dark")

    col1.plotly_chart(fig1, use_container_width=True)

    # Demand Trend
    st.subheader("Is demand stable or fluctuating?")

    trend = filtered.groupby('Date').size().reset_index(name='Rides')

    fig2 = px.line(trend, x='Date', y='Rides')
    fig2.update_layout(template="plotly_dark")

    col2.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    **Insight**
    - Revenue is concentrated in limited payment methods → dependency risk  
    - Demand fluctuates across days → unstable pattern  

    **Recommendation**
    - Push digital payments with incentives  
    - Apply surge pricing during peak demand  
    """)

# =====================================================
# PAGE 2
# =====================================================
elif page == "Revenue Drivers":

    st.title("Revenue Drivers Analysis")

    # Vehicle Revenue
    st.subheader("Which vehicle types drive revenue?")

    vehicle_data = filtered.groupby('Vehicle_Type')['Revenue'].sum().reset_index()

    fig3 = px.bar(vehicle_data, x='Revenue', y='Vehicle_Type', orientation='h')
    fig3.update_layout(template="plotly_dark")

    st.plotly_chart(fig3, use_container_width=True)

    # Day Revenue (FIXED ORDER)
    st.subheader("Which days generate highest revenue?")

    day_data = filtered.groupby('Day')['Revenue'].sum().reset_index()

    fig4 = px.bar(day_data, x='Day', y='Revenue',
                  category_orders={"Day": day_order})
    fig4.update_layout(template="plotly_dark")

    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("""
    **Insight**
    - Premium vehicle segments generate higher revenue  
    - Revenue peaks on specific days → demand concentration  

    **Recommendation**
    - Increase availability of high-performing vehicle types  
    - Allocate drivers strategically on peak days  
    """)

# =====================================================
# PAGE 3
# =====================================================
elif page == "Risk & Quality":

    st.title("Risk & Customer Experience")

    # FILTER ONLY CANCELLED (FIXED)
    cancel_data = filtered[
        filtered['Canceled_Rides_by_Driver'].notna() &
        (filtered['Canceled_Rides_by_Driver'] != "Not Cancelled")
    ]

    st.subheader("Why are drivers cancelling rides?")

    cancel_reason = cancel_data['Canceled_Rides_by_Driver'].value_counts().reset_index()
    cancel_reason.columns = ['Reason', 'Count']

    fig5 = px.bar(cancel_reason, x='Reason', y='Count')
    fig5.update_layout(template="plotly_dark")

    st.plotly_chart(fig5, use_container_width=True)

    # Ratings (clean)
    st.subheader("Customer vs Driver Ratings (Segment View)")

    rating = filtered.groupby('Vehicle_Type')[['Customer_Rating','Driver_Ratings']].mean().reset_index()

    fig6 = px.scatter(
        rating,
        x='Customer_Rating',
        y='Driver_Ratings',
        size=[20]*len(rating),
        color='Vehicle_Type'
    )

    fig6.update_layout(template="plotly_dark")

    st.plotly_chart(fig6, use_container_width=True)

    st.markdown("""
    **Insight**
    - Majority cancellations are operational (driver/car issues)  
    - Customer-related issues also contribute but less significantly  

    **Recommendation**
    - Improve driver reliability tracking  
    - Penalize repeated cancellations  
    - Optimize driver allocation system  
    """)
