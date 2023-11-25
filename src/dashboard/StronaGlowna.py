import streamlit as st
import os 

print(os.environ["PYTHONPATH"])
from dashboard.functions.data_loading import load_data_concurrently


if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Real Estate EDA")

    st.title("Analiza ofert na rynku nieruchomości")

    st.markdown("Opis *projektu*")

    with st.expander("Web scraping"):
        st.markdown("Dodać informację na temat filtrów wyszukiwania")

if not hasattr(st.session_state, "data"):
    st.session_state.data = {}

load_data_concurrently(True)

st.markdown("Wczytano dane")
