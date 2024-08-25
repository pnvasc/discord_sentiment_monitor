import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from flask import Flask
from .database import Session, Message
from sqlalchemy import func
from datetime import datetime, timedelta
from .user_segmentation import segment_users

server = Flask(__name__)
app = dash.Dash(__name__, server=server)

app.layout = html.Div([
    html.H1("Discord Sentiment App Dashboard", style={'textAlign': 'center'}),
    
    # First row
    html.Div([
        # First column of first row
        html.Div([
            dcc.Graph(id='sentiment-graph')
        ], className='six columns'),
        
        # Second column of first row
        html.Div([
            dcc.Graph(id='message-count-graph')
        ], className='six columns'),
    ], className='row'),
    
    # Second row
    html.Div([
        # First column of second row
        html.Div([
            dcc.Graph(id='user-segments-pie')
        ], className='six columns'),
        
        # Second column of second row
        html.Div([
            dcc.Graph(id='average-sentiment-graph')
        ], className='six columns'),
    ], className='row'),
    
    dcc.Interval(
        id='interval-component',
        interval=60*1000,  # 1 minute
        n_intervals=0
    )
], className='container')

@app.callback(Output('sentiment-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_sentiment_graph(n):
    session = Session()
    messages = session.query(Message).order_by(Message.timestamp.desc()).limit(100).all()
    df = pd.DataFrame([(msg.timestamp, msg.sentiment_score, msg.topic_category) for msg in messages],
                      columns=['Timestamp', 'Sentiment', 'Category'])
    session.close()

    fig = px.scatter(df, x='Timestamp', y='Sentiment', color='Category',
                     title='Sentiment and Category of Last 100 Messages')
    return fig

@app.callback(Output('message-count-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_message_count_graph(n):
    session = Session()
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    message_counts = session.query(func.date(Message.timestamp), func.count(Message.id)) \
                            .filter(Message.timestamp >= seven_days_ago) \
                            .group_by(func.date(Message.timestamp)) \
                            .all()
    session.close()

    df = pd.DataFrame(message_counts, columns=['Date', 'Count'])
    fig = px.bar(df, x='Date', y='Count', title='Number of Messages Over Last 7 Days')
    return fig

@app.callback(Output('user-segments-pie', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_user_segments_pie(n):
    segments = segment_users()
    df = pd.DataFrame([(segment, len(users)) for segment, users in segments.items()],
                      columns=['Segment', 'Count'])
    fig = px.pie(df, values='Count', names='Segment', title='User Segments')
    return fig

@app.callback(Output('average-sentiment-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_average_sentiment_graph(n):
    session = Session()
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    
    average_sentiments = session.query(
        func.date(Message.timestamp).label('date'),
        func.avg(Message.sentiment_score).label('avg_sentiment')
    ).filter(Message.timestamp >= seven_days_ago) \
     .group_by(func.date(Message.timestamp)) \
     .order_by('date') \
     .all()
    
    session.close()

    df = pd.DataFrame(average_sentiments, columns=['date', 'avg_sentiment'])
    
    fig = px.line(df, x='date', y='avg_sentiment', 
                  title='Average Sentiment Over Last 7 Days')
    
    # Customize y-axis
    fig.update_yaxes(
        title='Average Sentiment',
        tickvals=[-1, -0.5, 0, 0.5, 1],
        ticktext=['Very Negative', 'Negative', 'Neutral', 'Positive', 'Very Positive'],
        range=[-1.3, 1.3]
    )
    
    return fig

def run_dashboard(host='0.0.0.0', port=8050):
    app.run_server(host=host, port=port, debug=True, use_reloader=False)

if __name__ == '__main__':
    run_dashboard()
