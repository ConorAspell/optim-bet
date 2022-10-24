import dash_bootstrap_components as dbc
import dash_html_components as html
import numpy as np
import pandas as pd
import dash_core_components as dcc
import dash_table
from database.database_methods import read_df, get_recommended_bets,transform_data_frame,transform_data_frame2
import plotly.express as px

def best_odds(threed_df,twod_df):
    all_matches = threed_df.match.unique()
    # threed_df['match'] = threed_df['home_team'] + " v " + threed_df['away_team'] + " " +threed_df['league'].str.replace('_', ' ')
    # all_matches = threed_df.match.unique()
    # df = threed_df.loc[threed_df.home_team=="Colorado Rapids"]
    # df = df.drop_duplicates(subset=['home_team', 'away_team', 'site_key'])
    # home = df.sort_values(by=['home_team_odds'],ascending=False)
    # away = df.sort_values(by=['away_team_odds'],ascending=False)
    # draw = df.sort_values(by=['draw_odds'],ascending=False)
    # html.Div(id='dd-output-container')
    content= html.Div(children=[         
            dcc.Dropdown(
        id="best_dropdown",
        options=[{"label": x, "value": x} for x in all_matches],
        value=all_matches[0],
        clearable=False,
    ),
    dcc.Graph(id="home_graph"),
    dcc.Graph(id="away_graph"),
    dcc.Graph(id="draw_graph")])
        # dcc.Graph(id='home_graph',
        #                  figure=px.bar(home, x='site_key',
        #                  y="home_team_odds", labels={'home_team_odds':home.home_team.iat[0] + " odds",'site_key' : 'Bet Provider'})),
                
        # dcc.Graph(id='away_graph',
        #                  figure=px.bar(away,  x='site_key',
        #                  y="away_team_odds", labels={'away_team_odds':away.away_team.iat[0] + " odds", 'site_key' : 'Bet Provider'} )),
        # dcc.Graph(id='draw_graph',
        #                  figure=px.bar(draw,  x='site_key',
        #                  y="draw_odds", labels={'draw_odds':"draw odds",'site_key' : 'Bet Provider'}))
                
    return content
    