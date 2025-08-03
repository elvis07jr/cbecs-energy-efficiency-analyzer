import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor

# Page Configuration
st.set_page_config(
    page_title="CBECS 2018 Energy Explorer",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
    }
    .section-header {
        font-size: 1.8rem;
        color: #2c3e50;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    .filter-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .empty-data-message {
        padding: 1rem;
        background-color: #fff3cd;
        border-radius: 0.5rem;
        border-left: 5px solid #ffc107;
        margin: 1rem 0;
    }
    .filter-help {
        font-size: 0.9rem;
        color: #6c757d;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('cbecs2018_final_public.csv')
    # Data cleaning and preprocessing
    df = df.replace([999, 9999, 99999], np.nan)  # Replace missing value codes
    df['ENERGY_INTENSITY'] = df['MFUSED'] / df['SQFT']  # Calculate energy intensity
    df['AGE'] = 2018 - df['YRCONC']  # Building age
    return df

df = load_data()

# Create comprehensive mappings that include all values in the dataset
def create_mapping(data, column, base_mapping):
    """Create a mapping that includes all values in the dataset"""
    mapping = base_mapping.copy()
    for value in data[column].dropna().unique():
        if value not in mapping:
            mapping[value] = f"Unknown ({value})"
    return mapping

# Base mappings
base_regions = {
    1: "Northeast", 2: "Midwest", 3: "South", 4: "West"
}

base_building_types = {
    1: "Vacant", 2: "Office", 3: "Laboratory", 4: "Nonrefrigerated warehouse",
    5: "Food sales", 6: "Public order and safety", 7: "Outpatient health care",
    8: "Refrigerated warehouse", 9: "Religious worship", 10: "Public assembly",
    11: "Education", 12: "Food service", 13: "Inpatient health care",
    14: "Nursing", 15: "Lodging", 16: "Retail (other than mall)", 17: "Service",
    18: "Enclosed mall", 19: "Strip mall", 20: "Other"
}

# Create comprehensive mappings
regions = create_mapping(df, 'REGION', base_regions)
building_types = create_mapping(df, 'PBA', base_building_types)

# Sidebar Filters
st.sidebar.markdown("## 📊 Dashboard Filters")
st.sidebar.markdown("---")

# Add a reset button
if st.sidebar.button("Reset All Filters"):
    st.experimental_rerun()

with st.sidebar.expander("🏢 Building Characteristics", expanded=True):
    # Region filter with data validation
    available_regions = [regions[r] for r in df['REGION'].dropna().unique()]
    selected_regions = st.multiselect(
        "Region",
        options=available_regions,
        default=available_regions,
        help="Select one or more regions to include in the analysis"
    )
    
    # Building type filter with data validation
    available_building_types = [building_types[b] for b in df['PBA'].dropna().unique()]
    selected_building_types = st.multiselect(
        "Building Type",
        options=available_building_types,
        default=available_building_types,
        help="Select one or more building types to include in the analysis"
    )
    
    # Size range with data validation
    min_sqft = int(df['SQFT'].min())
    max_sqft = int(df['SQFT'].max())
    size_range = st.slider(
        "Building Size (sq ft)",
        min_value=min_sqft,
        max_value=max_sqft,
        value=(min_sqft, max_sqft),
        step=1000,
        help="Filter buildings by size range"
    )
    
    # Age range with data validation
    min_age = int(df['AGE'].min())
    max_age = int(df['AGE'].max())
    age_range = st.slider(
        "Building Age (years)",
        min_value=min_age,
        max_value=max_age,
        value=(min_age, max_age),
        step=5,
        help="Filter buildings by age range"
    )

with st.sidebar.expander("⚡ Energy Systems", expanded=False):
    # HVAC filters are simplified since they don't affect the main data filtering
    st.markdown("HVAC system filters coming soon!")

with st.sidebar.expander("🌍 Location & Climate", expanded=False):
    # Climate zone filter with data validation
    available_climate_zones = sorted(df['PUBCLIM'].dropna().unique())
    climate_zones = st.multiselect(
        "Climate Zone",
        options=available_climate_zones,
        default=available_climate_zones,
        help="Select one or more climate zones"
    )
    
    # Census division filter with data validation
    available_divisions = sorted(df['CENDIV'].dropna().unique())
    divisions = st.multiselect(
        "Census Division",
        options=available_divisions,
        default=available_divisions,
        help="Select one or more census divisions"
    )

# Filter helper function
def filter_data(df, selected_regions, selected_building_types, size_range, age_range, climate_zones, divisions):
    """Apply filters to the dataset with proper error handling"""
    try:
        # Convert selected names back to codes
        region_codes = [r for r, name in regions.items() if name in selected_regions]
        building_type_codes = [b for b, name in building_types.items() if name in selected_building_types]
        
        # Apply filters
        filtered = df[
            (df['REGION'].isin(region_codes)) &
            (df['PBA'].isin(building_type_codes)) &
            (df['SQFT'].between(size_range[0], size_range[1])) &
            (df['AGE'].between(age_range[0], age_range[1])) &
            (df['PUBCLIM'].isin(climate_zones)) &
            (df['CENDIV'].isin(divisions))
        ]
        
        return filtered
    except Exception as e:
        st.error(f"Error applying filters: {str(e)}")
        return pd.DataFrame()

# Apply filters
filtered_df = filter_data(
    df, selected_regions, selected_building_types, 
    size_range, age_range, climate_zones, divisions
)

# Main Dashboard
st.markdown('<h1 class="main-header">Commercial Buildings Energy Consumption Survey (CBECS) 2018</h1>', unsafe_allow_html=True)

# Check if filtered data is empty
if filtered_df.empty:
    st.markdown("""
    <div class="empty-data-message">
        <h3>⚠️ No data matches your selected filters</h3>
        <p>Please try the following:</p>
        <ul>
            <li>Click the "Reset All Filters" button in the sidebar</li>
            <li>Broaden your filter criteria (especially size and age ranges)</li>
            <li>Select more regions or building types</li>
            <li>Check that your selected climate zones and divisions exist in the data</li>
        </ul>
        <p><strong>Current filter status:</strong></p>
        <ul>
            <li>Selected regions: {}</li>
            <li>Selected building types: {}</li>
            <li>Size range: {} to {} sq ft</li>
            <li>Age range: {} to {} years</li>
            <li>Climate zones: {}</li>
            <li>Census divisions: {}</li>
        </ul>
    </div>
    """.format(
        selected_regions, selected_building_types, 
        size_range[0], size_range[1], age_range[0], age_range[1],
        climate_zones, divisions
    ), unsafe_allow_html=True)
    
    # Show data summary to help user understand available data
    st.subheader("Data Summary")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Available Regions:**")
        for region in available_regions:
            st.write(f"- {region}")
    
    with col2:
        st.markdown("**Available Building Types:**")
        for btype in available_building_types:
            st.write(f"- {btype}")
    
    st.markdown("**Size Range:** {} to {} sq ft".format(min_sqft, max_sqft))
    st.markdown("**Age Range:** {} to {} years".format(min_age, max_age))
    
    st.stop()

# Key Metrics
st.markdown("## 📈 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Total Buildings", f"{len(filtered_df):,}")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    avg_intensity = filtered_df['ENERGY_INTENSITY'].mean()
    st.metric("Avg Energy Intensity", f"{avg_intensity:.1f} BTU/sqft")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    total_energy = filtered_df['MFUSED'].sum() / 1e9  # Convert to billion BTU
    st.metric("Total Energy Use", f"{total_energy:.1f} B BTU")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    avg_sqft = filtered_df['SQFT'].mean()
    st.metric("Avg Building Size", f"{avg_sqft:,.0f} sqft")
    st.markdown('</div>', unsafe_allow_html=True)

# Building Characteristics Section
st.markdown('<h2 class="section-header">🏢 Building Characteristics</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Building Type Distribution
    building_counts = filtered_df['PBA'].value_counts().reset_index()
    building_counts.columns = ['PBA', 'count']
    building_counts['Building Type'] = building_counts['PBA'].map(building_types)
    
    if not building_counts.empty:
        fig = px.sunburst(
            building_counts,
            path=['Building Type'],
            values='count',
            title="Building Type Distribution",
            height=500
        )
        fig.update_layout(margin=dict(t=50, l=0, r=0, b=0))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.markdown('<div class="empty-data-message">⚠️ No building type data available</div>', unsafe_allow_html=True)

with col2:
    # Building Size Distribution
    if not filtered_df['SQFT'].isna().all():
        fig = px.histogram(
            filtered_df,
            x='SQFT',
            nbins=50,
            title="Building Size Distribution",
            labels={'SQFT': 'Square Feet'},
            color_discrete_sequence=['#3498db']
        )
        fig.update_layout(xaxis_type="log")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.markdown('<div class="empty-data-message">⚠️ No building size data available</div>', unsafe_allow_html=True)

# Energy Consumption Analysis
st.markdown('<h2 class="section-header">⚡ Energy Consumption Analysis</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Energy Source Breakdown
    energy_sources = ['ELUSED', 'NGUSED', 'FKUSED', 'PRUSED', 'STUSED']
    energy_labels = ['Electricity', 'Natural Gas', 'Fuel Oil', 'Propane', 'Steam']
    
    if not filtered_df[energy_sources].isna().all().all():
        energy_data = filtered_df[energy_sources].sum()
        energy_df = pd.DataFrame({
            'Energy Type': energy_labels,
            'Consumption (Billion BTU)': energy_data / 1e9
        })
        
        fig = px.bar(
            energy_df,
            x='Energy Type',
            y='Consumption (Billion BTU)',
            title="Energy Source Breakdown",
            color='Energy Type',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.markdown('<div class="empty-data-message">⚠️ No energy consumption data available</div>', unsafe_allow_html=True)

with col2:
    # Energy Intensity by Building Type
    if not filtered_df['ENERGY_INTENSITY'].isna().all():
        intensity_by_type = filtered_df.groupby('PBA')['ENERGY_INTENSITY'].mean().reset_index()
        intensity_by_type['Building Type'] = intensity_by_type['PBA'].map(building_types)
        intensity_by_type = intensity_by_type.dropna().sort_values('ENERGY_INTENSITY', ascending=False)
        
        if not intensity_by_type.empty:
            fig = px.bar(
                intensity_by_type,
                x='Building Type',
                y='ENERGY_INTENSITY',
                title="Energy Intensity by Building Type",
                labels={'ENERGY_INTENSITY': 'BTU/sqft'},
                color='ENERGY_INTENSITY',
                color_continuous_scale='Viridis'
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown('<div class="empty-data-message">⚠️ No energy intensity data available</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="empty-data-message">⚠️ No energy intensity data available</div>', unsafe_allow_html=True)

# Regional Analysis
st.markdown('<h2 class="section-header">🗺️ Regional Analysis</h2>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    # Regional Energy Consumption
    if not filtered_df['MFUSED'].isna().all():
        regional_energy = filtered_df.groupby('REGION')['MFUSED'].sum().reset_index()
        regional_energy['Region'] = regional_energy['REGION'].map(regions)
        regional_energy['Energy (Billion BTU)'] = regional_energy['MFUSED'] / 1e9
        
        fig = px.bar(
            regional_energy,
            x='Region',
            y='Energy (Billion BTU)',
            title="Total Energy Consumption by Region",
            color='Region',
            color_discrete_sequence=px.colors.qualitative.Set1
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.markdown('<div class="empty-data-message">⚠️ No regional energy data available</div>', unsafe_allow_html=True)

with col2:
    # Regional Building Count
    regional_count = filtered_df['REGION'].value_counts().reset_index()
    regional_count.columns = ['REGION', 'count']
    regional_count['Region'] = regional_count['REGION'].map(regions)
    
    if not regional_count.empty:
        fig = px.pie(
            regional_count,
            values='count',
            names='Region',
            title="Building Distribution by Region"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.markdown('<div class="empty-data-message">⚠️ No regional building count data available</div>', unsafe_allow_html=True)

# Data Explorer
st.markdown('<h2 class="section-header">🔍 Data Explorer</h2>', unsafe_allow_html=True)

st.markdown("### Filtered Data Sample")
st.dataframe(
    filtered_df.head(100),
    use_container_width=True,
    height=400
)

st.markdown("### Data Summary")
st.write(filtered_df.describe())

# Download Button
st.markdown("### Download Filtered Data")
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name='cbecs_filtered_data.csv',
    mime='text/csv'
)

# Footer
st.markdown("---")
st.markdown(
    "CBECS 2018 Energy Explorer | Data Source: U.S. Energy Information Administration | "
    "Dashboard created with Streamlit"
)