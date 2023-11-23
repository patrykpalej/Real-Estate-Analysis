import streamlit as st
from streamlit_folium import st_folium

from utils.storage import (get_credentials, generate_psql_connection_string,
                           read_from_db)
from dashboard.functions.lots import (preprocess_lots, plot_all,
                                      plot_by_location, plot_by_month,
                                      plot_by_province, plot_map)


# Prepare data
credentials = get_credentials()
connection_string = generate_psql_connection_string(*credentials)
df = read_from_db("SELECT * FROM otodom_lots", connection_string)
df = preprocess_lots(df)

# Create plots
fig_all = plot_all(df)
fig_by_location = plot_by_location(df)
fig_by_month = plot_by_month(df)
fig_by_province = plot_by_province(df)
fig_map = plot_map(df)

# Page layout
st.set_page_config(
    layout="wide",
    page_title="Działki"
)

st.title("Działki")

st.plotly_chart(fig_all)
st.markdown("***")
st.plotly_chart(fig_by_location)
st.markdown("***")
st.plotly_chart(fig_by_month)
st.markdown("***")
st.plotly_chart(fig_by_province)
st.markdown("***")
# st_folium(fig_map, height=900, width=900)
st.components.v1.html(fig_map._repr_html_(), width=1100, height=1200)
