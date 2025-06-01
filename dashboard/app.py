
# dashboard/app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Price Tracker", layout="centered")

@st.cache_data
def load_data():
    try:
        csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "price_log.csv")
        df = pd.read_csv(csv_path)
        df["timestamp"] = pd.to_datetime(df["timestamp"], format='ISO8601', errors='coerce')

        return df
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()

df = load_data()

st.title("📊 Book Price Tracker Dashboard")

if df.empty:
    st.warning("No data available. Please run the scraper first.")
    st.stop()

# Product dropdown
products = df["product_name"].dropna().unique()
selected_product = st.selectbox("Select a product", sorted(products))

filtered = df[df["product_name"] == selected_product].sort_values("timestamp")

# Clean price
filtered = filtered[filtered["price"].notnull()]
filtered = filtered[filtered["price"].apply(lambda x: isinstance(x, str))]
filtered["price_num"] = filtered["price"].str.replace(r"[^\d.]", "", regex=True).astype(float)

if filtered.empty:
    st.warning("No valid price data available for this product.")
else:
    st.subheader("📈 Price Over Time")
    fig, ax = plt.subplots()
    ax.plot(filtered["timestamp"], filtered["price_num"], marker="o")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (GBP)")
    ax.set_title(f"{selected_product}")
    st.pyplot(fig)

    st.subheader("📄 Latest Entry")
    st.dataframe(filtered.tail(1), use_container_width=True)

    st.download_button(
        label="⬇️ Download CSV",
        data=df.to_csv(index=False),
        file_name="price_log.csv",
        mime="text/csv"
    )
