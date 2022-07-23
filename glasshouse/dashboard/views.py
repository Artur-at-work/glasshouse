from django.shortcuts import render
from dashboard.plots import plot_price_history

def price_history(request):
    plotly_plot_obj = plot_price_history()
    return render(request, "price_history.html", context={'plot_div': plotly_plot_obj})
