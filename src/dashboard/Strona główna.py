import streamlit as st
import time

from dashboard.functions.data_loading import load_data_concurrently


if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Real Estate EDA")

    st.title("Analiza ofert na rynku nieruchomości")

    st.text("Dane pochodzą z okresu...")
    st.write("Dane pochodzą z okresu...")
    st.markdown("Dane pochodzą z okresu...")

if not hasattr(st.session_state, "data"):
    st.session_state.data = {}

start = time.perf_counter()
load_data_concurrently(True)
stop = time.perf_counter()
print("!", stop - start)

st.markdown("Teraz")
