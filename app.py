import pandas as pd
import streamlit as st

st.set_page_config(page_title="Customer Purchase Analysis", page_icon="🛒", layout="wide")
st.title("🛒 Customer Purchase Analysis")


# ---------- 1. Load data ----------
@st.cache_data
def load_data(source) -> pd.DataFrame:
    df = pd.read_csv(source)
    # ---------- 2. Clean data ----------
    df = df.drop_duplicates()
    df["JoiningDate"] = pd.to_datetime(df["JoiningDate"], errors="coerce")
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df = df.dropna(subset=["Gender", "Amount"])
    return df


uploaded = st.sidebar.file_uploader("Upload your own dataset (CSV)", type="csv")
try:
    df = load_data(uploaded if uploaded else "data.csv")
except Exception as e:
    st.error(f"Could not read the dataset: {e}")
    st.stop()

required = {"CustomerID", "Name", "Age", "Gender", "Amount", "JoiningDate"}
if not required.issubset(df.columns):
    st.error(f"CSV must contain columns: {', '.join(sorted(required))}")
    st.stop()

# ---------- 3. Filters ----------
st.sidebar.header("Filters")
gender = st.sidebar.selectbox("Select Gender", ["All"] + sorted(df["Gender"].unique().tolist()))

age_min, age_max = int(df["Age"].min()), int(df["Age"].max())
age_range = st.sidebar.slider("Age range", age_min, age_max, (age_min, age_max))

filtered = df[df["Age"].between(*age_range)]
if gender != "All":
    filtered = filtered[filtered["Gender"] == gender]

if filtered.empty:
    st.warning("No data for the selected filters.")
    st.stop()

# ---------- 4. Analysis (KPIs) ----------
c1, c2, c3 = st.columns(3)
c1.metric("Total Customers", f"{filtered['CustomerID'].nunique():,}")
c2.metric("Total Purchase Amount", f"₹{filtered['Amount'].sum():,.0f}")
c3.metric("Avg Purchase / Customer", f"₹{filtered['Amount'].mean():,.0f}")

# ---------- 5. Visualizations ----------
left, right = st.columns(2)

with left:
    st.subheader("Purchase by Gender")
    st.bar_chart(filtered.groupby("Gender")["Amount"].sum())

with right:
    st.subheader("Monthly Purchase Trend")
    monthly = filtered.set_index("JoiningDate").resample("MS")["Amount"].sum()
    st.line_chart(monthly)

st.subheader("Purchase by Age Group")
bins = [0, 25, 35, 45, 55, 100]
labels = ["<25", "25-34", "35-44", "45-54", "55+"]
age_group = pd.cut(filtered["Age"], bins=bins, labels=labels, right=False)
st.bar_chart(filtered.groupby(age_group, observed=False)["Amount"].sum())

# ---------- 6. Data table + download ----------
st.subheader("Customer Data")
st.dataframe(filtered.sort_values("CustomerID"), width="stretch", hide_index=True)

st.download_button(
    "⬇️ Download filtered data",
    filtered.to_csv(index=False).encode("utf-8"),
    file_name="filtered_customers.csv",
    mime="text/csv",
)
