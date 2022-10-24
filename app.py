import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output

import dash_daq as daq
import dash_table

import dash_bootstrap_components as dbc
from database.database_methods import read_df, get_recommended_bets,transform_data_frame,transform_data_frame2
import datetime

from navbar import Navbar
from arb import arby
from best_odds import best_odds

import plotly.express as px

nav = Navbar()


header = html.H3(
    'Edit the Stake Column'
)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
threed_df = read_df('threed_data')
twod_df = read_df('twod_data')
tournament = read_df('tournaments')
threed_df['match'] = threed_df['home_team'] + " v " + threed_df['away_team'] + " " +threed_df['league'].str.replace('_', ' ')


match_df = threed_df.drop_duplicates(subset=['home_team', 'away_team', 'site_key'])
home = match_df.sort_values(by=['home_team_odds'],ascending=False)
away = match_df.sort_values(by=['away_team_odds'],ascending=False)
draw = match_df.sort_values(by=['draw_odds'],ascending=False)



content = html.Div(id="page-content", children=[])

def Homepage():
    layout = html.Div([
    dcc.Location(id="url"),
    nav,
    content
    ])
    return layout

app = dash.Dash(__name__,suppress_callback_exceptions=True, external_stylesheets = [dbc.themes.UNITED])
app.layout = Homepage()
server = app.server


@app.callback(
    Output('bet-table', 'data'),
    Input('bet-table', 'data'),
    Input('bet-table', 'columns'),
    [dash.dependencies.Input('submit-val', 'n_clicks_timestamp')],
    [dash.dependencies.State('uksites', 'value')],
    [dash.dependencies.State('ussites', 'value')],
    prevent_initial_call=True
    )
def display_output(rows, columns,n_clicks_timestamp,value,value2):
    value.extend(value2)

    df2 = transform_data_frame(threed_df,value)
    if df2.empty:
        return df2.to_dict(orient="records")
    
    df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
    if df.empty:
        df = df2
    common_cols = ['away_team_odds', 'draw_odds', 'home_team_odds',
       'away_site', 'away_team', 'draw_site',
       'home_site', 'home_team'
       ]
    df=df.dropna()
    if datetime.datetime.now().timestamp() - (n_clicks_timestamp/1000) <2: 
        df.stake = 0
    else:
        df2 = df2[df2['away_team'].isin(df['away_team'])].dropna()
        df2.reset_index(inplace=True)
        df2.drop(columns=['index'],inplace=True)
        if not df[common_cols].equals(df2[common_cols]) and df.shape[0] == df2.shape[0]:
            df[common_cols] = df2[common_cols]
            df=df.dropna()
            return df.to_dict(orient="records")
    

    df2.stake = df.stake
    df =df2
    df.stake.replace('\D+', np.nan,regex=True,inplace=True)
    df=df.fillna(0)
    df.stake= df.stake.astype('float64')
    df.home_bet= df.home_bet.astype('float64')
    df.away_bet= df.away_bet.astype('float64')
    df.draw_bet= df.draw_bet.astype('float64')
    df['home_bet'] = round(df['stake'] * df2['home_amount'],2)
    df['away_bet'] = round(df['stake'] * df2['away_amount'],2)
    df['draw_bet'] = round(df['stake'] * df2['draw_amount'],2)
    df['home_return'] = round(df['stake'] * df2['home_profit'],2)
    df['away_return'] = round(df['stake'] * df2['away_profit'],2)
    df['draw_return'] = round(df['stake'] * df2['draw_profit'],2)
    return df.to_dict(orient="records")

@app.callback(
    Output('bet-table-2', 'data'),
    Input('bet-table-2', 'data'),
    Input('bet-table-2', 'columns'),
    [dash.dependencies.Input('submit-val', 'n_clicks_timestamp')],
    [dash.dependencies.State('uksites', 'value')],
    [dash.dependencies.State('ussites', 'value')],
    prevent_initial_call=True
    )
def display_output_2(rows, columns,n_clicks_timestamp,value,value2):
    
    value.extend(value2)

    temp_df1 = transform_data_frame2(twod_df,value)
    if temp_df1.empty:
        return temp_df1.to_dict(orient="records")

    common_cols = ['away_team_odds', 'home_team_odds',
    'away_site', 'away_team', 
    'home_site', 'home_team'
    ]
    df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
    if df.empty:
        df = temp_df1
    df=df.dropna()
    
    temp_df1 = temp_df1[temp_df1['away_team'].isin(temp_df1['away_team'])].dropna()
    temp_df1.reset_index(inplace=True)
    temp_df1.drop(columns=['index'],inplace=True)
    if not df[common_cols].equals(temp_df1[common_cols]) and df.shape[0] == temp_df1.shape[0]:
        df[common_cols] = temp_df1[common_cols]
        df=df.dropna()
        return df.to_dict(orient="records")
    if datetime.datetime.now().timestamp() - (n_clicks_timestamp/1000) <10: 
        df.stake = 0

    temp_df1.stake = df.stake
    df =temp_df1
    df.stake.replace('\D+', np.nan,regex=True,inplace=True)
    df.stake=df.stake.fillna(0)
    df.stake= df.stake.astype('float64')
    df.home_bet= df.home_bet.astype('float64')
    df.away_bet= df.away_bet.astype('float64')
    temp_df1.away_amount= temp_df1.away_amount.astype('float64')
    temp_df1.home_amount= temp_df1.home_amount.astype('float64')
    temp_df1.reset_index(inplace=True) 
    df.reset_index(inplace=True)
    df.drop(columns=['index'],inplace=True)
    df['home_bet'] = round(df['stake'] * temp_df1['home_amount'],2)
    df['away_bet'] = round(df['stake'] * temp_df1['away_amount'],2)
    df['home_return'] = round(df['stake'] * temp_df1['home_profit'],2)
    df['away_return'] = round(df['stake'] * temp_df1['away_profit'],2)

    return df.to_dict(orient="records")

@app.callback(
    Output("home_graph", "figure"), 
    [Input("best_dropdown", "value")])
def update_home_bar_chart(match):
    data = home.loc[home.match==match]
    fig=px.bar(data, x='site_key',
                         y="home_team_odds", labels={'home_team_odds':data.home_team.iat[0] + " odds",'site_key' : 'Bet Provider'})
    return fig

@app.callback(
    Output("away_graph", "figure"), 
    [Input("best_dropdown", "value")])
def update_away_bar_chart(match):
    data = away.loc[away.match==match]
    fig=px.bar(data, x='site_key',
                         y="away_team_odds", labels={'away_team_odds':data.away_team.iat[0] + " odds",'site_key' : 'Bet Provider'})
    return fig

@app.callback(
    Output("draw_graph", "figure"), 
    [Input("best_dropdown", "value")])
def update_draw_bar_chart(match):
    data = draw.loc[draw.match==match]
    fig=px.bar(data, x='site_key',
                         y="draw_odds", labels={'site_key' : 'Bet Provider'})
    return fig
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return [
                html.H1('Kindergarten in Iran',
                        style={'textAlign':'center'}),
                
                ]
    elif pathname == "/match":
        return arby(threed_df, twod_df)

    elif pathname == "/best_odds":
        return best_odds(threed_df, twod_df)

    elif pathname == "/sign-ups":
        return [
                html.H1('SIGN UPS',
                        style={'textAlign':'center'}),
                
                ]
    elif pathname == "/donate":
        return [
                html.H1('DONATE',
                        style={'textAlign':'center'}),
                
                ]
    elif pathname == "/tournament":
        return [
                html.H1('TOURNAMENT',
                        style={'textAlign':'center'}),]
                
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == '__main__':
    app.run_server(debug=True)