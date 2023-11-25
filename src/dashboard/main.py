import streamlit as st
from st_pages import Page, show_pages

from dashboard.functions.data_loading import load_data_concurrently


st.set_page_config(layout="wide", page_title="Analiza rynku nieruchomości")

show_pages(
    [
        Page("dashboard/main.py", "Opis projektu", "💻"),
        Page("dashboard/pages/page_houses.py", "Oferty domów", "🏡"),
        Page("dashboard/pages/page_lots.py", "Oferty działek", "🟩"),
        Page("dashboard/pages/page_apartments.py", "Oferty mieszkań", "🏢"),
    ])


if __name__ == "__main__":
    st.title("Analiza ofert na rynku nieruchomości")
    st.markdown("## Opis projektu")
    st.markdown("...")
    # with st.expander("Web scraping"):
    #     st.markdown("Dodać informację na temat filtrów wyszukiwania")

if not hasattr(st.session_state, "data"):
    st.session_state.data = {}

load_data_concurrently(True)

st.markdown("Wczytano dane")
