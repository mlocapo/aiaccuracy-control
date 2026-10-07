import streamlit as st
import pandas as pd

st.set_page_config(page_title="aiCCURACY Control", layout="wide")

st.title("📦 aiCCURACY Control Prototype")
st.write("Cycle Count Variance Viewer – Capstone Prototype v0")

# --- GitHub RAW file URLs ---
WAREHOUSE_URL = "https://raw.githubusercontent.com/mlocapo/aiaccuracy-control/main/warehouse_cycle_count.csv"
MANUFACTURING_URL = "https://raw.githubusercontent.com/mlocapo/aiaccuracy-control/main/manufacturing_cycle_count.csv"

# --- Dataset selection ---
option = st.radio(
    "Select a dataset:",
    ("Warehouse Cycle Count", "Manufacturing Cycle Count")
)

# --- Load correct dataset ---
try:
    if option == "Warehouse Cycle Count":
        df = pd.read_csv(WAREHOUSE_URL)
    else:
        df = pd.read_csv(MANUFACTURING_URL)
except Exception as e:
    st.error(f"Could not load the selected dataset. Error: {e}")
    st.stop()

# --- Clean column names ---
df.columns = df.columns.str.strip()

# --- Validate required columns ---
required_cols = {"System_Qty", "Count_Qty"}
if not required_cols.issubset(df.columns):
    st.error("CSV must contain columns: System_Qty and Count_Qty")
    st.stop()

# --- Variance calculation ---
df["Variance"] = df["Count_Qty"] - df["System_Qty"]

# --- Display raw data ---
st.subheader("📊 Raw Data")
st.dataframe(df, use_container_width=True)

# --- Summary statistics ---
st.subheader("📈 Variance Summary")
st.write(df["Variance"].describe())

# --- Variance chart ---
st.subheader("📉 Variance Chart")
st.line_chart(df["Variance"])

# --- Largest variances ---
st.subheader("🔍 Top Variances")
top_variances = df.sort_values("Variance", key=abs, ascending=False).head(10)
st.dataframe(top_variances, use_container_width=True)

st.success("App loaded successfully!")
