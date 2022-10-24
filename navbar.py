import dash_bootstrap_components as dbc
def Navbar():
    navbar = dbc.Nav(
           [
                dbc.NavLink("Match-Arbitrage", href="/match"),
                dbc.NavLink("Tournament Arbitrage", href="/tournament"),
                dbc.NavLink("Best Odds", href="/best_odds"),
                dbc.NavLink("Betting Sites Sign Ups", href="/sign-ups"),
                dbc.NavLink("Donate", href="/donate"),
              
                    ],
          vertical=False,
          justified=True,
          pills=True,
          style={'color' : 'blue'}
        )
    return navbar