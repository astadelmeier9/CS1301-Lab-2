# This creates the main landing page for the Streamlit application.
# Contains an introduction to the project and guide users to other pages.

# Import Streamlit
import streamlit as st

import streamlit as st

st.set_page_config(page_title="Lab 02 Streamlit App", page_icon="📊")

st.title("Welcome to My Streamlit Project")

st.write("""
This app collects survey responses, saves them to a CSV file, and visualizes both CSV
and JSON data across multiple pages.
""")

st.write("Use the sidebar to visit the Survey or Graphs pages.")
