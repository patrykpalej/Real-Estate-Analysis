import os
import sys
import streamlit as st
from st_pages import Page, show_pages
from st_pages import show_pages_from_config
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.environ["PYTHONPATH"])

from dashboard.functions.data_loading import load_data_concurrently
from dashboard.functions.main_page import main_page

os.chdir(os.environ["PYTHONPATH"])

st.set_page_config(layout="wide", page_title="Real Estate Market Analysis")

show_pages_from_config()

# show_pages(
#     [
#         Page("dashboard/main.py", "Project description", "💻"),
#         Page("dashboard/pages/page_houses.py", "Houses", "🏡"),
#         Page("dashboard/pages/page_lands.py", "Lands", "🌳"),
#         Page("dashboard/pages/page_apartments.py", "Apartments", "🏢")
#     ])


if __name__ == "__main__":
    main_page()


if not hasattr(st.session_state, "data"):
    st.session_state.data = {}
    load_data_concurrently(True)

st.markdown("Data loaded")
