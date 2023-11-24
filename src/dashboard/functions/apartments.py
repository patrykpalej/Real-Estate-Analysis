import folium
from branca.colormap import linear
from datetime import date
import plotly.subplots as sp
import plotly.graph_objects as go


color_1 = 'rgba(100, 149, 237, 0.6)'
color_2 = 'rgba(144, 238, 144, 0.6)'
color_3 = 'rgba(235, 202, 213, 0.6)'
color_4 = 'rgba(148, 137, 235, 0.6)'
color_5 = 'rgba(173, 216, 230, 0.6)'
color_6 = 'rgba(255, 228, 181, 0.6)'


def preprocess_apartments(df):
    columns = ["url", "price", "utc_created_at", "province", "latitude",
               "longitude", "build_year", "apartment_area", "build_year"]

    df = df[columns]
    df["price_per_m2"] = df["price"] / df["apartment_area"]

    return df
