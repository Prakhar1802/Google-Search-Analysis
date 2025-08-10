# streamlit_app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from pytrends.request import TrendReq

# Streamlit page config
st.set_page_config(page_title="Google Trends Analysis", layout="wide")

# Title
st.title("Google Trends Analysis Dashboard")

# Sidebar for input
st.sidebar.header("Search Settings")
keyword = st.sidebar.text_input("Enter a keyword:", "machine learning")
timeframe = st.sidebar.selectbox("Select timeframe:",
                                 ["today 12-m", "today 3-m", "today 5-y", "all"])
geo = st.sidebar.text_input("Geo code (leave empty for worldwide):", "")

# Initialize Pytrends
pytrends = TrendReq(hl='en-US', tz=360)

# Build initial payload
pytrends.build_payload(kw_list=[keyword], cat=0, timeframe=timeframe, geo=geo, gprop='')

# ------------------------
# Country-wise interest
# ------------------------
region_data = pytrends.interest_by_region()
region_data = region_data.sort_values(by=keyword, ascending=False).head(15)

st.subheader(f"Top Countries Searching for '{keyword}'")
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=region_data[keyword], y=region_data.index, palette="crest", ax=ax)
ax.set_title(f"Top Countries searching for {keyword}")
ax.set_xlabel("Interest")
ax.set_ylabel("Countries")
st.pyplot(fig)

# World map
region_data_reset = region_data.reset_index()
fig_map = px.choropleth(region_data_reset,
                        locationmode="country names",
                        locations="geoName",
                        color=keyword,
                        title=f"{keyword.capitalize()} Interest by Country",
                        color_continuous_scale="Blues")
st.plotly_chart(fig_map, use_container_width=True)

# ------------------------
# Interest over time
# ------------------------
st.subheader(f"📈 Interest Over Time for '{keyword}'")
time_df = pytrends.interest_over_time()
fig_line = px.line(time_df, x=time_df.index, y=keyword,
                   title=f"{keyword.capitalize()} interest over time",
                   color_discrete_sequence=["blue"])
fig_line.update_layout(
    xaxis=dict(showgrid=True, gridcolor='lightgrey'),
    yaxis=dict(showgrid=True, gridcolor='lightgrey')
)
st.plotly_chart(fig_line, use_container_width=True)

# ------------------------
# Multiple keyword comparison (dynamic)
# ------------------------
st.subheader("🔍 Related Keywords Comparison")

# Get related queries
pytrends.build_payload(kw_list=[keyword], cat=0, timeframe=timeframe, geo=geo, gprop='')
related_queries = pytrends.related_queries()
top_related_df = related_queries[keyword]['top']

if top_related_df is not None:
    top_keywords_list = top_related_df['query'].tolist()
    comparison_keywords = [keyword] + [kw for kw in top_keywords_list if kw.lower() != keyword.lower()][:4]
else:
    comparison_keywords = [keyword]

st.write("**Comparison Keywords:**", comparison_keywords)

# Get interest over time for comparison keywords
pytrends.build_payload(kw_list=comparison_keywords, cat=0, timeframe=timeframe, geo=geo, gprop='')
comparison_df = pytrends.interest_over_time()

# Plot comparison chart
fig_compare = px.line(comparison_df, x=comparison_df.index, y=comparison_df.columns[:-1],
                      title=f"Interest Over Time for Keywords Related to '{keyword}'")
fig_compare.update_layout(
    xaxis=dict(showgrid=True, gridcolor='lightgrey'),
    yaxis=dict(showgrid=True, gridcolor='lightgrey')
)
st.plotly_chart(fig_compare, use_container_width=True)
