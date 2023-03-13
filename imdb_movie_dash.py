# IMDB MOVIE DASHBOARD

# This program build a dashboard using dash e plotly to view and analyze IMDb Top 250 films.
# IMDb (Internet Movie Database) is an online database of information related to films, television series, 
# podcasts, home videos, video games, and streaming content online – including cast, production crew 
# and personal biographies, plot summaries, trivia, ratings, and fan and critical reviews.

# With this work, we intend to aswer some questions:
# 1. Is there any relationship between a movie's relase date and its gross?
# 2. What about the amount of rating and votes quantity?
# 3. What are the favorite movie genres?
# 4. What are the most popular film directors?
# 5. What are the most popular actors or actresses?


# Import modules:
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, dash_table, Input, Output
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
from plotly.subplots import make_subplots

# Getting data:
exec(open('imdb_movie_getdata.py').read())

## Data preprocess:

# Creating list of MOVIES:
movie_list = [x for x in df.movie_title]
movie_list.sort()
# Creating a df ordered by MOVIE_TITLE:
df_movie = df.sort_values('movie_title')

# Creating list of GENRES:
genres = [x.split(',') for x in df.genre]
genre_list=[]
for genre in genres:
    for element in genre:
        genre_list.append(element.lstrip(' ').rstrip(' '))
genre_list=sorted(set(genre_list))
genre_list.insert(0, 'All genres')

# Creating table of GENRES:
df_genre = df.loc[:,['movie_title','genre','rate','metascore','votes','gross']]
df_genre.loc[:, 'votes'] = df_genre['votes'].map('{:0,.0f}'.format)
df_genre.loc[:, 'gross'] = df_genre['gross'].map('$ {:0,.0f}M'.format)
df_genre = df_genre.reset_index(drop=True)

# Creating top 10 GENRE table:
genre_count = [df_genre[df_genre.genre.str.contains(i)].shape[0] for i in genre_list]
df_genre_count = pd.DataFrame({'genre_ord': genre_list,'count_genre': genre_count})
df_genre_count = df_genre_count.sort_values('count_genre',ascending=False).reset_index(drop=True)
df_genre_count = df_genre_count.loc[0:9,]

# Creating list of DIRECTORS:
directors = [x.split(',') for x in df.directors]
director_list=[]
for director in directors:
    for element in director:
        director_list.append(element.lstrip(' ').rstrip(' '))
director_list=sorted(set(director_list))
director_list.insert(0,'All directors')

# Creating table of DIRECTORS:
df_director = df.loc[:,['movie_title','directors','rate','metascore','votes','gross']]
df_director.loc[:, 'votes'] = df_director['votes'].map('{:0,.0f}'.format)
df_director.loc[:, 'gross'] = df_director['gross'].map('$ {:0,.0f}M'.format)
df_director = df_director.reset_index(drop=True)

# Creating top 10 DIRECTORS table:
director_count = [df_director[df_director.directors.str.contains(i)].shape[0] for i in director_list]
df_director_count = pd.DataFrame({'director_ord': director_list,'count_director': director_count})
df_director_count = df_director_count.sort_values('count_director',ascending=False).reset_index(drop=True)
df_director_count = df_director_count.loc[0:9,]

# Creating list of STARS:
stars = [x.split(',') for x in df.stars]
stars_list=[]
for star in stars:
    for element in star:
        stars_list.append(element.lstrip(' ').rstrip(' '))
stars_list=sorted(set(stars_list))
stars_list.insert(0,'All stars')

# Creating table of STARS:
df_stars = df.loc[:,['movie_title','stars','rate','metascore','votes','gross']]
df_stars.loc[:, 'votes'] = df_stars['votes'].map('{:0,.0f}'.format)
df_stars.loc[:, 'gross'] = df_stars['gross'].map('$ {:0,.0f}M'.format)
df_stars = df_stars.reset_index(drop=True)

# Creating top 10 STARS table:
stars_count = [df_stars[df_stars.stars.str.contains(i)].shape[0] for i in stars_list]
df_stars_count = pd.DataFrame({'stars_ord': stars_list,'count_stars': stars_count})
df_stars_count = df_stars_count.sort_values('count_stars',ascending=False).reset_index(drop=True)
df_stars_count = df_stars_count.loc[0:9,]

## Set style:

# Setting Darkly style:
dbc_css = 'https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css'
load_figure_template('darkly')

# Tabs styles:
tabs_styles = {'height':'32px','width':'400px','align-items':'center','border-radius':'4px'}

tab_style = {'background':'#133955','border-style':'solid','border-color':'grey',
             'border-radius':'4px','align-items':'center','padding':'5px','fontWeight':'bold'}

tab_selected_style = {'backgroundColor':'SlateGrey','border-style':'solid','border-color':'grey',
                      'border-radius':'4px','align-items':'center','color':'white','padding':'5px'}


# App Create:
app = Dash(__name__,external_stylesheets=[dbc.themes.DARKLY,dbc_css])

# Creating lay out:
app.layout = dbc.Container(html.Div(
    [dbc.Row(html.Br()),
     dbc.Row([
            dbc.Col(html.Div([html.H2('IMDB MOVIE DASHBOARD'),]),width={'size':8,'order':'first'}
                    ),
            dbc.Col(html.Div([html.Img(src='https://cdn-icons-png.flaticon.com/512/9126/9126790.png',
                                       alt='fig-header',width=50 ,height=50
                                       )]),width={'size':1,'order':'last'},align='right'
                    ),           
            ],justify='between'),
     dbc.Row([html.Hr(),
              dcc.Markdown('''
              This is a movie dashboard to view and analyze IMDb "Top 250" films.      
              [IMDb (Internet Movie Database)](https://www.imdb.com/) is an online database of 
              information related to films, television series, podcasts, home videos, video games, 
              and streaming content online, including cast, production crew and personal biographies, 
              plot summaries, trivia, ratings, and fan and critical 
              reviews. *[source: wikipedia](https://en.wikipedia.org/wiki/IMDb)*
              '''),
            ],className='dbc'),
     dbc.Row((html.Div([
                        html.H4('MOVIE CHARTS'),
                        html.Hr(),
                        dcc.Tabs([
                                dcc.Tab(label='Release Date x Gross', children=[
                                    html.Br(),
                                    dcc.Graph(id='graph_year_gross'),
                                    html.Br(),
                                    dcc.RangeSlider(1920,2030,10,value=[1990,2030],
                                                    id='slider_year_gross',
                                                    className='dbc',
                                                    marks={i: '{}'.format(i) for i in range(1920,2030,10)})
                                    ], style = tab_style, selected_style=tab_selected_style),
                                dcc.Tab(label='Rating x Votes Quantity', children=[
                                    html.Br(),
                                    dcc.Graph(id='graph_rate_votes'),
                                    html.Br(),
                                    dcc.RangeSlider(8.0,9.4,0.2,value=[8.8,9.4],
                                                    id='slider_rate_votes',
                                                    className='dbc')
                                    ], style = tab_style, selected_style=tab_selected_style)
                                ], style = tabs_styles)
                            ])
            )),html.Br(),
     dbc.Row((html.Div([
                        html.H4('MOVIE DETAILS'),
                        html.Hr(),
                        dcc.Dropdown(movie_list,'A Beautiful Mind',id='drop_movies',className='dbc'),
                        html.Br(),
                        dbc.Row([
                                dbc.Col(dbc.Card([
                                            dbc.Row([
                                                dbc.Col(dbc.CardImg(id='img_movie'),width=1),
                                                dbc.Col(dbc.CardBody([dbc.CardLink('A Beautiful Mind',
                                                                                   id='link_movie',
                                                                                   href=df_movie.link[0]),
                                                                    html.P(id='summary_movie')
                                                                    ]))],className="g-0 d-flex align-items-center")
                                                ])),
                                ]),
                        html.Br(),
                        dbc.Row([
                                dbc.Col(dbc.Card([dbc.CardHeader(html.P('RATE',style={'fontSize': 11}),
                                                                 className="card-title"),
                                                  dbc.CardBody(html.H6(id='rate_movie'),
                                                               className="card-text")])),
                                dbc.Col(dbc.Card([dbc.CardHeader(html.P('METASCORE',style={'fontSize': 11}),
                                                                 className="card-title"),
                                                  dbc.CardBody(html.H6(id='metascore_movie'),
                                                               className="card-text")])),
                                dbc.Col(dbc.Card([dbc.CardHeader(html.P('CERTIFICATE',style={'fontSize': 11}),
                                                                 className="card-title"),
                                                  dbc.CardBody(html.H6(id='certificate_movie'),
                                                               className="card-text")])),
                                dbc.Col(dbc.Card([dbc.CardHeader(html.P('RUNTIME',style={'fontSize': 11}),
                                                                 className="card-title"),
                                                  dbc.CardBody(html.H6(id='runtime_movie'),
                                                               className="card-text")])),
                                dbc.Col(dbc.Card([dbc.CardHeader(html.P('GROSS (M-USD)',style={'fontSize': 11}),
                                                                 className="card-title"),
                                                  dbc.CardBody(html.H6(id='gross_movie'),
                                                               className="card-text")])),
                                dbc.Col(dbc.Card([dbc.CardHeader(html.P('GENRE',style={'fontSize': 11}),
                                                                 className="card-title"),
                                                  dbc.CardBody(html.H6(id='genre_movie'),
                                                               className="card-text")]),width=4)
                                ],className='h-5'),
                        html.Br(),
                        dbc.Row([
                                dbc.Col(dbc.Card([dbc.CardHeader(html.P('DIRECTORS',style={'fontSize': 11}),
                                                                 className="card-title"),
                                                  dbc.CardBody(html.H6(id='directors_movie'),
                                                               className="card-text")]),width=4),
                                dbc.Col(dbc.Card([dbc.CardHeader(html.P('STARS',style={'fontSize': 11}),
                                                                 className="card-title"),
                                                  dbc.CardBody(html.H6(id='stars_movie'),
                                                               className="card-text")]),width=8)
                                ])
                        ]
                        )
            )
        ),html.Br(),    
     dbc.Row((html.Div([html.H4('TOPS ON TABS'),html.Hr()]))
        ),
     dbc.Row([
            dbc.Col(dcc.Tabs([
                        dcc.Tab(label='Genre', value='tab_genre', children=[
                            html.Br(),
                            dcc.Dropdown(genre_list,'All genres',id='drop_genre',className='dbc'),
                            html.Br(),
                            dash_table.DataTable(
                                data=df_genre.to_dict('records'),
                                columns=[{'name': i.upper(), 'id': i} for i in df_genre.columns],
                                id='table_genre',
                                style_table={'maxWidth': 700,'maxHeight': 370,
                                             'overflowX':'auto','overflowY':'auto'},
                                style_cell={'maxWidth': '140px','fontSize':11,'textAlign':'center',
                                            'backgroundColor': '#303030','whiteSpace':'normal'},
                                style_header={'color':'white','fontSize':11,
                                              'fontWeight':'bold','backgroundColor':'#24435c'}
                                ),
                                ],style = tab_style, selected_style=tab_selected_style),
                        dcc.Tab(label='Directors', value='tab_directors', children=[
                            html.Br(),
                            dcc.Dropdown(director_list,'All directors',id='drop_director',className='dbc'),
                            html.Br(),
                            dash_table.DataTable(
                                data=df_director.to_dict('records'),
                                columns=[{'name': i.upper(), 'id': i} for i in df_director.columns],
                                id='table_director',
                                style_table={'maxWidth': 700,'maxHeight': 370,
                                             'overflowX':'auto','overflowY':'auto'},
                                style_cell={'maxWidth': '140px','fontSize':11,'textAlign':'center',
                                            'backgroundColor': '#303030','whiteSpace':'normal'},
                                style_header={'color':'white','fontsize':11,
                                              'fontWeight':'bold','backgroundColor':'#24435c'}    
                                )
                                ],style = tab_style, selected_style=tab_selected_style),
                        dcc.Tab(label='Stars', value='tab_stars', children=[
                                html.Br(),
                                dcc.Dropdown(stars_list,'All stars',id='drop_stars',className='dbc'),
                                html.Br(),
                                dash_table.DataTable(
                                    data=df_stars.to_dict('records'),
                                    columns=[{'name': i.upper(), 'id':i} for i in df_stars.columns],
                                    id='table_stars',
                                    style_table={'maxWidth': 700,'maxHeight': 370,
                                                 'overflowX':'auto','overflowY':'auto'},
                                    style_cell={'maxWidth': '140px','fontSize':11,'textAlign':'center',
                                                'backgroundColor': '#303030','whiteSpace':'normal'},
                                    style_header={'color':'white','fontsize':11,
                                                  'fontWeight':'bold','backgroundColor':'#24435c'}                                                
                                    )
                                    ],style = tab_style, selected_style=tab_selected_style)
                                ],id='top_tabs', value='tab_genre', style = tabs_styles)
                    ),
            dbc.Col([html.P(id='top_text'),
                    dcc.Graph(id='top_graph')]
                    )
                 ]
                 ),html.Br()
]
),className='dbc'
)

## Callbacks:

# Update image movie:
@app.callback(
        Output('img_movie','src'),
        Input('drop_movies','value'))
def update_card_img_movie(value):
    src = df_movie.loc[df_movie.movie_title == value].image.reset_index(drop=True)[0]
    return src

# Update link movie name:
@app.callback(
        Output('link_movie','children'),
        Input('drop_movies','value'))
def update_card_link_movie_name(value):
    children = value
    return children

# Update link movie:
@app.callback(
        Output('link_movie','href'),
        Input('drop_movies','value'))
def update_card_link_movie(value):
    href = df_movie.loc[df_movie.movie_title == value].link.reset_index(drop=True)[0]
    return href

# Update summary movie:
@app.callback(
        Output('summary_movie','children'),
        Input('drop_movies','value'))
def update_card_summary_movie(value):
    children = df_movie.loc[df_movie.movie_title == value].summary.reset_index(drop=True)[0]
    return children

# Update rate movie card:
@app.callback(
        Output('rate_movie','children'),
        Input('drop_movies','value'))
def update_card_rate_movie(value):
    children = df_movie.loc[df_movie.movie_title == value].rate.reset_index(drop=True)[0]
    return children

# Update metascore movie card:
@app.callback(
        Output('metascore_movie','children'),
        Input('drop_movies','value'))
def update_card_metascore_movie(value):
    children = df_movie.loc[df_movie.movie_title == value].metascore.reset_index(drop=True)[0]
    return children

# Update certificate movie card:
@app.callback(
        Output('certificate_movie','children'),
        Input('drop_movies','value'))
def update_card_certificate_movie(value):
    children = df_movie.loc[df_movie.movie_title == value].certificate.reset_index(drop=True)[0]
    return children

# Update runtime movie card:
@app.callback(
        Output('runtime_movie','children'),
        Input('drop_movies','value'))
def update_card_runtime_movie(value):
    children = df_movie.loc[df_movie.movie_title == value].runtime.reset_index(drop=True)[0]
    return children

# Update gross movie card:
@app.callback(
        Output('gross_movie','children'),
        Input('drop_movies','value'))
def update_card_gross_movie(value):
    children = df_movie.loc[df_movie.movie_title == value].gross.reset_index(drop=True)[0]
    return children

# Update genre movie card:
@app.callback(
        Output('genre_movie','children'),
        Input('drop_movies','value'))
def update_card_genre_movie(value):
    children = df_movie.loc[df_movie.movie_title == value].genre.reset_index(drop=True)[0]
    return children

# Update directors movie card:
@app.callback(
        Output('directors_movie','children'),
        Input('drop_movies','value'))
def update_card_directors_movie(value):
    children = df_movie.loc[df_movie.movie_title == value].directors.reset_index(drop=True)[0]
    return children

# Update stars movie card:
@app.callback(
        Output('stars_movie','children'),
        Input('drop_movies','value'))
def update_card_stars_movie(value):
    children = df_movie.loc[df_movie.movie_title == value].stars.reset_index(drop=True)[0]
    return children

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

# Update GENDER table:
@app.callback(
    Output('table_genre','data'),
    Input('drop_genre','value')
)
def update_table_genre(value):
    if value == 'All genres':
        data=df_genre.to_dict('records')
    else:
        df_genre_filtered = df_genre[df_genre.genre.str.contains(str(value))].sort_values('rate', ascending=False)
        data=df_genre_filtered.to_dict('records')
    return data

# Update DIRECTOR table:
@app.callback(
    Output('table_director','data'),
    Input('drop_director','value')
)
def update_table_director(value):
    if value == 'All directors':
        data=df_director.to_dict('records')
    else:
        df_director_filtered = df_director[df_director.directors.str.contains(str(value))].sort_values('rate', ascending=False)
        data=df_director_filtered.to_dict('records')
    return data

# Update STARS table:
@app.callback(
    Output('table_stars','data'),
    Input('drop_stars','value')
)
def update_table_stars(value):
    if value == 'All stars':
        data=df_stars.to_dict('records')
    else:
        df_stars_filtered = df_stars[df_stars.stars.str.contains(str(value))].sort_values('rate', ascending=False)
        data=df_stars_filtered.to_dict('records')
    return data

# Update TOP Graph and Title:
@app.callback(
    Output('top_graph','figure'),
    Output('top_text','children'),
    Input('top_tabs','value')
)
def update_tops(value):
    if value == 'tab_genre':
        fig = px.bar(df_genre_count,x='count_genre',y='genre_ord',template='darkly')
        fig.update_layout(font_size=12,yaxis=dict(autorange="reversed"),yaxis_title=None,xaxis_title='Quantity of movies')
        fig.update_traces(hovertemplate='<b>Qty: %{x}</b>')
        children = 'TOP TEN GENRE'

    elif value == 'tab_directors':
        fig = px.bar(df_director_count,x='count_director',y='director_ord',template='darkly')
        fig.update_layout(font_size=12,yaxis=dict(autorange="reversed"),yaxis_title=None,xaxis_title='Quantity of movies')
        fig.update_traces(hovertemplate='<b>Qty: %{x}</b>')
        children = 'TOP TEN DIRECTORS'

    else:
        fig = px.bar(df_stars_count,x='count_stars',y='stars_ord',template='darkly')
        fig.update_layout(font_size=12,yaxis=dict(autorange="reversed"),yaxis_title=None,xaxis_title='Quantity of movies')
        fig.update_traces(hovertemplate='<b>Qty: %{x}</b>')
        children = 'TOP TEN STARS'

    return fig, children

if __name__ == '__main__':
    app.run_server(debug=True)