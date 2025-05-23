import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load dataset
df = pd.read_csv("Twitterdatainsheets.csv", low_memory=False)

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Ensure expected columns exist
expected_columns = ['tweetid', 'weekday', 'hour', 'day', 'lang', 'isreshare', 
                    'reach', 'retweetcount', 'likes', 'klout', 'sentiment', 
                    'text', 'locationid', 'userid']

missing_cols = [col for col in expected_columns if col not in df.columns]
if missing_cols:
    st.error(f"Missing columns in dataset: {missing_cols}")

# Convert necessary columns to numeric
num_cols = ['hour', 'likes', 'retweetcount', 'reach']
for col in num_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Rename `userid` to `followers` for clarity (if applicable)
if 'userid' in df.columns:
    df.rename(columns={'userid': 'followers'}, inplace=True)

# Streamlit UI
st.title("📊 Twitter Engagement Dashboard")

# Sidebar Filters
st.sidebar.header("Filter Options")
selected_sentiment = st.sidebar.selectbox("Select Sentiment", df["sentiment"].unique())
selected_language = st.sidebar.selectbox("Select Language", df["lang"].unique())

# Filter Data
filtered_df = df[(df["sentiment"] == selected_sentiment) & (df["lang"] == selected_language)]

# Section 1: Best Time to Post
st.subheader("🕒 Best Time to Post")
if "hour" in df.columns:
    hourly_engagement = df.groupby("hour")["likes"].mean().reset_index()
    fig = px.line(hourly_engagement, x="hour", y="likes", title="Engagement by Hour", markers=True)
    st.plotly_chart(fig)

# Section 2: Best Days to Post
st.subheader("📅 Best Days for Engagement")
if "weekday" in df.columns:
    daywise_engagement = df.groupby("weekday")["likes"].mean().reset_index()
    fig = px.bar(daywise_engagement, x="weekday", y="likes", title="Engagement by Day", color="weekday")
    st.plotly_chart(fig)

# Section 3: Sentiment Analysis
st.subheader("😊 Sentiment Impact on Engagement")
if "sentiment" in df.columns:
    fig = px.histogram(df, x="sentiment", y="likes", title="Engagement by Sentiment", color="sentiment")
    st.plotly_chart(fig)

# Section 4: Male vs Female Tweet Engagement (If Gender Column Exists)
if "gender" in df.columns:
    st.subheader("👥 Male vs Female Tweet Engagement")
    gender_engagement = df.groupby("gender")["likes"].mean().reset_index()
    fig = px.bar(gender_engagement, x="gender", y="likes", title="Engagement by Gender", color="gender")
    st.plotly_chart(fig)

# Section 5: Influencer Impact (Fixing the Followers Column Issue)
st.subheader("📢 Influencer Engagement")
if "followers" in df.columns and "retweetcount" in df.columns:
    fig = px.scatter(df, x="followers", y="retweetcount", size="reach", color="isreshare",
                     title="Influence of Followers on Engagement")
    st.plotly_chart(fig)
else:
    st.warning("Followers column not found. Using UserID instead.")
    if "userid" in df.columns:
        fig = px.scatter(df, x="userid", y="retweetcount", size="reach", color="isreshare",
                         title="Influence of Users on Engagement")
        st.plotly_chart(fig)

# Section 6: Language Analysis
st.subheader("🌍 Language Preference in Engagement")
if "lang" in df.columns:
    fig = px.pie(df, names="lang", values="likes", title="Engagement by Language")
    st.plotly_chart(fig)

# Section 7: Engagement vs Reach
st.subheader("📈 Reach vs Engagement")
if "reach" in df.columns and "likes" in df.columns:
    fig = px.scatter(df, x="reach", y="likes", title="Reach vs Engagement", color="reach")
    st.plotly_chart(fig)
