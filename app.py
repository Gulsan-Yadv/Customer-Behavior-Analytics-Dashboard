import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Retail Customer Behavior Analytics",
    page_icon="📊",
    layout="wide"
)

# -------------------- LOAD DATA --------------------
@st.cache_data
def load_data():
    return pd.read_csv("customer_shopping_behavior.csv")

df = load_data()

# -------------------- SIDEBAR --------------------
st.sidebar.title("📊 Dashboard Filters")

gender = st.sidebar.multiselect(
    "Gender",
    options=sorted(df["Gender"].unique()),
    default=sorted(df["Gender"].unique())
)

category = st.sidebar.multiselect(
    "Category",
    options=sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

season = st.sidebar.multiselect(
    "Season",
    options=sorted(df["Season"].unique()),
    default=sorted(df["Season"].unique())
)

payment = st.sidebar.multiselect(
    "Payment Method",
    options=sorted(df["Payment Method"].unique()),
    default=sorted(df["Payment Method"].unique())
)

filtered_df = df[
    (df["Gender"].isin(gender)) &
    (df["Category"].isin(category)) &
    (df["Season"].isin(season)) &
    (df["Payment Method"].isin(payment))
]

# -------------------- TITLE --------------------
st.title("📊 Retail Customer Behavior Analytics Dashboard")

st.markdown("Interactive dashboard for analyzing customer shopping behavior.")

st.divider()

# -------------------- KPI CARDS --------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("Customers", len(filtered_df))
c2.metric("Revenue ($)", f"{filtered_df['Purchase Amount (USD)'].sum():,.0f}")
c3.metric("Average Purchase", f"${filtered_df['Purchase Amount (USD)'].mean():.2f}")
c4.metric("Average Rating", round(filtered_df["Review Rating"].mean(),2))

st.divider()

# -------------------- CHARTS --------------------
left, right = st.columns(2)

with left:
    st.subheader("Purchases by Category")

    category_chart = (
        filtered_df["Category"]
        .value_counts()
        .reset_index()
    )

    category_chart.columns = ["Category", "Count"]

    fig = px.bar(
        category_chart,
        x="Category",
        y="Count",
        color="Category",
        text="Count"
    )

    st.plotly_chart(fig, width="stretch")

with right:
    st.subheader("Gender Distribution")

    fig = px.pie(
        filtered_df,
        names="Gender",
        hole=.45
    )

    st.plotly_chart(fig, width="stretch")

left, right = st.columns(2)

with left:

    st.subheader("Payment Methods")

    fig = px.pie(
        filtered_df,
        names="Payment Method",
        hole=.45
    )

    st.plotly_chart(fig, width="stretch")

with right:

    st.subheader("Age Distribution")

    fig = px.histogram(
        filtered_df,
        x="Age",
        nbins=20,
        color="Gender"
    )

    st.plotly_chart(fig, width="stretch")

st.divider()

# -------------------- SECOND ROW OF CHARTS --------------------

left, right = st.columns(2)

with left:
    st.subheader("Season Wise Purchases")

    season_chart = (
        filtered_df["Season"]
        .value_counts()
        .reset_index()
    )

    season_chart.columns = ["Season", "Count"]

    fig = px.bar(
        season_chart,
        x="Season",
        y="Count",
        color="Season",
        text="Count"
    )

    st.plotly_chart(fig, width="stretch")

with right:

    st.subheader("Subscription Status")

    fig = px.pie(
        filtered_df,
        names="Subscription Status",
        hole=.45
    )

    st.plotly_chart(fig, width="stretch")


# -------------------- LOCATION --------------------

st.subheader("Purchases by Location")

location_chart = (
    filtered_df.groupby("Location")["Purchase Amount (USD)"]
    .sum()
    .reset_index()
)

location_chart = location_chart.sort_values(
    by="Purchase Amount (USD)",
    ascending=False
)

fig = px.bar(
    location_chart,
    x="Location",
    y="Purchase Amount (USD)",
    color="Purchase Amount (USD)"
)

st.plotly_chart(fig, width="stretch")


# -------------------- REVIEW RATING --------------------

st.subheader("Review Rating Distribution")

fig = px.histogram(
    filtered_df,
    x="Review Rating",
    nbins=10,
    color="Gender"
)

st.plotly_chart(fig, width="stretch")


# -------------------- DATASET --------------------

st.subheader("Dataset Explorer")

st.dataframe(filtered_df, width="stretch")


# -------------------- DOWNLOAD --------------------

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Dataset",
    data=csv,
    file_name="filtered_customer_data.csv",
    mime="text/csv"
)


# -------------------- BUSINESS INSIGHTS --------------------

st.subheader("📌 Business Insights")

top_category = filtered_df["Category"].value_counts().idxmax()
top_payment = filtered_df["Payment Method"].value_counts().idxmax()
top_season = filtered_df["Season"].value_counts().idxmax()

st.success(f"Top Selling Category : {top_category}")

st.info(f"Most Preferred Payment Method : {top_payment}")

st.warning(f"Highest Shopping Season : {top_season}")


# -------------------- FOOTER --------------------

st.divider()

st.caption(
    "Retail Customer Behavior Analytics Dashboard | Built using Streamlit & Plotly"
)