# Data processing
import pandas as pd
import numpy as np
from datetime import datetime
from pandas import Series

# Visualization
import seaborn as sns
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objs as go

#import functions
from favorita.functions_model import grid_search, get_forecast, store_selection, regressor_delimitor


# preprocess for data viz
def preproc_viz(df, selected_store: int):
    #import data
    df= store_selection(selected_store)
    #adding temporal data
    df['ds'] = pd.to_datetime(df['ds'])
    df['week_day'] = df["ds"].dt.day_name()
    df['month']= df['ds'].dt.strftime('%B')
    df['année']= df['ds'].dt.strftime('%Y')
    df['quarter'] = df['ds'].dt.quarter

    return df

#get the monthly sales
def get_graph_monthly(df):
    #Total Monthly Sales
    fig, ax = plt.subplots(figsize=(14,5))
    palette = sns.color_palette("mako_r", 4)
    a = sns.barplot(x="month", y="y",data=df,hue = 'année',)
    a.set_title("Total Sales per months according years",fontsize=15)
    plt.legend(loc='upper right')
    plt.show()

    return fig

# get the top 5 products sales
def get_graph_highest(df):

    df = df.groupby('family').agg({"y" : "mean"}).reset_index().sort_values(by='y', ascending=False)[:5]

    fig = go.Figure(
        data=[go.Pie(
            values=df['y'], labels=df['family'], name='family',
            marker=dict(colors=['#334668','#496595','#6D83AA','#91A2BF','#C8D0DF']),
            hoverinfo='label+percent+value', textinfo='label'
            )],
        layout=go.Layout(title="Mix Top 5 Highest product sales")
        )

    # styling
    fig.update_yaxes(showgrid=False, ticksuffix=' ', categoryorder='total ascending')
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout(height=500, bargap=0.2,
                    margin=dict(b=0,r=20,l=20), xaxis=dict(tickmode='linear'),
                    title_text="Average Sales Analysis - Flop 5 products",
                    template="plotly_white",
                    title_font=dict(size=29, color='#8a8d93', family="Lato, sans-serif"),
                    font=dict(color='#8a8d93'),
                    hoverlabel=dict(bgcolor="#f2f2f2", font_size=13, font_family="Lato, sans-serif"),
                    showlegend=False)

    return fig

# get the flop 5 products sales
def get_graph_lowest(df):

     df = df.groupby('family').agg({"y" : "mean"}).reset_index().sort_values(by='y', ascending=True)[:5]

     fig = go.Figure(
        data=[go.Pie(
            values=df['y'], labels=df['family'], name='family',
            marker=dict(colors=['#B82E2E','#D62728','#E45756','#FFA15A','#FED4C4']),
            hoverinfo='label+percent+value', textinfo='label'
            )],
        layout=go.Layout(title="Mix Top 5 lowest product sales")
        )

    # styling
     fig.update_yaxes(showgrid=False, ticksuffix=' ', categoryorder='total ascending')
     fig.update_xaxes(visible=False)
     fig.update_yaxes(visible=False)
     fig.update_layout(height=500, bargap=0.2,
                      margin=dict(b=0,r=20,l=20), xaxis=dict(tickmode='linear'),
                      title_text="Average Sales Analysis - Top 5 products",
                      template="plotly_white",
                      title_font=dict(size=29, color='#8a8d93', family="Lato, sans-serif"),
                      font=dict(color='#8a8d93'),
                      hoverlabel=dict(bgcolor="#f2f2f2", font_size=13, font_family="Lato, sans-serif"),
                      showlegend=False)
     return fig
