import streamlit as st
import pandas as pd
import joblib



st.set_page_config(
    page_title="Vehicle Recommendation System",
    page_icon="🚗",
    layout="wide"
)

st.markdown(
    "<h1 style='text-align: center;'>Vehicle Recommendation System</h1>",
    unsafe_allow_html=True
)
st.divider()


# -----------------------
# Load data and model
# -----------------------
df = pd.read_csv("indian_vehicle_dataset.csv")
model = joblib.load("vehicle_recommendation_model.pkl")

# -----------------------
# Feature Engineering
# -----------------------
df["Durability_Score"] = (
    df["Engine Life (years)"] +
    df["Gearbox Life (years)"] +
    df["Suspension Life (years)"] +
    df["Brake Life (years)"] +
    df["Body Panel Life (years)"] +
    df["Tyre Life (years)"] +
    df["Battery Life (years)"]
) / 7

OWNERSHIP_YEARS = 5
df["Total_Cost_of_Ownership"] = (
    df["Price (INR)"] +
    (df["Annual Maintenance Cost (INR)"] * OWNERSHIP_YEARS) +
    df["Replacement Cost of Parts (INR)"]
)

# -----------------------
# UI
# -----------------------
st.subheader("Top Recommended Vehicles")

st.sidebar.header("User Preferences")

max_budget = st.sidebar.slider(
    "Maximum Budget (INR)",
    int(df["Price (INR)"].min()),
    int(df["Price (INR)"].max()),
    1200000
)

min_durability = st.sidebar.slider(
    "Minimum Durability Score",
    float(df["Durability_Score"].min()),
    float(df["Durability_Score"].max()),
    float(df["Durability_Score"].mean())
)

max_maintenance = st.sidebar.slider(
    "Max Annual Maintenance Cost (INR)",
    int(df["Annual Maintenance Cost (INR)"].min()),
    int(df["Annual Maintenance Cost (INR)"].max()),
    10000
)

st.sidebar.header("🔧 Filter Preferences")

segment_filter = st.sidebar.multiselect(
    "Select Vehicle Segment",
    df["Segment"].unique(),
    default=df["Segment"].unique()
)

fuel_filter = st.sidebar.multiselect(
    "Select Fuel Type",
    df["Fuel Type"].unique(),
    default=df["Fuel Type"].unique()
)


# -----------------------
# Recommendation Logic
# -----------------------
if st.button("Get Recommendations"):



    


    filtered = df[
    (df["Price (INR)"] <= max_budget) &
    (df["Durability_Score"] >= min_durability) &
    (df["Annual Maintenance Cost (INR)"] <= max_maintenance) &
    (df["Segment"].isin(segment_filter)) &
    (df["Fuel Type"].isin(fuel_filter))
    ].copy()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Vehicles", len(df))
    col2.metric("Matching Vehicles", len(filtered))
    col3.metric("Max Budget (₹)", f"{max_budget:,}")


    if filtered.empty:
        st.warning("No vehicles match your criteria.")
    else:
        features = [
            "Price (INR)",
            "Durability_Score",
            "Annual Maintenance Cost (INR)",
            "Total_Cost_of_Ownership"
        ]

        filtered["Predicted_Value_Score"] = model.predict(filtered[features])

        result = filtered.sort_values(
            "Predicted_Value_Score", ascending=False
        ).head(5)

        st.subheader("Top Recommended Vehicles")
        for _, row in result.iterrows():
            st.markdown(f"""
            ### 🚘 {row['Brand']} {row['Model']}
            - **Segment:** {row['Segment']}
            - **Fuel:** {row['Fuel Type']}
            - **Price:** ₹{row['Price (INR)']:,}
            - **Durability:** {row['Durability_Score']:.2f}
            - **Maintenance:** ₹{row['Annual Maintenance Cost (INR)']:,}
            """)
            st.divider()


