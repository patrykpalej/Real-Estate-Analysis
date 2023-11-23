import streamlit as st

from utils.storage import (get_credentials, generate_psql_connection_string,
                           read_from_db)
from dashboard.functions.lots import (preprocess_lots, plot_all,
                                      plot_by_location)


credentials = get_credentials()
connection_string = generate_psql_connection_string(*credentials)
df = read_from_db("SELECT * FROM otodom_lots", connection_string)
df = preprocess_lots(df)

fig_all = plot_all(df)
fig_by_location = plot_by_location(df)
# ---
st.set_page_config(
    layout="wide",
    page_title="Działki"
)

st.title("Działki")
st.plotly_chart(fig_all)

st.markdown("***")

st.plotly_chart(fig_by_location)

