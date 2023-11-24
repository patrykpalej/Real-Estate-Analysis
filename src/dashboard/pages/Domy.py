import streamlit as st
from datetime import date, timedelta

from dashboard.functions.houses import (
    plot_all, plot_by_month, plot_by_province, plot_map)
from dashboard.main import df_houses as df


st.set_page_config(layout="wide", page_title="Domy",)

st.title("Domy")
st.header("Filtry")

st.markdown(
        """
       <style>
       </style>
   """, unsafe_allow_html=True)


min_area, max_area, _, min_price, max_price, _, min_created, max_created = \
    st.columns([3, 3, 1, 3, 3, 1, 3, 3])

min_year, max_year, _, market, _, province = \
    st.columns([3, 3, 1, 3, 1, 9])

with min_area:
    min_area_filter = min_area.number_input("Minimalna powierzchnia domu",
                      min_value=df['house_area'].min(), value=df['house_area'].min(),
                      max_value=df['house_area'].max())

with max_area:
    max_area_filter = max_area.number_input("Maksymalna powierzchnia domu",
                      min_value=df['house_area'].min(), value=df['house_area'].max(),
                      max_value=df['house_area'].max())

with min_price:
    min_price_filter = min_price.number_input("Minimalna cena",
                      min_value=df['price'].min(), value=df['price'].min(),
                      max_value=df['price'].max())

with max_price:
    max_price_filter = max_price.number_input("Maksymalna cena",
                      min_value=df['price'].min(), value=df['price'].max(),
                      max_value=df['price'].max())

with min_created:
    min_created_filter = min_created.date_input("Oferta dodana po", date.today() - timedelta(days=30))

with max_created:
    max_created_filter = max_created.date_input("Oferta dodana przed", date.today())

with min_year:
    min_year_filter = min_year.number_input(
        "Minimalny rok budowy", min_value=int(df['build_year'].min()),
        value=int(df['build_year'].min()), max_value=int(df['build_year'].max()))

with max_year:
    max_year_filter = max_year.number_input(
        "Maksymalny rok budowy", min_value=int(df['build_year'].min()),
        value=int(df['build_year'].max()), max_value=int(df['build_year'].max()))

with market:
    market_filter = market.multiselect("Rynek", options=df["market"].unique(),
                                       default=df["market"].unique())

with province:
    province_filter = province.multiselect(
        "Województwa", options=df["province"].unique(),
        default=df["province"].unique())

df = df[(df["utc_created_at"].dt.date <= max_created_filter) &
        (df["utc_created_at"].dt.date >= min_created_filter) &
        (df["price"] >= min_price_filter) &
        (df["price"] <= max_price_filter) &
        (df["house_area"] <= max_area_filter) &
        (df["house_area"] >= min_area_filter) &
        (df["market"].isin(market_filter))]


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
        fig_map = plot_map(df)
        st.components.v1.html(fig_map._repr_html_(), width=1100, height=1200)

else:
    st.markdown("Nie ma żadnych ofert, które spełniają kryteria")
