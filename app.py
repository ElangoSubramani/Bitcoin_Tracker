import dash
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import requests

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport','content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}])
server=app.server

coins = ["bitcoin", "ethereum", "binancecoin", "ripple"]
interval = 18000  
api_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"

def make_card(coin):
    change = coin["price_change_percentage_24h"]
    price = coin["current_price"]*83.42
    color = "danger" if change < 0 else "success"
    icon = "bi bi-arrow-down" if change < 0 else "bi bi-arrow-up"
    return dbc.Card(
        
      
        html.Div(
            [
                html.H4(
                    [
                        html.Img(src=coin["image"], height=35, className="me-1"),
                        coin["name"],
                    ]
                ),
                html.H4(f"₹{price:,.2f}"),
                html.H5(
                    [f"{round(change, 2)}%", html.I(className=icon), " 24hr"],
                    className=f"text-{color}",
                ),
            ],
            className=f"border-{color} border-start border-5",
        ),
        className="text-center text-nowrap my-2 p-2",
    )

interval = dcc.Interval(interval=interval)
cards = html.Div()

line_chart = dcc.Graph(id='line-chart')

line_chart_figure_data = {}  

def get_data():
    try:
        response = requests.get(api_url, timeout=1)
        return response.json()
    except requests.exceptions.RequestException as e:
       return None

app.layout = dbc.Container([dbc.Row(html.H1("BITCOIN TRACKING DASHBOARD")),interval, cards, line_chart, dbc.Row([
                
                html.A(

                        html.Img(
                            src="assets/1687361194136.jpg",  
                            height=100,  

                        ),
                   className="me1"),
                    html.P("""
                           Hii I'm Elango, This DashBoard was Developed using Plotly with Dash a python framework which triggers the data from api.coingecko.com API . This app is developed for Educational Purpose.
                        One can easily understand the Value of Bitcoin in INR  with the help of those KPIs and Line chart at Realtime(lively)
                        
                        I'm Passionate about data analysis and engineering, I can create custom data-driven web apps using python (Plotly with Dash) translating data into actionable insights.
1.)Data cleaning, processing and transformation
2.)Building customized analytic web apps and dashboards
3.)Mobile Application using Flutter Bloc.
                        
 Let's connect and innovate together!


                         """),
                         html.A(
                         html.H6("Git Hub: https://github.com/ElangoSubramani"),
                         href="https://github.com/ElangoSubramani",  # LinkedIn profile URL
                    target="_blank",
                         ),
            ])], className="my-5")

@app.callback([Output(cards, "children"), Output('line-chart', 'figure')], Input(interval, "n_intervals"))
def update_cards_and_chart(_):
    coin_data = get_data()
    if coin_data is None or type(coin_data) is dict:
        return dash.no_update, dash.no_update

    # Extract data for the selected coins
    selected_coin_data = {coin["id"]: coin for coin in coin_data if coin["id"] in coins}

    # Create cards and update data for the line chart
    coin_cards = []
    line_chart_data = []
    for coin_id, coin in selected_coin_data.items():
        coin_cards.append(make_card(coin))

        # Update or initialize data for the line chart
        if coin_id in line_chart_figure_data:
            line_chart_figure_data[coin_id]['x'].append(coin['last_updated'])
            line_chart_figure_data[coin_id]['y'].append(coin['current_price'])
        else:
            line_chart_figure_data[coin_id] = {
                'x': [coin['last_updated']],
                'y': [coin['current_price']],
                'mode': 'lines+markers',
                'name': coin['name']
            }

    # Make the card layout
    card_layout = [
        dbc.Row([dbc.Col(card, md=3) for card in coin_cards]),
        dbc.Row(dbc.Col(f"Last Updated {coin_data[0].get('last_updated')}")),
    ]

    # Create line chart layout
    line_chart_layout = go.Layout(
        title='Live Coin Prices',
        xaxis=dict(title='Timestamp'),
        yaxis=dict(title='Price (INR)'),
        showlegend=True
    )

    # Create line chart figure using updated data
    line_chart_figure = {'data': list(line_chart_figure_data.values()), 'layout': line_chart_layout}

    return card_layout, line_chart_figure

if __name__ == "__main__":
    app.run_server(port=8000, debug=False)
