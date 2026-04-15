# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash()


df = pd.read_csv('data/formatted_data.csv')
df['Date'] = pd.to_datetime(df['Date'])
# df = df.sort_values(by='Date')
df = df.groupby("Date")["Sales"].sum().reset_index()



fig = px.line(df, x="Date", y="Sales")

app.layout = html.Div(children=[
    html.H1(children='Sales reports of "Pink Morsel" between 2018 and 2022'),

    # html.Div(children='''
    #     Dash: A web application framework for your data.
    # '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run(debug=True)
