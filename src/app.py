import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Setup
st.set_page_config(layout="wide", page_title="Privacy Analysis Dashboard")
st.title("Institutional Communication in Privacy Policies (2021-2026)")

#folder
base_path = os.path.dirname(__file__)
data_path = os.path.join(base_path, "data.csv")

@st.cache_data
def load_data():
    return pd.read_csv(data_path)

df = load_data()
# ------------------------------

# Sidebar Filters
st.sidebar.header("Data Filters")
sector_choice = st.sidebar.multiselect("Sectors", df['Sector'].unique(), default=df['Sector'].unique())
engage_slider = st.sidebar.slider("Min. Consumer Engagement", float(df['ConsumerEngagement'].min()), float(df['ConsumerEngagement'].max()), float(df['ConsumerEngagement'].min()))

# Filter Logic
filtered = df[(df['Sector'].isin(sector_choice)) & (df['ConsumerEngagement'] >= engage_slider)]

# User Guide
with st.expander("User Guide and Dashboard Instructions"):
    st.markdown("""
    ### How to Navigate this Analysis
    * **Filters:** Use the sidebar to select specific **Sectors** or adjust the **Minimum Consumer Engagement** threshold.
    * **Sector Comparison (Bar Chart):** Compare how different companies perform in consumer engagement. Higher bars indicate more frequent communication.
    * **Voice vs. Complexity (Scatter Plot):** * **X-Axis (OrgVoice):** Higher scores represent a more personal organizational tone.
        * **Y-Axis (Cognitive Complexity):** Higher scores indicate language that is more difficult for consumers to process.
        * **Bubble Size:** Represents the level of Consumer Engagement.
    * **Linguistic Trends (Box Plot):** Highlights the distribution and average complexity levels across different industries.
    """)

# Strategic Implications
st.divider()
st.subheader("Strategic Implications")
col1, col2 = st.columns(2)

with col1:
    st.info("Analysis suggests that sectors with high Cognitive Complexity scores, such as Financial Services, may face challenges in consumer comprehension due to technical language in their policies.")

with col2:
    st.success("Data indicates that organizations with higher Organizational Voice scores generally see higher Consumer Engagement, suggesting a more personal tone correlates with better user interaction.")

# Visualization 1: Sector Comparison
st.subheader("Consumer Engagement by Company")
fig1 = px.bar(filtered, x="company", y="ConsumerEngagement", color="Sector")
st.plotly_chart(fig1, use_container_width=True)

# Visualization 2: Linguistic Dimensions
st.subheader("Organizational Voice vs. Cognitive Complexity")
# This ensures bubble sizes are always positive for the chart
filtered['Size_Ref'] = filtered['ConsumerEngagement'] - filtered['ConsumerEngagement'].min() + 2
fig2 = px.scatter(filtered, x="OrgVoice", y="CognitiveComplexity", size="Size_Ref", color="Sector", 
                 hover_name="company", hover_data={"Size_Ref": False, "ConsumerEngagement": True})
st.plotly_chart(fig2, use_container_width=True)

# Visualization 3: Distribution of Metrics by Sector
st.subheader("Linguistic Trends by Sector")
fig3 = px.box(filtered, x="Sector", y="CognitiveComplexity", color="Sector", points="all")
st.plotly_chart(fig3, use_container_width=True)

# Visualization 4: Raw Data Table
st.subheader("Policy Metric Breakdown")
st.dataframe(filtered.drop(columns=['Size_Ref']), use_container_width=True)

# User Guide & Implications
st.divider()
st.markdown("### Strategic Implications")
st.info("High **Cognitive Complexity** scores suggest policies that may be legally robust but difficult for average consumers to navigate.")
