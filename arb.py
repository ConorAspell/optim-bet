import dash_bootstrap_components as dbc
import dash_html_components as html
import numpy as np
import pandas as pd
import dash_core_components as dcc
import dash_table
from database.database_methods import read_df, get_recommended_bets,transform_data_frame,transform_data_frame2
def arby(threed_df,twod_df):
    all_sites = list(threed_df.site_key.unique())
    df1,df2 = get_recommended_bets(twod_df,threed_df,all_sites)
    us_sites = list(threed_df.loc[threed_df.region=="eu"].site_key.unique())
    uk_sites = list(threed_df.loc[threed_df.region=="uk"].site_key.unique())

    us_sites = sorted(us_sites)
    uk_sites = sorted(uk_sites)
    ussites1 = [{'label': k, 'value': k} for k in us_sites]

    uksites1 = [{'label': k, 'value': k} for k in uk_sites]


    uschecklist=dcc.Checklist(options=ussites1,value=[],labelStyle={'display': 'inline-block','margin' : '5px'},id='ussites')
    ukchecklist=dcc.Checklist(options=uksites1,value=[],labelStyle={'display': 'inline-block','margin' : '5px'},id='uksites')


    arb= html.Div(children=[ 
        
        html.H4(children='Arbitrage Bets'),
        html.Div([
            html.H4('EU sites'),
            uschecklist,
            html.H4('UK sites'),
            ukchecklist,
            html.Button('Submit', id='submit-val', n_clicks_timestamp=-1),
            html.Div(id='container-button-basic',
                    children='Select Bet Providers and hit Submit')]
        ),
        html.H3(children='Edit the "Stake" Column to see exact bets and returns'),

        html.Div([
            dash_table.DataTable(
            id='bet-table',
            columns=[{"name": i, "id": i} for i in df2.columns if i not in ['league','away_amount','home_amount','draw_amount','home_profit',
        'away_profit', 'draw_profit']],
            data=df2.to_dict('records'),
            editable=True,
        )]),

        html.Div([
            dash_table.DataTable(
            id='bet-table-2',
            columns=[{"name": i, "id": i} for i in df1.columns if i not in ['league','away_amount','home_amount','home_profit','away_profit']],
            data=df1.to_dict('records'),
            editable=True,
        )])
        ])
    return arb