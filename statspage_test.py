import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import sqlite3
import pandas as pd
import webbrowser
from threading import Timer
from datetime import datetime, timedelta
import base64

# Convert the image to base64
def image_to_base64(image_path):
    with open(image_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    return 'data:image/png;base64,{}'.format(encoded_image)

encoded_image = image_to_base64('data\streaks\streaks.png')
# Connect to the SQLite database
def fetch_data():
    conn = sqlite3.connect('cascade_project.db')
    
    subjects = pd.read_sql_query("SELECT subject FROM timer", conn)['subject'].tolist()
    time_spent = pd.read_sql_query("SELECT time FROM timer", conn)['time'].tolist()
    days = pd.read_sql_query("SELECT day FROM time_per_day ORDER BY day ASC", conn)['day'].tolist()
    time_per_day = pd.read_sql_query("SELECT time FROM time_per_day ORDER BY day ASC", conn)['time'].tolist()
    
    cursor = conn.cursor()
    most_studied_subject = cursor.execute("SELECT subject FROM timer ORDER BY time DESC LIMIT 1").fetchone()
    least_studied_subject = cursor.execute("SELECT subject FROM timer ORDER BY time LIMIT 1").fetchone()
    most_focused_day = cursor.execute("SELECT day FROM time_per_day ORDER BY time DESC LIMIT 1").fetchone()
    least_focused_day = cursor.execute("SELECT day FROM time_per_day ORDER BY time LIMIT 1").fetchone()
    most_efficient_day = cursor.execute('''SELECT 
        CASE strftime('%w', day)
            WHEN '0' THEN 'Sunday'
            WHEN '1' THEN 'Monday'
            WHEN '2' THEN 'Tuesday'
            WHEN '3' THEN 'Wednesday'
            WHEN '4' THEN 'Thursday'
            WHEN '5' THEN 'Friday'
            WHEN '6' THEN 'Saturday'
        END AS day_name
    FROM time_per_day;''').fetchone()
    
    streaks, longest_streak = calculate_streaks(days)
    
    return subjects, time_spent, days, time_per_day, most_studied_subject, least_studied_subject, most_focused_day, least_focused_day, most_efficient_day, streaks, longest_streak

def calculate_streaks(days):
    days = sorted([datetime.strptime(day, '%Y-%m-%d').date() for day in days])
    streaks = []
    current_streak = [days[0]]
    longest_streak = 1
    current_streak_length = 1
    
    for i in range(1, len(days)):
        if days[i] == days[i - 1] + timedelta(days=1):
            current_streak.append(days[i])
            current_streak_length += 1
        else:
            streaks.append(current_streak)
            if current_streak_length > longest_streak:
                longest_streak = current_streak_length
            current_streak = [days[i]]
            current_streak_length = 1
    
    streaks.append(current_streak)
    if current_streak_length > longest_streak:
        longest_streak = current_streak_length
    
    return streaks, longest_streak

subjects, time_spent, days, time_per_day, most_studied_subject, least_studied_subject, most_focused_day, least_focused_day, most_efficient_day, streaks, longest_streak = fetch_data()

# Ensure that the lengths of subjects and time_spent are the same
min_length = min(len(subjects), len(time_spent))
subjects = subjects[:min_length]
time_spent = time_spent[:min_length]

# Define colors for each bar
colors = ['#1f77b4', '#ee52ff', '#ff5263', '#ffee52', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']

# Create a Dash app
app = dash.Dash(__name__)

app.layout = html.Div(
    style={'backgroundColor': '#2D2F3A', 'color': '#FFFFFF', 'fontFamily': 'Arial'},
    children=[
        html.H1("Statistics Dashboard", style={'textAlign': 'center', 'padding': '20px'}),
        
        html.Div(
            style={'display': 'flex', 'justifyContent': 'space-around', 'padding': '20px'},
            children=[
                html.Div(
                    style={'flex': '1', 'margin': '10px', 'padding': '20px', 'backgroundColor': '#3E4155', 'borderRadius': '10px'},
                    children=[
                        html.H2("Hours Spent", style={'textAlign': 'center'}),
                        dcc.Graph(id='bar-chart-1', 
                                  figure=go.Figure(data=[
                                      go.Bar(
                                          x=subjects, 
                                          y=time_spent,
                                          marker_color=colors[:len(subjects)]  # Apply colors
                                      )
                                  ]).update_layout(title="", paper_bgcolor='#3E4155', plot_bgcolor='#3E4155', font=dict(color='#FFFFFF'))),
                    ]
                ),
                html.Div(
                    style={'flex': '1', 'margin': '10px', 'padding': '20px', 'backgroundColor': '#3E4155', 'borderRadius': '10px'},
                    children=[
                        html.H2("Most Focused", style={'textAlign': 'center'}),
                        dcc.Graph(id='bar-chart-2', 
                                  figure=go.Figure(data=[
                                      go.Bar(
                                          x=days, 
                                          y=time_per_day,
                                          marker_color=colors[:len(days)]  # Apply colors
                                      )
                                  ]).update_layout(title="", paper_bgcolor='#3E4155', plot_bgcolor='#3E4155', font=dict(color='#FFFFFF'))),
                    ]
                ),
            ]
        ),
        
        html.Div(
            style={'display': 'flex', 'justifyContent': 'space-around', 'padding': '20px'},
            children=[
                html.Div(
                    style={'flex': '1', 'margin': '10px', 'padding': '20px', 'backgroundColor': '#3E4155', 'borderRadius': '10px'},
                    children=[
                        html.H2("Study Streaks", style={'textAlign': 'center'}),
                        dcc.Graph(id='streak-chart', 
                                  figure=go.Figure(data=[
                                      go.Bar(
                                          x=[f'Streak {i+1}' for i in range(len(streaks))], 
                                          y=[len(streak) for streak in streaks],
                                          marker_color=[
                                              'orange' if len(streak) == longest_streak else '#5E5EEA' 
                                              for streak in streaks
                                          ],
                                          hovertext=[f"Start: {streak[0]}<br>End: {streak[-1]}" for streak in streaks],
                                          hoverinfo='text'
                                      )
                                  ]).update_layout(
                                      title="", 
                                      paper_bgcolor='#3E4155', 
                                      plot_bgcolor='#3E4155', 
                                      font=dict(color='#FFFFFF'),
                                      xaxis_title="Streak",
                                      yaxis_title="Days"
                                  )),
                        html.Div(
                            style={'textAlign': 'center', 'padding': '10px'},
                            children=[
                                html.Img(src=encoded_image, style={'width': '50px', 'height': '50px'}),
                                html.H3(f"{longest_streak} Days", style={'color': '#FF8C00'}),
                            ]
                        ),
                    ]
                ),
                html.Div(
                    style={'flex': '1', 'margin': '10px', 'padding': '20px', 'backgroundColor': '#3E4155', 'borderRadius': '10px'},
                    children=[
                        html.H2("Trends", style={'textAlign': 'center'}),
                        html.P(f"You are more efficient studying on {most_efficient_day[0] if most_efficient_day else 'N/A'}", style={'padding': '10px'}),
                        html.P("You have studied 0% more this Month.", style={'padding': '10px'}),
                        html.P("You have mastered 80% of calculus concepts.", style={'padding': '10px'}),
                        html.P("Your most focused time was in Week 9.", style={'padding': '10px'}),
                        html.P("You have spent most time studying ML.", style={'padding': '10px'}),
                    ]
                ),
                html.Div(
                    style={'flex': '1', 'margin': '10px', 'padding': '20px', 'backgroundColor': '#3E4155', 'borderRadius': '10px'},
                    children=[
                        html.H2("Quiz Scores", style={'textAlign': 'center'}),
                        dcc.Dropdown(
                            id='course-dropdown',
                            options=[{'label': subject, 'value': subject} for subject in subjects],
                            value=subjects[0],
                            style={'color': '#000000'}
                        ),
                        html.Div(id='quiz-scores', style={'padding': '20px'}),
                    ]
                ),
            ]
        ),
        
        html.Div(
            style={'display': 'flex', 'justifyContent': 'space-around', 'padding': '20px'},
            children=[
                html.Div(
                    style={'flex': '1', 'margin': '10px', 'padding': '20px', 'backgroundColor': '#3E4155', 'borderRadius': '10px'},
                    children=[
                        html.H2("Summary", style={'textAlign': 'center'}),
                        html.P(f"Best Subject: {most_studied_subject[0] if most_studied_subject else 'N/A'}", style={'padding': '10px'}),
                        html.P(f"Most Improvement Needed: {least_studied_subject[0] if least_studied_subject else 'N/A'}", style={'padding': '10px'}),
                        html.P(f"Most Studied: {most_studied_subject[0] if most_studied_subject else 'N/A'}", style={'padding': '10px'}),
                    ]
                )
            ]
        )
    ]
)

@app.callback(
    Output('quiz-scores', 'children'),
    Input('course-dropdown', 'value')
)

def update_quiz_scores(selected_course):
    # Fetch quiz scores for the selected course from the database
    conn = sqlite3.connect('cascade_project.db')
    query = f"SELECT difficulty, question_limit, marks FROM quizzes WHERE course='{selected_course}'"
    quiz_data = pd.read_sql_query(query, conn)
    conn.close()

    # Define the style for the cells to add space between columns
    cell_style = {'padding': '10px'}

    # Create the HTML table
    return html.Table(
        children=[
            html.Tr([
                html.Th("Difficulty", style=cell_style),
                html.Th("Question Limit", style=cell_style),
                html.Th("Marks", style=cell_style)
            ])] +
            [html.Tr([
                html.Td(row['difficulty'], style=cell_style),
                html.Td(row['question_limit'], style=cell_style),
                html.Td(row['marks'], style=cell_style)
            ]) for index, row in quiz_data.iterrows()],
        style={'border-collapse': 'separate', 'border-spacing': '0 10px'}  # Add this line to add spacing between rows
    )

def open_browser():
    webbrowser.open_new("http://127.0.0.1:8050/")

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run_server(debug=True)
