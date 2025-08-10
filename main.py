# --------------------------
# Import required libraries
# --------------------------
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from pytrends.request import TrendReq

# --------------------------
# 1. Initialize Pytrends API
# --------------------------
# hl='en-US' -> language & region preference
# tz=360 -> timezone offset in minutes (360 = UTC+6)
pytrends = TrendReq(hl='en-US', tz=360)

# Define the main keyword to search
keyword = "machine learning"

# --------------------------
# 2. Build initial payload
# --------------------------
# kw_list=[keyword] -> keywords to fetch data for
# cat=0 -> no specific category
# timeframe='today 12-m' -> data from last 12 months
# geo='' -> global data
# gprop='' -> Google Web Search
pytrends.build_payload(kw_list=[keyword], cat=0, timeframe='today 12-m', geo='', gprop='')

# --------------------------
# 3. Country-wise interest
# --------------------------
region_data = pytrends.interest_by_region()
region_data = region_data.sort_values(by=keyword, ascending=False).head(15)

# Plot bar chart of top countries
plt.figure(figsize=(10, 6))
sns.barplot(x=region_data[keyword], y=region_data.index, palette="crest")
plt.title(f"Top Countries searching for {keyword}")
plt.xlabel("Interest")
plt.ylabel("Countries")
plt.show()

# --------------------------
# 4. World Map view of interest
# --------------------------
region_data = region_data.reset_index()
fig = px.choropleth(region_data,
                    locationmode="country names",
                    locations="geoName",
                    color=keyword,
                    title=f"{keyword.capitalize()} interest in Countries",
                    color_continuous_scale="Blues")
fig.show()

# --------------------------
# 5. Interest over time for the keyword
# --------------------------
time_df = pytrends.interest_over_time()

fig = px.line(time_df, x=time_df.index, y=keyword,
              title=f"{keyword.capitalize()} interest over time",
              color_discrete_sequence=["blue"])
fig.update_layout(
    xaxis=dict(showgrid=True, gridcolor='lightgrey'),
    yaxis=dict(showgrid=True, gridcolor='lightgrey')
)
fig.show()

# --------------------------
# 6. Multiple Keywords Comparison (Dynamic)
# --------------------------

# Step 1: Store the initial keyword
initial_keyword = keyword

# Step 2: Build payload to fetch related queries for the initial keyword
pytrends.build_payload(kw_list=[initial_keyword], cat=0, timeframe='today 12-m', geo='', gprop='')

# Step 3: Fetch related queries from Google Trends
related_queries = pytrends.related_queries()

# Step 4: Extract top related queries for the initial keyword
top_related_df = related_queries[initial_keyword]['top']

if top_related_df is not None:
    # Step 5: Convert related queries to a list
    top_keywords_list = top_related_df['query'].tolist()

    # Step 6: Create a comparison keyword list dynamically
    # - Keep initial keyword at the start
    # - Avoid duplicates (ignore if same as initial keyword)
    # - Limit to top 4 related keywords
    comparison_keywords = [initial_keyword] + [kw for kw in top_keywords_list if kw.lower() != initial_keyword.lower()][
                                              :4]
else:
    # Step 7: Fallback in case no related queries found
    comparison_keywords = [initial_keyword]

print("Comparison keywords:", comparison_keywords)

# Step 8: Build payload for the comparison keywords
pytrends.build_payload(kw_list=comparison_keywords, cat=0, timeframe='today 12-m', geo='', gprop='')

# Step 9: Get interest over time for multiple keywords
comparison_df = pytrends.interest_over_time()

# Step 10: Plot line graph for keyword comparison
fig = px.line(comparison_df, x=comparison_df.index, y=comparison_df.columns[:-1],
              title=f"Interest Over Time for Keywords Related to '{initial_keyword}'")
fig.update_layout(
    xaxis=dict(showgrid=True, gridcolor='lightgrey'),
    yaxis=dict(showgrid=True, gridcolor='lightgrey')
)
fig.show()
