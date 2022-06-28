import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

from plotly.offline import plot
from plotly.graph_objects import Scatter
from django.db import connection

def plot_price_history():
    # direct call to Django SQLite
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM scrape_PriceHistory")
        row = cursor.fetchall()
    
    result_table = pd.DataFrame(row) # TODO: preserve column names
    print(list(result_table.columns))

    fig = px.line(result_table, x=2, y=1, color=3)
    fig.update_layout(title_text = 'Price History by House',
                      xaxis_title = 'Dates',
                      yaxis_title = 'Price')
    plotly_plot_obj = plot({'data': fig}, output_type='div')

    return plotly_plot_obj
