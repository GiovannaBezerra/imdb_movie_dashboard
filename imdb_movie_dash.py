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

# Getting data:
exec(open('imdb_movie_getdata.py').read())


# App Create:
app = Dash(__name__,external_stylesheets=[dbc.themes.DARKLY])


# Creating lay out:

app.layout = dbc.Container(html.Div(
    [dbc.Row(html.Div([
                        html.H1('IMDB MOVIE DASHBOARD'),
                        html.Hr(),
                        html.P('Um dashboard para análise e consulta de filmes avaliados no IMDB'),
                        html.Br()
                        ]
                        )
            ),
     dbc.Row([dbc.Col(html.Div([
                                html.H2('RATING X VOTES'),
                                html.Hr(),
                                ]
                                )
                    ),
              dbc.Col(html.Div([
                                html.H2('TOPS ON TABS'),
                                html.Hr()
                                ]
                                )
                    )
            ]
            ),
     dbc.Row([dbc.Col(html.Div([
                                html.H2('RELEASE DATE X GROSS'),
                                html.Hr()
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
)
)

if __name__ == '__main__':
    app.run_server(debug=True)