import streamlit as st
from datetime import date, timedelta

from dashboard.functions.data_loading import load_data_concurrently

from dashboard.functions.apartments import (
    plot_all, plot_by_month, plot_by_province, plot_map)


st.set_page_config(layout="wide", page_title="Mieszkania")

st.title("Mieszkania")
st.header("Filtry")

st.markdown(
        """
       <style>
        .stNumberInput {
            margin-bottom: 2em;

       </style>
   """, unsafe_allow_html=True)

try:
    df = st.session_state.data["apartments"]
except (KeyError, AttributeError):
    with st.spinner(f'Ładowanie danych'):
        st.session_state.data = {}
        load_data_concurrently(True)
        df = st.session_state.data["apartments"]

min_area, max_area, _, min_price, max_price, _, min_created, max_created = (
    st.columns([3, 3, 1, 3, 3, 1, 3, 3]))

province, _, market, status, _, min_year, max_year = (
    st.columns([6, 1, 3, 3, 1, 3, 3]))

with min_area:
    min_area_filter = min_area.number_input(
        "Min. powierzchnia mieszkania", min_value=df['apartment_area'].min(),
        value=df['apartment_area'].min(), max_value=df['apartment_area'].max())

with max_area:
    max_area_filter = max_area.number_input(
        "Max. powierzchnia mieszkania", min_value=df['apartment_area'].min(),
        value=df['apartment_area'].max(), max_value=df['apartment_area'].max())

with min_price:
    min_price_filter = min_price.number_input(
        "Minimalna cena", min_value=df['price'].min(), value=df['price'].min(),
        max_value=1200000)  # outliers in data

with max_price:
    max_price_filter = max_price.number_input(
        "Maksymalna cena", min_value=df['price'].min(),
        value=1200000, max_value=1200000)

with min_created:
    min_created_filter = min_created.date_input(
        "Oferta dodana po", date.today() - timedelta(days=90))

with max_created:
    max_created_filter = max_created.date_input(
        "Oferta dodana przed", date.today())

with province:
    toggle_province = st.toggle('Filtruj województwa')
    if toggle_province:
        province_filter = province.multiselect(
            "Województwa", options=df["province"].unique(),
            default=df["province"].unique())

with market:
    market_filter = market.multiselect(
        "Rynek", options=df["market"].unique(), default=df["market"].unique())

with status:
    status_filter = status.multiselect(
        "Status", options=df["status"].unique(),
        default=df["status"].unique())

with min_year:
    min_year_filter = min_year.number_input(
        "Minimalny rok budowy", min_value=df['build_year'].min(),
        value=df['build_year'].min(), max_value=df['build_year'].max())

with max_year:
    max_year_filter = max_year.number_input(
        "Maksymalny rok budowy", min_value=df['build_year'].min(),
        value=df['build_year'].max(), max_value=df['build_year'].max())


df = df[(df["utc_created_at"].dt.date <= max_created_filter) &
        (df["utc_created_at"].dt.date >= min_created_filter) &
        (df["price"] >= min_price_filter) &
        (df["price"] <= max_price_filter) &
        (df["apartment_area"] <= max_area_filter) &
        (df["apartment_area"] >= min_area_filter) &
        (df["build_year"] <= max_year_filter) &
        (df["build_year"] >= min_year_filter) &
        (df["market"].isin(market_filter)) &
        (df["status"].isin(status_filter))]

if "province_filter" in locals():
    df = df[df["province"].isin(province_filter)]

st.markdown(f"Liczba ofert: {len(df)}")

st.header("Wykresy")


if len(df):
    with st.spinner(f'Przetwarzam {len(df)} ofert(y)'):
        fig_all = plot_all(df)
        st.plotly_chart(fig_all)
        st.markdown("***")

    with st.spinner(f'Przetwarzam {len(df)} ofert(y)'):
        fig_by_month = plot_by_month(df)
        st.plotly_chart(fig_by_month)
        st.markdown("***")

    with st.spinner(f'Przetwarzam {len(df)} ofert(y)'):
        fig_by_province = plot_by_province(df)
        st.plotly_chart(fig_by_province)
        st.markdown("***")

    with st.spinner(f'Przetwarzam {len(df)} ofert(y)'):
        toggle_urls = st.toggle(
            'Uwzględnij adresy url ofert (może potrwać dłużej)')

        button_map = st.button('Pokaż mapę')

        if button_map:
            fig_map = plot_map(df, urls=toggle_urls)
            if toggle_urls:
                st.markdown("Kliknij na punkt aby zobaczyć adres oferty")

            st.components.v1.html(fig_map._repr_html_(), width=1100, height=1200)
else:
    st.markdown("Nie ma żadnych ofert, które spełniają kryteria")
