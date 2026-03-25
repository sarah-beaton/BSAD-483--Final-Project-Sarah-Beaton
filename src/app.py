import streamlit as st
import pandas as pd
import plotly.express as px

# Config
st.set_page_config(layout="wide", page_title="Privacy Policy Analysis")
st.title("Institutional Communication in Canadian Privacy Policies")
st.markdown("### Longitudinal Linguistic Factor Analysis (2021-2026)")

# Load Data w root assmpt
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")
    return df

df = load_data()

# flt
st.sidebar.header("Dashboard Controls")
selected_sectors = st.sidebar.multiselect("Select Sectors", df['Sector'].unique(), default=df['Sector'].unique())
min_year = st.sidebar.select_slider("Select Start Year", options=sorted(df['Year'].unique()))

filtered_df = df[(df['Sector'].isin(selected_sectors)) & (df['Year'] >= min_year)]

#viz
col1, col2 = st.columns(2)

with col1:
    st.subheader("Consumer Engagement by Company")
    fig1 = px.bar(filtered_df, x="company", y="ConsumerEngagement", color="Sector")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Linguistic Dimensions: Voice vs. Complexity")
    # Fix for negative size error: shift values for visualization only
    filtered_df['MarkerSize'] = filtered_df['ConsumerEngagement'] - filtered_df['ConsumerEngagement'].min() + 2
    fig2 = px.scatter(filtered_df, x="OrgVoice", y="CognitiveComplexity", 
                     size="MarkerSize", color="Sector", hover_name="company",
                     hover_data={"MarkerSize": False, "ConsumerEngagement": True})
    st.plotly_chart(fig2, use_container_width=True)

# Viz tb
st.subheader("Policy Metric Summary")
st.dataframe(filtered_df[['Sector', 'company', 'Year', 'ConsumerEngagement', 'OrgVoice', 'CognitiveComplexity']], use_container_width=True)

# dec
st.divider()
st.subheader("Strategic Implications")
st.info("Analysis shows that **Financial Services** lead in engagement. Organizations in the **Health** sector exhibit lower scores, suggesting a need for policy simplification to improve consumer trust.")
