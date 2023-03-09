# Questions:
# Quais generos aparecem mais entre os 250 top? Quais os genêros favoritos?
# Quais diretores aparecem em mais filmes? 
# Quais atores aparecem em mais filmes?
# Linha do tempo de lançamento dos top 20 filmes.
# Quais os 10 filmes com maior orçamento?


# Filmes com maior rating
# Filmes com maior metascore (nota geral da obra no Metacritic, um site que agrega as avaliações e notas de mídias especializadas.the metascore is a weighted average of many reviews coming from reputed critics. The Metacritic team reads the reviews and assigns each a 0–100 score, which is then given a weight, mainly based on the review’s quality and source.)
# Filmes com mais votos
# Quais filmes com maior duração
# Espaço para consulta



#Import modules:
from dash import Dash, html, dcc, dash_table, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from dash_bootstrap_templates import load_figure_template

# Getting data:
exec(open('imdb_movie_getdata.py').read())

# Incluir no file de getdata:
df.gross = df.gross.fillna(0)

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

# App Create:
app = Dash(__name__,external_stylesheets=[dbc.themes.DARKLY,dbc_css])

load_figure_template("darkly")

# Tabs styles:
tabs_styles = {
   'height': '32px', 
   'width': '500px',
    'align-items': 'center',
    'border-radius': '4px'
}

tab_style = {
    "background": "	#133955",
    'border-style': 'solid',
    'border-color': 'grey',
    'border-radius': '4px',
    'align-items': 'center',
    'padding': '5px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'backgroundColor': 'SlateGrey',
    'border-style': 'solid',
    'border-color': 'grey',
    'border-radius': '4px',
    'align-items': 'center',
    'color': 'white',
    'padding': '5px'
}



# Creating lay out:

app.layout = dbc.Container(html.Div(
    [dbc.Row([dbc.Col(html.Div([
                                html.Br(),
                                html.H1('IMDB MOVIE DASHBOARD'),
                                html.Hr(),
                                html.P('Um dashboard para análise e consulta de filmes avaliados no IMDB'),
                                html.Br()
                                ]
                                ),width=10
                    ),
              dbc.Col(html.Div([
                                html.Img(src='https://cdn-icons-png.flaticon.com/512/4618/4618701.png',
                                         alt='fig-header',width=90 ,height=90
                                         )
                                ]
                                ),width=2
                    )
            ]
            ),
     dbc.Row([dbc.Col(html.Div([
                                html.H4('RATING X VOTES'),
                                html.Hr(),
                                dcc.Graph(id='graph_rate_votes'),
                                html.Br(),
                                dcc.RangeSlider(8.0,9.4,0.2,value=[8.8,9.4],id='slider_rate_votes',className='dbc')
                                ]
                                ),width=6
                    ),
              dbc.Col(html.Div([
                                html.H4('RELEASE DATE X GROSS'),
                                html.Hr(),
                                dcc.Graph(id='graph_year_gross'),
                                html.Br(),
                                dcc.RangeSlider(1920,2030,10,value=[1960,2010],id='slider_year_gross',className='dbc',
                                                marks={i: '{}'.format(i) for i in range(1920,2030,10)})
                                ]
                                ),width=6
                    )
            ]
            ),html.Br(),
     dbc.Row([dbc.Col(html.Div([
                                html.H4('TOPS ON TABS'),
                                html.Hr(),
                                dcc.Tabs([
                                    dcc.Tab(label='Tab one', children=[
                                        html.H3('Conteúdo da tabela um'),
                                        dcc.Graph(id='graph1')
                                        ],style = tab_style, selected_style=tab_selected_style),
                                    dcc.Tab(label='Tab two', children=[
                                        html.H3('Conteúdo da tabela dois')
                                        ],style = tab_style, selected_style=tab_selected_style),
                                    dcc.Tab(label='Tab three', children=[
                                        html.H3('Conteúdo da tabela três')
                                        ],style = tab_style, selected_style=tab_selected_style)
                                    ], style = tabs_styles)
                                ]
                                )
                    ),
              dbc.Col(html.Div([
                                html.H2("MOVIE'S DETAILS"),
                                html.Hr()
                                ]
                                )
                    )
            ]
            )
]
),className='dbc'
)

# Update RATING X VOTES graph:
@app.callback(
    Output('graph_rate_votes', 'figure'), 
    Input('slider_rate_votes', 'value'))
def update_graph_rate_votes(value):
    df_votes = df[(df.rate>=value[0]) & (df.rate<=value[1])].sort_values('votes')
    subfig = make_subplots(specs=[[{"secondary_y": True}]])

    fig_line = px.line(df_votes, x='movie_title', y='rate', template='darkly')
    fig_area = px.area(df_votes, x='movie_title', y='votes', template='darkly')

    fig_line.update_traces(hovertemplate='<b>Rate:</b> %{y}', line_color='#FF7F50', line_width=1)
    fig_area.update_traces(yaxis="y2", hovertemplate='<b>Votes:</b> %{y:.0f}')

    subfig.add_traces(fig_line.data + fig_area.data)
    subfig.layout.yaxis.title='Rates'
    subfig.layout.yaxis2.title='Votes'
    subfig.update_xaxes(visible=False)
    subfig.update_layout(hovermode='x unified')

    return subfig


# Update RELEASE DATE X GROSS graph:
@app.callback(
    Output('graph_year_gross', 'figure'), 
    Input('slider_year_gross', 'value'))
def update_graph_year_gross(value):
    df_gross = df[(df.year>=value[0]) & (df.year<=value[1])].sort_values('gross')
    fig = px.scatter(df_gross, x='year', y='gross', 
                     color='gross', size='gross', template="darkly", custom_data=['movie_title'])
    fig.update_traces(hovertemplate='<b>Movie: %{customdata[0]}</b>'+'<br><b>Gross:</b> $ %{y}M'+'<br><b>Year:</b> %{x}')
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)