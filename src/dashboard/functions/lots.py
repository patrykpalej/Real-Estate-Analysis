import numpy as np
import plotly.subplots as sp
import plotly.graph_objects as go


def preprocess_lots(df):
    columns = ["url", "price", "lot_area", "utc_created_at", "province",
               "location", "latitude", "longitude"]

    df = df[columns]
    df["price_per_m2"] = df["price"] / df["lot_area"]

    return df


def plot_all(df):
    titles = ["Powierzchnia działki [m2]", "Cena [zł]", "Cena za m2 [zł/m2]"]
    fig = sp.make_subplots(rows=1, cols=3, subplot_titles=titles)

    histogram1 = go.Histogram(x=df["lot_area"],
                              xbins=dict(start=1, end=2500, size=100),
                              marker=dict(color='rgba(100, 149, 237, 0.7)',
                                          line=dict(width=2, color="black")))

    histogram2 = go.Histogram(x=df["price"],
                              xbins=dict(start=1e4, end=25e4, size=1e4),
                              marker=dict(color='rgba(144, 238, 144, 0.7)',
                                          line=dict(width=2, color="black")))

    histogram3 = go.Histogram(x=df["price_per_m2"],
                              xbins=dict(start=0, end=350, size=10),
                              marker=dict(color='rgba(255, 182, 193, 0.7)',
                                          line=dict(width=2, color="black")))

    fig.add_trace(histogram1, row=1, col=1)
    fig.add_trace(histogram2, row=1, col=2)
    fig.add_trace(histogram3, row=1, col=3)

    for i in fig['layout']['annotations']:
        i['font'] = dict(size=24)

    fig.update_xaxes(range=[0, 2601], row=1, col=1)
    fig.update_xaxes(range=[0, 250001], row=1, col=2)
    fig.update_xaxes(range=[0, 351], row=1, col=3)

    fig.update_yaxes(title_text='', row=1, col=1,
                     title_font=dict(size=20))

    fig.update_layout(title_text='Dane całkowite', title_x=0.43,
                      showlegend=False, width=1450, title_font=dict(size=28))
    return fig


def plot_by_location(df):
    df_country = df[df["location"] == "country"]
    df_suburb = df[df["location"] == "suburban"]
    df_city = df[df["location"] == "city"]

    titles = ["Powierzchnia działki [m2]", "Cena [zł]", "Cena za m2 [zł/m2]"]
    fig = sp.make_subplots(rows=3, cols=3, subplot_titles=titles)

    hist1_1 = go.Histogram(x=df_country["lot_area"], name="Distribution",
                           xbins=dict(start=1, end=2500, size=100),
                           marker=dict(color='rgba(100, 149, 237, 0.7)',
                                       line=dict(color='black', width=2)))
    line1_1 = go.Scatter(x=[df_country["lot_area"].mean(),
                            df_country["lot_area"].mean()],
                         y=[0, np.histogram(df_country["lot_area"], range(1, 2500, 100))[0].max()/2],
                         mode='lines', name="Average",
                         line=dict(color='red', width=2)
    )

    hist1_2 = go.Histogram(x=df_country["price"], name="Distribution",
                           xbins=dict(start=1e4, end=25e4, size=1e4),
                           marker=dict(color='rgba(144, 238, 144, 0.7)',
                                       line=dict(color='black', width=2)))
    line1_2 = go.Scatter(x=[df_country["price"].mean(),
                            df_country["price"].mean()],
                         y=[0, np.histogram(df_country["price"], range(10000, 250000, 10000))[0].max()/2],
                         mode='lines', name="Average",
                         line=dict(color='red', width=2)
                         )

    hist1_3 = go.Histogram(x=df_country["price_per_m2"], name="Distribution",
                           xbins=dict(start=0, end=350, size=10),
                           marker=dict(color='rgba(255, 182, 193, 0.7)',
                                       line=dict(color='black', width=2)))
    line1_3 = go.Scatter(x=[df_country["price_per_m2"].mean(),
                            df_country["price_per_m2"].mean()],
                         y=[0, np.histogram(df_country["price_per_m2"], range(0, 350, 10))[0].max()/2],
                         mode='lines', name="Average",
                         line=dict(color='red', width=2)
                         )

    fig.add_trace(hist1_1, row=1, col=1)
    fig.add_trace(line1_1, row=1, col=1)

    fig.add_trace(hist1_2, row=1, col=2)
    fig.add_trace(line1_2, row=1, col=2)

    fig.add_trace(hist1_3, row=1, col=3)
    fig.add_trace(line1_3, row=1, col=3)

    hist2_1 = go.Histogram(x=df_suburb["lot_area"], name="Distribution",
                           xbins=dict(start=1, end=2500, size=100),
                           marker=dict(color='rgba(100, 149, 237, 0.7)',
                                       line=dict(color='black', width=2)))
    line2_1 = go.Scatter(x=[df_suburb["lot_area"].mean(),
                            df_suburb["lot_area"].mean()],
                         y=[0, np.histogram(df_suburb["lot_area"],
                                            range(1, 2500, 100))[0].max() / 2],
                         mode='lines', name="Average",
                         line=dict(color='red', width=2)
                         )

    hist2_2 = go.Histogram(x=df_suburb["price"], name="Distribution",
                           xbins=dict(start=1e4, end=25e4, size=1e4),
                           marker=dict(color='rgba(144, 238, 144, 0.7)',
                                       line=dict(color='black', width=2)))
    line2_2 = go.Scatter(x=[df_suburb["price"].mean(),
                            df_suburb["price"].mean()],
                         y=[0, np.histogram(df_suburb["price"],
                                            range(10000, 250000, 10000))[0].max() / 2],
                         mode='lines', name="Average",
                         line=dict(color='red', width=2)
                         )

    hist2_3 = go.Histogram(x=df_suburb["price_per_m2"], name="Distribution",
                           xbins=dict(start=0, end=350, size=10),
                           marker=dict(color='rgba(255, 182, 193, 0.7)',
                                       line=dict(color='black', width=2)))
    line2_3 = go.Scatter(x=[df_suburb["price_per_m2"].mean(),
                            df_suburb["price_per_m2"].mean()],
                         y=[0, np.histogram(df_suburb["price_per_m2"],
                                            range(0, 350, 10))[0].max() / 2],
                         mode='lines', name="Average",
                         line=dict(color='red', width=2)
                         )

    fig.add_trace(hist2_1, row=2, col=1)
    fig.add_trace(line2_1, row=2, col=1)

    fig.add_trace(hist2_2, row=2, col=2)
    fig.add_trace(line2_2, row=2, col=2)

    fig.add_trace(hist2_3, row=2, col=3)
    fig.add_trace(line2_3, row=2, col=3)

    hist3_1 = go.Histogram(x=df_city["lot_area"], name="Distribution",
                           xbins=dict(start=1, end=2500, size=100),
                           marker=dict(color='rgba(100, 149, 237, 0.7)',
                                       line=dict(color='black', width=2)))
    line3_1 = go.Scatter(x=[df_city["lot_area"].mean(),
                            df_city["lot_area"].mean()],
                         y=[0, np.histogram(df_city["lot_area"],
                                            range(1, 2500, 100))[0].max() / 2],
                         mode='lines', name="Average",
                         line=dict(color='red', width=2)
                         )

    hist3_2 = go.Histogram(x=df_city["price"], name="Distribution",
                           xbins=dict(start=1e4, end=25e4, size=1e4),
                           marker=dict(color='rgba(144, 238, 144, 0.7)',
                                       line=dict(color='black', width=2)))
    line3_2 = go.Scatter(x=[df_city["price"].mean(),
                            df_city["price"].mean()],
                         y=[0, np.histogram(df_city["price"],
                                            range(10000, 250000, 10000))[0].max() / 2],
                         mode='lines', name="Average",
                         line=dict(color='red', width=2)
                         )

    hist3_3 = go.Histogram(x=df_city["price_per_m2"], name="Distribution",
                           xbins=dict(start=0, end=350, size=10),
                           marker=dict(color='rgba(255, 182, 193, 0.7)',
                                       line=dict(color='black', width=2)))
    line3_3 = go.Scatter(x=[df_city["price_per_m2"].mean(),
                            df_city["price_per_m2"].mean()],
                         y=[0, np.histogram(df_city["price_per_m2"],
                                            range(0, 350, 10))[0].max() / 2],
                         mode='lines', name="Average",
                         line=dict(color='red', width=2)
                         )

    fig.add_trace(hist3_1, row=3, col=1)
    fig.add_trace(line3_1, row=3, col=1)

    fig.add_trace(hist3_2, row=3, col=2)
    fig.add_trace(line3_2, row=3, col=2)

    fig.add_trace(hist3_3, row=3, col=3)
    fig.add_trace(line3_3, row=3, col=3)

    fig.update_yaxes(title_text='Wieś', row=1, col=1, title_font=dict(size=20))
    fig.update_yaxes(title_text='Przedmieścia', row=2, col=1, title_font=dict(size=20))
    fig.update_yaxes(title_text='Miasto', row=3, col=1, title_font=dict(size=20))

    ylim_area = 1.05 * max([
        np.histogram(df_country["lot_area"], range(1, 2500, 100))[0].max(),
        np.histogram(df_suburb["lot_area"], range(1, 2500, 100))[0].max(),
        np.histogram(df_city["lot_area"], range(1, 2500, 100))[0].max()
    ])

    ylim_price = 1.05 * max([
        np.histogram(df_country["price"], range(10000, 250000, 10000))[0].max(),
        np.histogram(df_suburb["price"], range(10000, 250000, 10000))[0].max(),
        np.histogram(df_city["price"], range(10000, 250000, 10000))[0].max()
    ])

    ylim_price_per_m2 = 1.05 * max([
        np.histogram(df_country["price_per_m2"], range(0, 350, 10))[0].max(),
        np.histogram(df_suburb["price_per_m2"], range(0, 350, 10))[0].max(),
        np.histogram(df_city["price_per_m2"], range(0, 350, 10))[0].max()
    ])

    for r in range(1, 4):
        fig.update_xaxes(range=[0, 2601], row=r, col=1)
        fig.update_xaxes(range=[0, 250001], row=r, col=2)
        fig.update_xaxes(range=[0, 351], row=r, col=3)

        fig.update_yaxes(range=[0, ylim_area], row=r, col=1)
        fig.update_yaxes(range=[0, ylim_price], row=r, col=2)
        fig.update_yaxes(range=[0, ylim_price_per_m2], row=r, col=3)

    for i in fig['layout']['annotations']:
        i['font'] = dict(size=24)

    fig.update_layout(title_text='Podział na lokalizację', title_x=0.46,
                      width=1450, height=1100, showlegend=False,
                      title_font=dict(size=25))

    return fig
