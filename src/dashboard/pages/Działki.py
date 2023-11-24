import streamlit as st
from dashboard.functions.lots import (plot_all,
                                      plot_by_location, plot_by_month,
                                      plot_by_province, plot_map)
from dashboard.main import df_lots as df


st.set_page_config(layout="wide", page_title="Działki")


with st.spinner('Ładowanie wykresów'):
    fig_all = plot_all(df)
    fig_by_location = plot_by_location(df)
    fig_by_month = plot_by_month(df)
    fig_by_province = plot_by_province(df)
    fig_map = plot_map(df)

    st.title("Działki")

    st.plotly_chart(fig_all)
    st.markdown("***")
    st.plotly_chart(fig_by_month)
    st.markdown("***")
    st.plotly_chart(fig_by_province)
    st.markdown("***")
    st.components.v1.html(fig_map._repr_html_(), width=1100, height=1200)
