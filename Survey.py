import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

st.title("Data Collection Survey 📝")
st.write("Please fill out the form below to add your data to the dataset.")

with st.form("survey_form"):
    category_input = st.text_input("Enter a category:")
    value_input = st.text_input("Enter a corresponding value:")
    submitted = st.form_submit_button("Submit Data")

    if submitted:
        if category_input.strip() != "" and value_input.strip() != "":
            new_row = pd.DataFrame([[category_input, value_input]], columns=["Category", "Value"])
            if os.path.exists("data.csv") and os.path.getsize("data.csv") > 0:
                existing_data = pd.read_csv("data.csv")
                updated_data = pd.concat([existing_data, new_row], ignore_index=True)
            else:
                updated_data = new_row
            updated_data.to_csv("data.csv", index=False)
            st.success("Your data has been submitted!")
            st.write(f"You entered: **Category:** {category_input}, **Value:** {value_input}")
        else:
            st.warning("Please enter both a category and a value.")

st.divider()
st.header("Current Data in CSV")

if os.path.exists("data.csv") and os.path.getsize("data.csv") > 0:
    current_data_df = pd.read_csv("data.csv")
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")
