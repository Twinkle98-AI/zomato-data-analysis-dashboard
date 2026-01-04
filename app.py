import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="Zomato Rating Dashboard", page_icon="⭐")
st.title("⭐ Zomato Rating Dashboard")
st.write("Fully error-proof exploratory analysis of Zomato ratings")

# -------------------------
# Load Dataset
# -------------------------
df = pd.read_csv("Zomato-data-.csv")

st.subheader("📌 Dataset Columns (Auto-detected)")
st.write(df.columns.tolist())

# -------------------------
# Auto-detect Columns
# -------------------------
# Rating column
rating_candidates = ["rate", "rating", "aggregate_rating"]
rating_col = next((c for c in rating_candidates if c in df.columns), None)

# Name column
name_candidates = ["name", "restaurant_name"]
name_col = next((c for c in name_candidates if c in df.columns), None)

# Location column
location_candidates = ["location", "listed_in(city)", "city", "area", "address"]
location_col = next((c for c in location_candidates if c in df.columns), None)

# -------------------------
# Safety Check
# -------------------------
if rating_col is None:
    st.error("❌ No rating column found in dataset.")
    st.stop()

# -------------------------
# Clean Rating Column
# -------------------------
df = df[df[rating_col].notnull()]
df[rating_col] = df[rating_col].astype(str)

# Remove non-numeric ratings
df = df[~df[rating_col].isin(["NEW", "-", "Not rated"])]

# Convert "4.1/5" → 4.1
df[rating_col] = df[rating_col].str.split("/").str[0]
df[rating_col] = pd.to_numeric(df[rating_col], errors="coerce")
df = df.dropna(subset=[rating_col])

# -------------------------
# Dataset Preview
# -------------------------
st.subheader("🔍 Dataset Preview")

preview_cols = []
if name_col:
    preview_cols.append(name_col)
if location_col:
    preview_cols.append(location_col)
preview_cols.append(rating_col)

st.dataframe(df[preview_cols].head())

# -------------------------
# KPI Metrics
# -------------------------
st.subheader("📊 Key Metrics")

col1, col2 = st.columns(2)
col1.metric("Total Restaurants", df.shape[0])
col2.metric("Average Rating", round(df[rating_col].mean(), 2))

# -------------------------
# Rating Distribution
# -------------------------
st.subheader("📈 Rating Distribution")

fig, ax = plt.subplots()
ax.hist(df[rating_col], bins=10)
ax.set_xlabel("Rating")
ax.set_ylabel("Number of Restaurants")
st.pyplot(fig)

# -------------------------
# Top Rated Restaurants
# -------------------------
st.subheader("🏆 Top Rated Restaurants")

top_rated = df.sort_values(by=rating_col, ascending=False).head(10)
st.dataframe(top_rated[preview_cols])

# -------------------------
# Footer
# -------------------------
st.divider()
st.markdown("🛠 **Tools:** Python, Pandas, Matplotlib, Streamlit")
st.markdown("📌 **Project Type:** Fully Error-Proof EDA Dashboard")




