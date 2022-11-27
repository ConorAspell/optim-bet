import requests
import json
import pandas as pd
import numpy as np
import boto3

s3_client = boto3.client('s3')

def read_df(key):
    bucket_name= 'optim-bet-bucket'
    data = s3_client.get_object(Bucket=bucket_name, Key=key)
    # data = requests.get('https://kjgumdk8w4.execute-api.eu-west-1.amazonaws.com/test2/test?table_name=' + table)
    # data = data.json()
    # data = data['body']
    # data=pd.DataFrame(data)
    return pd.read_csv(data['Body'], sep=',')
    


def general_spread(odds):
    spends = []
    returns = []
    for i in range(0, len(odds)):
        spends.append(1/odds[i])
        returns.append(1/odds[i] * odds[i])
    if sum(spends) <=1:
        leftover = 1 - sum(spends)
        spends[spends.index(max(spends))]+=leftover
        return spends

def transform_data_frame(df,sites):
    if len(sites) > 0:
    # sites = ['paddypower', 'williamhill', 'betvictor','matchbook', 'betfair', 'betfred', 'ladbrokes', 'quinn_bet', 'boyle_sports', 'onexbet', 'cbet']
        df =df.loc[df['site_key'].isin(sites)]
    else:
        return pd.DataFrame()
    grouped_df = df.groupby(["home_team", "away_team", "league"]).agg({"home_team_odds": max,"away_team_odds": max,"draw_odds": max})
    cols = df.columns.to_list().extend(['home_amount', 'away_amount', 'draw_amount'])
    test_df = pd.DataFrame(columns=cols )
    
    for x in grouped_df.iterrows():
        bets = general_spread([x[1]['home_team_odds'], x[1]['away_team_odds'], x[1]['draw_odds']])
        if bets:
            x[1]['home_amount'] = bets[0]
            x[1]['away_amount'] = bets[1]
            x[1]['draw_amount'] = bets[2]
            x[1]['home_team'] = x[0][0]
            x[1]['away_team'] = x[0][1]
            x[1]['league'] = x[0][2]
            
            df2 = df.loc[((df.away_team==x[0][1]) & (df.home_team==x[0][0]))].fillna(0)
            home_df = df2.loc[(df2.home_team_odds == max(df2.home_team_odds))]
            away_df = df2.loc[ (df2.away_team_odds == max(df2.away_team_odds)) ]
            draw_df = df2.loc[ (df2.draw_odds == max(df2.draw_odds)) ]
            x[1]['home_site'] = home_df['site_key'].iloc[0]
            x[1]['away_site'] = away_df['site_key'].iloc[0]
            x[1]['draw_site'] = draw_df['site_key'].iloc[0]

            test_df = test_df.append(x[1])
    
   
    test_df['home_profit'] = test_df['home_team_odds'] * test_df['home_amount']
    test_df['away_profit'] = test_df['away_team_odds'] * test_df['away_amount']
    test_df['draw_profit'] = test_df['draw_odds'] * test_df['draw_amount']
    test_df.reset_index(drop=True, inplace=True)

    test_df['stake'] = 0
    test_df['home_bet'] = 0
    test_df['away_bet'] = 0
    test_df['draw_bet'] = 0
    test_df['home_return'] = 0
    test_df['away_return'] = 0
    test_df['draw_return'] = 0

    test_df = test_df[['stake', 'home_bet', 'away_bet', 'draw_bet','home_return', 'away_return', 'draw_return','away_team_odds', 'draw_odds', 'home_team_odds', 'away_amount',
       'away_site', 'away_team', 'draw_amount', 'draw_site', 'home_amount',
       'home_site', 'home_team', 'league', 'home_profit', 'away_profit',
       'draw_profit']]

    return test_df

def transform_data_frame2(df,sites):
    if len(sites) > 0:
        df =df.loc[df['site_key'].isin(sites)]
    else:
        return pd.DataFrame()
    grouped_df = df.groupby(["home_team", "away_team", "league"]).agg({"home_team_odds": max,"away_team_odds": max})
    cols = df.columns.to_list()
    cols.extend(['home_amount', 'away_amount'])
    test_df = pd.DataFrame(columns=cols )
    
    for x in grouped_df.iterrows():
        bets = general_spread([x[1]['home_team_odds'], x[1]['away_team_odds']])
        if bets:
            x[1]['home_amount'] = bets[0]
            x[1]['away_amount'] = bets[1]
            x[1]['home_team'] = x[0][0]
            x[1]['away_team'] = x[0][1]
            x[1]['league'] = x[0][2]
            df2 = df.loc[((df.away_team==x[0][1]) & (df.home_team==x[0][0]))]
            home_df = df2.loc[(df2.home_team_odds == max(df2.home_team_odds))]
            away_df = df2.loc[ (df2.away_team_odds == max(df2.away_team_odds))]
            x[1]['home_site'] = home_df['site_key'].iloc[0]
            x[1]['away_site'] = away_df['site_key'].iloc[0]
            x[1]['last_update'] = away_df['last_update'].iloc[0]
            x[1]['region'] = away_df['region'].iloc[0]

            test_df = test_df.append(x[1])
    test_df['home_profit'] = test_df['home_team_odds'] * test_df['home_amount']
    test_df['away_profit'] = test_df['away_team_odds'] * test_df['away_amount']
    test_df.reset_index(drop=True, inplace=True)
    test_df=test_df.drop(['site_key', 'h2h'], axis=1)

    test_df['stake'] = 0
    test_df['home_bet'] = 0
    test_df['away_bet'] = 0
    test_df['home_return'] = 0
    test_df['away_return'] = 0

    test_df = test_df[['stake', 'home_bet', 'away_bet', 'home_return', 'away_return', 'away_team_odds',  'home_team_odds', 'away_amount',
       'away_site', 'away_team',  'home_amount','home_site', 'home_team', 'league', 'home_profit', 'away_profit']]
    return test_df

def get_recommended_bets(df1,df2,sites=[]):

    # df1 = read_df('twod_data')
    # df2 = read_df('threed_data')
    df1 = transform_data_frame2(df1,sites)
    df2 = transform_data_frame(df2,sites)
    return df1, df2


