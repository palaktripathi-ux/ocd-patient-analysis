import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import streamlit as st
st.write("App started successfully")


# Page config
st.set_page_config(
    page_title="OCD Patient Analysis Dashboard",
    layout="wide"
)

# Title
st.title("🧠 OCD Patient Analysis Dashboard")
st.write("Interactive exploration of OCD patient demographics and clinical data")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("data/processed/cleaned_ocd_data.csv")

df = load_data()

# Sidebar filters
st.sidebar.header("Filter Patients")

# Gender filter
gender_options = df["gender"].unique()
selected_gender = st.sidebar.multiselect(
    "Select Gender",
    gender_options,
    default=gender_options
)

# Age filter
min_age, max_age = int(df["age"].min()), int(df["age"].max())
age_range = st.sidebar.slider(
    "Select Age Range",
    min_age, max_age, (min_age, max_age)
)

# Apply filters
filtered_df = df[
    (df["gender"].isin(selected_gender)) &
    (df["age"].between(age_range[0], age_range[1]))
]

# KPI Metrics
st.subheader("📊 Key Metrics")
col1, col2, col3 = st.columns(3)

col1.metric("Total Patients", len(filtered_df))
col2.metric("Average Age", round(filtered_df["age"].mean(), 1))
col3.metric("Average Severity Score (Obsessions)", round(filtered_df["y-bocs_score_(obsessions)"].mean(), 1))
col3.metric("Average Severity Score (Compulsions)", round(filtered_df["y-bocs_score_(compulsions)"].mean(), 1))

# Charts
st.subheader("📈 Visual Analysis")

# Age distribution
fig1, ax1 = plt.subplots()
sns.histplot(filtered_df["age"], kde=True, ax=ax1)
ax1.set_title("Age Distribution")
st.pyplot(fig1)

# previous_diagnoses distribution (if exists)
if "previous_diagnoses" in filtered_df.columns:
    fig2, ax2 = plt.subplots()
    sns.countplot(x="previous_diagnoses", data=filtered_df, ax=ax2)
    ax2.set_title("Previous Diagnoses")
    st.pyplot(fig2)

# age vs y-bocs_score_(obsessions)
fig3, ax3 = plt.subplots()
sns.scatterplot(
    x="age",
    y="y-bocs_score_(obsessions)",
    data=filtered_df,
    ax=ax3
)
ax3.set_title("Age vs Severity Score (Obsessions)")
st.pyplot(fig3)

# age vs y-bocs_score_(compulsions)
fig4, ax4 = plt.subplots()
sns.scatterplot(
    x="age",
    y="y-bocs_score_(compulsions)",
    data=filtered_df,
    ax=ax4
)
ax4.set_title("Age vs Severity Score (Compulsions)")
st.pyplot(fig4)
# Raw data toggle
with st.expander("📄 View Raw Data"):
    st.dataframe(filtered_df)
    
from pathlib import Path
import pandas as pd
import streamlit as st

DATA_PATH = Path("data/processed/cleaned_ocd_data.csv")

@st.cache_data
def load_data():
    if not DATA_PATH.exists():
        st.error(f"File not found: {DATA_PATH}")
        st.stop()
    return pd.read_csv(DATA_PATH)
