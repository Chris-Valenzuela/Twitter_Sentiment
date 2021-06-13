import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
# from collections import deque

import sqlite3
import pandas as pd




app = dash.Dash(__name__)
app.layout = html.Div(
    [   html.H2('Live Twitter Sentiment'),
        dcc.Input(id='sentiment_term', value='twitter', type='text'),
        dcc.Graph(id='live-graph', animate=False),
        dcc.Interval(
            id='graph-update',
            interval=1*1000,
            n_intervals = 0
        ),
    ]
)
@app.callback(Output('live-graph', 'figure'),
            [Input(component_id='sentiment_term', component_property = 'value')],
            [Input('graph-update', 'n_intervals')])
def update_graph_scatter(sentiment_term, n_intervals):
    
    try:
        #every one second we are establishing a new connection. If you access it outside you will get Dash Thread errors
        # might not be the best way
        conn = sqlite3.connect('twitter.db')
        c = conn.cursor()

        # df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE '%Takeoff%' ORDER BY unix DESC LIMIT 1000", conn)
        # how to inject parameters to sqlite (avoid dumb responses)
        df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE ? ORDER BY unix DESC LIMIT 200", conn ,params=('%' + sentiment_term + '%',))
        df.sort_values('unix', inplace=True)
        df['date'] = pd.to_datetime(df['unix'], unit = 'ms')
        df.set_index('date', inplace=True)
        df['sentiment_smoothed'] = df['sentiment'].rolling(int(len(df)/5)).mean()
        df.dropna(inplace=True)

        # Resampling. this smoothes things out We really shouldn't be plotting more than a few hundred datapoints on a live graph, rendering this will significantly impact performance. 
        # One option we have is to use Pandas' resample. We could resample to one second with:
        # this basically takes the data we have at each second or given time for that search and finds the average (smooths it out). This really depends on how much tweets are outputted for that search
        df = df.resample('1min').mean()
        # print(df)
        
        # last 100 values
        # X = df.unix.values[-100:]
        X = df.index[-100:]
        Y = df.sentiment_smoothed.values[-100:]
        print(df)
        # print(df)


        # x = timestamp, y = sentiment smoothed via rolling mean in pandas 
  

        data = plotly.graph_objs.Scatter(
                x=list(X),
                y=list(Y),
                name='Scatter',
                mode= 'lines+markers'
                )

        return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                    yaxis=dict(range=[min(Y),max(Y)]),
                                                    title='Term: {}'.format(sentiment_term))}

    except Exception as e:
        with open('errors.txt','a') as f:
            f.write(str(e))
            f.write('\n')


if __name__ == '__main__':
    app.run_server(debug=True)


# so because this is a Live update you need to be running your database live to feed to your dash 