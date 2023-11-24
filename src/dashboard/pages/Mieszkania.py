import streamlit as st

from dashboard.functions.apartments import *
from dashboard.main import df_apartments as df


st.set_page_config(layout="wide", page_title="Mieszkania")


with st.spinner('Ładowanie wykresów'):
    # Create plots
    # fig_all = plot_all(df)
    # fig_by_month = plot_by_month(df)
    # fig_by_province = plot_by_province(df)
    # fig_map = plot_map(df)

    st.title("Mieszkania")

    # st.plotly_chart(fig_all)
    # st.markdown("***")
    # st.plotly_chart(fig_by_month)
    # st.markdown("***")
    # st.plotly_chart(fig_by_province)
    # st.markdown("***")
    # st.components.v1.html(fig_map._repr_html_(), width=1100, height=1200)
