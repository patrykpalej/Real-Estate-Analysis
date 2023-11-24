import streamlit as st

from utils.storage import (get_credentials, generate_psql_connection_string,
                           read_from_db)
from dashboard.functions.lots import preprocess_lots
from dashboard.functions.houses import preprocess_houses
from dashboard.functions.apartments import preprocess_apartments

connection_string = generate_psql_connection_string(*get_credentials())


if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Real Estate EDA")

    st.title("Analiza ofert na rynku nieruchomości")
    st.text("Dane pochodzą z okresu...")

df_lots = preprocess_lots(
    read_from_db("SELECT * FROM otodom_lots", connection_string))

df_houses = preprocess_houses(
    read_from_db("SELECT * FROM otodom_houses", connection_string))

df_apartments = preprocess_apartments(
    read_from_db("SELECT * FROM otodom_apartments", connection_string))
