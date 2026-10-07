import streamlit as st
import pandas as pd

st.set_page_config(page_title="aiCCURACY Control", layout="wide")

st.title("📦 aiCCURACY Control Prototype")
st.write("Cycle Count Variance Viewer – Capstone Prototype v0")

# --- File selection ---
option = st.radio(
    "Select a dataset:",
    ("Warehouse Cycle Count", "Manufacturing Cycle Count")
)

# --- Load correct file ---
if option == "Warehouse Cycle Count":
    file_path = "warehouse_cycle_count.csv"
else:
    file_path = "manufacturing_cycle_count.csv"

try:
    df = pd.read_csv(file_path)
except Exception as e:
    st.error(f"Could not load {file_path}. Make sure the file is uploaded to GitHub.")
    st.stop()

# --- Basic cleaning ---
df.columns = df.columns.str.strip()

# --- Variance calculation ---
if "System_Qty" in df.columns and "Count_Qty" in df.columns:
    df["Variance"] = df["Count_Qty"] - df["System_Qty"]
else:
    st.error("CSV must contain columns: System_Qty and Count_Qty")
    st.stop()

# --- Display data ---
st.subheader("📊 Raw Data")
st.dataframe(df, use_container_width=True)

# --- Summary statistics ---
st.subheader("📈 Variance Summary")
summary = df["Variance"].describe()
st.write(summary)

# --- Chart ---
st.subheader("📉 Variance Chart")
st.line_chart(df["Variance"])

# --- Largest variances ---
st.subheader("🔍 Top Variances")
top_variances = df.sort_values("Variance", key=abs, ascending=False).head(10)
st.dataframe(top_variances, use_container_width=True)

st.success("App loaded successfully!")
