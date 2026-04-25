import streamlit as st
import pandas as pd
import plotly.express as px

#Page config 
#Sets the title, icon and layout of the Streamlit app
st.set_page_config(
    page_title="European Bathing Water Quality",
    page_icon="🏖️",  #icon for visual appeal
    layout="wide"
)

#Load data
#Using @st.cache_data ensures the dataset is only loaded once
@st.cache_data
def load_data():
    df = pd.read_csv("bathing_water_clean.csv")
    return df

df = load_data()

#Sidebar filters 
#Allows users to interactively filter the dataset
st.sidebar.title("🔍 Filters")

all_countries = sorted(df['countrycode'].dropna().unique())
selected_countries = st.sidebar.multiselect(
    "Select Country", all_countries, default=all_countries[:5]  # limits default selection so UI is not overloaded
)
# Year filter (slider)
min_year = int(df['year'].min())
max_year = int(df['year'].max())
selected_year = st.sidebar.slider(
    "Select Year", min_year, max_year, max_year  # default = latest year
)
#water type filter (radio button)
water_types = df['watertype'].dropna().unique().tolist()
selected_type = st.sidebar.radio("Water Type", ["All"] + water_types)   #adds "All" option manually for flexibility

#Filter dataframe 
# Apply user selections to dataset
filtered = df[df['countrycode'].isin(selected_countries)]  #filters multiple countries
filtered_year = filtered[filtered['year'] == selected_year] #filters specific year

if selected_type != "All":
    filtered_year = filtered_year[
        filtered_year['watertype'] == selected_type
    ]

#Colour map 
# Defines consistent colours for quality categories
color_map = {
    'Excellent': '#2ecc71',
    'Good':      '#3498db',
    'Sufficient':'#f39c12',
    'Poor':      '#e74c3c'
}

#Page title 
st.title("European Bathing Water Quality Dashboard")
st.markdown("Analysing bathing water quality across Europe from **1990 to 2024**")
st.divider()

#KPI Row
#displays key summary statistics
col1, col2, col3, col4 = st.columns(4)

total_sites = len(filtered_year)
excellent = len(filtered_year[filtered_year['qualitylabel'] == 'Excellent'])
poor = len(filtered_year[filtered_year['qualitylabel'] == 'Poor'])
# Calculate percentage safely
pct_excellent = round((excellent / total_sites * 100), 1) if total_sites > 0 else 0 # avoids division by zero when no data is available

col1.metric("Total Sites", f"{total_sites:,}")
col2.metric(" Excellent", f"{excellent:,}")
col3.metric(" Poor", f"{poor:,}")
col4.metric(" % Excellent", f"{pct_excellent}%")

st.divider()

# Row 1: Quality breakdown + Water type 
col1, col2 = st.columns(2)
# Bar chart showing quality breakdown
with col1:
    st.subheader("Quality Rating Breakdown")
    quality_counts = filtered_year['qualitylabel'].value_counts().reset_index()
    quality_counts.columns = ['Quality', 'Count'] # renaming for readability in chart
    fig1 = px.bar(
        quality_counts, x='Quality', y='Count',
        color='Quality', color_discrete_map=color_map,
        title=f"Quality Ratings in {selected_year}"  #dynamic title
    )
    st.plotly_chart(fig1, use_container_width=True)
# Pie chart showing water type distribution
with col2:
    st.subheader("Coastal vs Inland vs Lake")
    type_counts = filtered_year['watertype'].value_counts().reset_index()
    type_counts.columns = ['Type', 'Count']
    fig2 = px.pie(
        type_counts, names='Type', values='Count',
        title="Water Type Distribution"
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

#Row 2: Trend over time
st.subheader("Quality Trends Over Time (1990–2024)")
# Group data to show trends by year and quality
trend = df[df['countrycode'].isin(selected_countries)]
trend = trend.groupby(      # groups data to count occurrences per year and quality category

    ['year', 'qualitylabel']
).size().reset_index(name='Count')
fig3 = px.line(
    trend, x='year', y='Count',
    color='qualitylabel',
    color_discrete_map=color_map,
    title="Bathing Water Quality Trends Over Time",
    labels={'year': 'Year', 'Count': 'Number of Sites'}
)
st.plotly_chart(fig3, use_container_width=True)

st.divider()

# Row 3: Country comparison 
st.subheader("Country Comparison")
# Aggregate quality by country
country_quality = filtered_year.groupby(
    ['countrycode', 'qualitylabel']
).size().reset_index(name='Count')
# aggregates counts for comparison between countries
fig4 = px.bar(
    country_quality,
    x='countrycode', y='Count',
    color='qualitylabel',
    color_discrete_map=color_map,
    title=f"Quality by Country in {selected_year}",
    labels={'countrycode': 'Country', 'Count': 'Number of Sites'}
)
st.plotly_chart(fig4, use_container_width=True)

st.divider()

#Row 4: Interactive Map
st.subheader("Interactive Map of Bathing Sites")
# Remove rows with missing coordinates
map_df = filtered_year.dropna(subset=['lat', 'lon'])

fig5 = px.scatter_mapbox(
    map_df,
    lat='lat', lon='lon',
    color='qualitylabel',
    color_discrete_map=color_map,
    hover_name='bathingwatername',
    hover_data=['countrycode', 'watertype', 'qualitylabel'],
    zoom=3, height=500,     # suitable zoom level for Europe-wide view
    title="Bathing Water Sites Map"
)
# Use open-source map style (no API key required)
fig5.update_layout(mapbox_style="open-street-map")
st.plotly_chart(fig5, use_container_width=True)

st.divider()

#Row 5: Search by beach name 
# Allows users to search for specific bathing locations
st.subheader("Search Beach History")
beach_search = st.text_input("Type a beach or lake name:")
if beach_search:
    results = df[df['bathingwatername'].str.contains(
        beach_search, case=False, na=False     #allows case insensitive search and avoid errors from missing values
    )]
    if len(results) > 0:
        st.dataframe(results[[
            'bathingwatername', 'countrycode',
            'year', 'qualitylabel', 'watertype'
        ]].sort_values('year'))   # sorts results chronologically
    else:
        st.warning("No beach found with that name.")
#Footer
st.divider()
st.caption("Data source: European Environment Agency (EEA) — Bathing Water Directive 1990–2024")