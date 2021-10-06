import dash
import dash_html_components as html 
import dash_core_components as dcc
import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as px


app = dash.Dash(__name__)

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')
all_options = {
    'США': ['Нью-Йорк', 'Сан-Франциско', 'Вашингтон'],
    'России': ['Москва', 'Новосибирск', 'Питер']
}

app.layout = html.Div([
    html.H1('My first app!'),
    html.H2('Простой график'),
    html.Div(className='scatter-sample',children=[
        dcc.Graph(
            figure={
                'data': [
                    {'x': [1, 2], 'y': [3, 1]}
                ]
            },
        )
    ]),
    html.H2('CallBacks'),
    html.Div(
        className="scatter",
        children=[
            dcc.Graph(id = 'my_graph'), 
            html.Div(
                className='slider',
                children=[
                    dcc.Slider(
                        id = 'my_slider',
                        min = df['year'].min(),
                        max = df['year'].max(),
                        value = df['year'].min(),
                        marks = {str(year) : str(year) for year in df['year'].unique()},
                        step=None
                    )
                ]
            ),
        ]
    ),
    html.H2('Взаимосвязанные обратные вызовы'),
    html.Div([
        dcc.RadioItems(
            id='countries-radio',
            options=[{'label': k, 'value': k} for k in all_options.keys()],
            value='США'
        ),
        html.Hr(),
        dcc.RadioItems(id='cities-radio'),
        html.Hr(),
        html.Div(id='display-selected-values')
    ]) 
])

#callbacks для графика 
@app.callback(
    Output('my_graph', 'figure'),
    [Input('my_slider', 'value')])
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]
    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                     size="pop", color="continent", hover_name="country",
                     log_x=True, size_max=55)
    return fig


#взаимосвязанные обратные вызовы
@app.callback(
    Output('cities-radio', 'options'),
    [Input('countries-radio', 'value')])
def set_cities_options(selected_country):
    return [{'label': i, 'value': i} for i in all_options[selected_country]]
@app.callback(
    Output('cities-radio', 'value'),
    [Input('cities-radio', 'options')])
def set_cities_value(available_options):
    return available_options[0]['value']
@app.callback(
    Output('display-selected-values', 'children'),
    [Input('countries-radio', 'value'),
     Input('cities-radio', 'value')])
def set_display_children(selected_country, selected_city):
    return '{} - это город {}'.format(
        selected_city, selected_country,
    )

app.run_server(debug=True) 