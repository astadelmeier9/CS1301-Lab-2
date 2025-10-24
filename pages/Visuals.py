import streamlit as st
import pandas as pd
import json
import os
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Visualizations",
    page_icon="📈",
)

st.title("Data Visualizations 📈")
st.write("This page displays graphs based on the collected data.")

st.divider()
st.header("Load Data")

csv_data = None
json_data = None

if os.path.exists("data.csv") and os.path.getsize("data.csv") > 0:
    try:
        csv_data = pd.read_csv("data.csv")
        st.success("CSV data loaded successfully.")
        st.dataframe(csv_data)  #NEW
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
else:
    st.warning("The 'data.csv' file is empty or missing.")

if os.path.exists("data.json") and os.path.getsize("data.json") > 0:
    try:
        with open("data.json") as f:
            json_data = json.load(f)
        st.success("JSON data loaded successfully.")
        st.json(json_data)  #NEW
    except Exception as e:
        st.error(f"Error loading JSON: {e}")
else:
    st.warning("The 'data.json' file is empty or missing.")

st.divider()
st.header("Edit or Create JSON Data")

json_editor = st.text_area(
    "Edit JSON content here:",
    value=json.dumps(json_data or {}, indent=4),
    height=200
)

if st.button("Save JSON"):
    try:
        updated_json = json.loads(json_editor)
        with open("data.json", "w") as f:
            json.dump(updated_json, f, indent=4)
        st.success("✅ JSON file updated successfully! Refresh the page to see new graphs.")
    except json.JSONDecodeError:
        st.error("❌ Invalid JSON format. Please fix syntax before saving.")

st.divider()
st.header("Graphs")

st.subheader("Graph 1: Static Bar Chart")
if csv_data is not None and not csv_data.empty:
    try:
        fig1, ax1 = plt.subplots()
        ax1.bar(csv_data["Category"], pd.to_numeric(csv_data["Value"], errors="coerce"))
        ax1.set_title("Values by Category")
        ax1.set_xlabel("Category")
        ax1.set_ylabel("Value")
        st.pyplot(fig1)
        st.caption("This static bar chart displays the values collected from the CSV data by category.")
    except Exception as e:
        st.error(f"Error displaying static graph: {e}")
else:
    st.warning("No CSV data available for the static graph.")

st.subheader("Graph 2: Dynamic Histogram (CSV)")
if csv_data is not None and not csv_data.empty:
    try:
        if "bins" not in st.session_state:
            st.session_state.bins = 5
        st.session_state.bins = st.slider("Select number of bins:", 3, 20, st.session_state.bins)  #NEW
        numeric_values = pd.to_numeric(csv_data["Value"], errors="coerce").dropna()
        fig2, ax2 = plt.subplots()
        ax2.hist(numeric_values, bins=st.session_state.bins, color="skyblue", edgecolor="black")
        ax2.set_title("Distribution of Values (Dynamic)")
        ax2.set_xlabel("Value")
        ax2.set_ylabel("Frequency")
        st.pyplot(fig2)
        st.caption("Use the slider above to adjust the histogram bins dynamically.")
    except Exception as e:
        st.error(f"Error displaying dynamic histogram: {e}")
else:
    st.warning("No numeric CSV data available for histogram.")

st.subheader("Graph 3: Dynamic Pie Chart (JSON)")
if json_data is not None and "favorite_activities" in json_data:
    activities = json_data["favorite_activities"]
    if "selected_activity" not in st.session_state:
        st.session_state.selected_activity = list(activities.keys())[0]
    selected = st.selectbox("Select an activity to highlight:", list(activities.keys()))
    
    fig3, ax3 = plt.subplots()
    # Create explode effect for selected activity
    explode = [0.1 if act == selected else 0 for act in activities.keys()]
    colors = ["orange" if act == selected else "lightblue" for act in activities.keys()]
    
    ax3.pie(activities.values(), labels=activities.keys(), autopct='%1.1f%%', 
            explode=explode, colors=colors, startangle=90)
    ax3.set_title("Favorite Activities Distribution from JSON")
    st.pyplot(fig3)
    st.caption(f"This dynamic pie chart uses JSON data. The highlighted slice shows **{selected}**.")

