import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('cbecs2018_final_public.csv')  # Update filename to match actual file

df = load_data()

# Dashboard setup
st.set_page_config(layout="wide", page_title="CBECS 2018 Explorer")

# Sidebar filters
st.sidebar.header("Filters")
selected_region = st.sidebar.selectbox("Region", options=df['REGION'].unique())
building_types = st.sidebar.multiselect("Building Type", options=df['PBA'].unique())

# Apply filters
filtered_df = df.copy()
if selected_region:
    filtered_df = filtered_df[filtered_df['REGION'] == selected_region]
if building_types:
    filtered_df = filtered_df[filtered_df['PBA'].isin(building_types)]

# Title
st.title("🏢 Commercial Buildings Energy Consumption Survey (CBECS) 2018")

# Overview metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Buildings", len(filtered_df))
col2.metric("Avg Energy Intensity", f"{filtered_df['MFUSED'].mean()/filtered_df['SQFT'].mean():.1f} BTU/sqft")
col3.metric("Most Common Type", filtered_df['PBA'].mode()[0] if not filtered_df.empty else "N/A")

# Building Types and Sizes
st.header("🏗️ Building Types and Sizes")

bldg_sqft = filtered_df.groupby('PBA')['SQFT'].sum().sort_values(ascending=False)
fig1 = px.bar(
    x=bldg_sqft.values,
    y=bldg_sqft.index,
    orientation='h',
    labels={'x': 'Total Square Footage', 'y': 'Building Type'},
    title="Total Floor Area by Building Type"
)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("🏢 Number of Buildings by Type")
bldg_count = filtered_df['PBA'].value_counts()
fig2 = px.bar(
    x=bldg_count.values,
    y=bldg_count.index,
    orientation='h',
    labels={'x': 'Number of Buildings', 'y': 'Building Type'}
)
st.plotly_chart(fig2, use_container_width=True)

# Energy consumption patterns
st.header("⚡ Energy Consumption Patterns")
energy_cols = ['ELUSED', 'NGUSED', 'FKUSED', 'PRUSED', 'STUSED']
energy_df = filtered_df[energy_cols].sum()
fig3 = px.bar(energy_df, x=energy_df.index, y=energy_df.values, labels={'x': 'Energy Type', 'y': 'Total Usage'})
st.plotly_chart(fig3, use_container_width=True)

# Energy efficiency benchmarking
st.header("📉 Energy Efficiency Benchmarking")
filtered_df['ENERGY_INTENSITY'] = filtered_df['MFUSED'] / filtered_df['SQFT']
fig4 = px.scatter(
    filtered_df,
    x='SQFT',
    y='ENERGY_INTENSITY',
    color='PBA',
    hover_name='PUBID',
    log_x=True,
    labels={'SQFT': 'Building Size (sqft)', 'ENERGY_INTENSITY': 'Energy Intensity (BTU/sqft)'}
)
st.plotly_chart(fig4, use_container_width=True)

# HVAC Systems analysis
st.header("🌡️ HVAC Systems Analysis")
hvac_cols = ['PKGHT', 'BOILER', 'FURNAC', 'HTPMPH']
hvac_df = filtered_df[hvac_cols].sum()
fig5 = px.bar(
    x=hvac_df.values,
    y=hvac_df.index,
    orientation='h',
    labels={'x': 'Count', 'y': 'HVAC System Type'},
    title='Distribution of HVAC Systems'
)
st.plotly_chart(fig5, use_container_width=True)

# Data table
st.header("🧾 Data Explorer")
st.dataframe(filtered_df.head(100))
