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

# Getting data:
exec(open('imdb_movie_getdata.py').read())

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

# App Create:
app = Dash(__name__,external_stylesheets=[dbc.themes.DARKLY])

# Gráfico Rating x Votes:
df2=df.sort_values('votes')
df2=df2.reset_index(drop=True)

fig_rate_votes=make_subplots(specs=[[{"secondary_y": True}]])

fig_rate_votes.add_trace(
    go.Scatter(x=df2.movie_title,
               y=df2.votes, 
               name='Votes', 
               mode='lines', 
               hovertemplate=None,
               line=dict(width=0.5, color='#325d81'),
               stackgroup='one',
               opacity=0.8),
    secondary_y=True,
)


fig_rate_votes.add_trace(
    go.Scatter(x=df2.movie_title,
               y=df2.rate, 
               name='Rate', 
               mode='lines',
               hovertemplate=None,
               line=dict(width=0.5, color='#396a93'),
               stackgroup='one'
               ),
    secondary_y=False,
)

fig_rate_votes.update_layout(
    margin=dict(l=20, r=20, t=20, b=20),
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='#f2f2f2',
    autosize = False,
    width = 600,
    height = 400,
    font_family = 'Arial',
    font_color = 'White',
    font_size = 14,
    hovermode="x unified",
    hoverlabel=dict(font_color='gray'),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

fig_rate_votes.update_xaxes(visible=False)
fig_rate_votes.update_yaxes(title_text="<b>Rates</b>", secondary_y=False)
fig_rate_votes.update_yaxes(title_text="<b>Votes</b>", secondary_y=True)

# Grafico Year x Gross:
fig_year_gross = go.Figure()

df.gross = df.gross.fillna(0)
df3 = df.sort_values('gross')

fig_year_gross.add_trace(
    go.Scatter(
        x=df3.year, y=df3.movie_title,
        text = df.gross,
        hovertemplate = '<b>Gross:</b> $ %{text}M' + '<br><b>Year:</b> %{x}' + '<br><b>Title:<b> %{y}',
        mode = 'markers',
        marker = dict(color = df3.gross, 
                      size = df3.gross, 
                      sizemode = 'area', 
                      sizeref = 2.*max(df3.gross)/(50.**2),
                      showscale=True)
    ))

fig_year_gross.update_xaxes(nticks=20)
fig_year_gross.update_yaxes(visible=False)

fig_year_gross.update_layout(
    margin=dict(l=20, r=20, t=20, b=20),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='SlateGrey',
    autosize = False,
    width = 600,
    height = 400,
    font_family = 'Arial',
    font_color = 'White',
    font_size = 14
)

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
                                html.H2('RATING X VOTES'),
                                html.Hr(),
                                dcc.Graph(figure=fig_rate_votes),
                                dcc.Slider(0, 250, 50, value = 50, className="mt-4")
                                ]
                                )
                    ),
              dbc.Col(html.Div([
                                html.H2('TOPS ON TABS'),
                                html.Hr(),
                                dcc.Tabs([
                                    dcc.Tab(label='Tab one', children=[
                                        html.H3('Conteúdo da tabela um')
                                        ], style = tab_style, selected_style=tab_selected_style),
                                    dcc.Tab(label='Tab two', children=[
                                        html.H3('Conteúdo da tabela dois')
                                        ], style = tab_style, selected_style=tab_selected_style),
                                    dcc.Tab(label='Tab three', children=[
                                        html.H3('Conteúdo da tabela três')
                                        ], style = tab_style, selected_style=tab_selected_style)
                                    ], style = tabs_styles)
                                ]
                                )
                    )
            ]
            ),html.Br(),
     dbc.Row([dbc.Col(html.Div([
                                html.H2('RELEASE DATE X GROSS'),
                                html.Hr(),
                                dcc.Graph(figure=fig_year_gross),
                                dcc.Slider(1920, 2030, 20, value = 1920)
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
), className="dbc"
)

if __name__ == '__main__':
    app.run_server(debug=True)