<img src="https://user-images.githubusercontent.com/44107852/225351489-5af6215f-5b7a-485e-9ee9-8296ce33daec.png" align="right"
     alt="imdb logo" width="90" height="60">     
# IMDb MOVIE DASHBOARD

<p align="center">
  <a href="#intro">Intro</a> •
  <a href="#how-it-works">How it works</a> •
  <a href="#building-and-running">Building and Running</a> •
  <a href="#how-to-use">How to use</a> •
  <a href="#notes-and-considerations">Notes and considerations</a> •
</p>

[gif]

## Intro 

[IMDb](https://www.imdb.com/) is one of the bigger online databases about Movies and everything releated 
to the Entertainment Industry. In addition to gathering information about cast and productions, the website
also allows users to create lists and rate their favorite movies.

The purpose of this project is to collect, process, view and analyze the **Top 250 movies on IMDB**. As so, this work was divided into two parts: **Web Scraping** and **Building Dashboard**.

In summary, some questions should be answered:  
* Is there any relationship between a movie's relase date and its gross earnings?
* What about the amount of rating and votes quantity?
* What are the favorite movie genres?
* What are the most popular film directors?
* What are the most popular actors or actresses?


## How it Works  

First of all, the program scrapes and preprocesses data from [Top 250 movies on IMDB](https://www.imdb.com/search/title/?groups=top_250&sort=user_rating) using the python language and the *requests* and *BeautifulSoup* libraries to get the website urls and collect information for each movie like: movie title, year of release, age classification, rating, metascore, directors, cast, gross earnings etc.

After, a Dashboard was built using the *Dash* and *Plotly* libraries and their Core, HTML and Bootstrap Components. With the analysis of the data obtained previously, graphs and visualizations were created to answer the initially defined questions.
 

## Building and Running

```
# Clone this repository:
git clone https://github.com/GiovannaBezerra/imdb_movie_dashboard.git

# Install development dependencies:
pip install pandas
pip3 install beautifulsoup4
pip install requests
pip install plotly
pip install dash
pip install dash-bootstrap-templates
pip install dash-bootstrap-components
```

After cloning the repository, two files must be saved: [imdb_movie_getdata.py](https://github.com/GiovannaBezerra/imdb_movie_dashboard/blob/main/imdb_movie_getdata.py), wich contains the source code to get data and [imdb_movie_dash.py](https://github.com/GiovannaBezerra/imdb_movie_dashboard/blob/main/imdb_movie_dash.py) wich contains the source code to build the dashboard.

To start the program, this last must be excecuted opening the python file in some IDE like VSCode, PyCharm and others.
... or use terminal to run the interactive program.   

![run_program](https://user-images.githubusercontent.com/44107852/225352197-f86f27e1-cfa4-41d1-bf01-c38d34a0fe8e.jpg)

The dashboard is now running and can be accessed by pointing a web browser at http://127.0.0.1:8050/.   

![run_program2](https://user-images.githubusercontent.com/44107852/225352283-32408af2-1ecf-499a-8000-172fd8bb97f5.jpg)   

![naveg_url](https://user-images.githubusercontent.com/44107852/225352368-020e63c9-c899-43ce-b9d9-b57153be6a0b.jpg)


## How to use

The **IMDb MOVIE DASHBOARD** can be accessed now.
![dash_init](https://user-images.githubusercontent.com/44107852/225352479-652a7e6f-91e5-4942-b4af-fd57c1629aca.jpg)

Navigate between tabs to view charts and analyze the relationship between movie release date and gross earning or rating value and number of votes.
[gif dos gráficos]

Select some film to view details like rating, metascore, classification, runtime, gross earning, genre, directors and star cast.
[gif dos cards dos filmes]

Navigate between Genre, Directors and Stars tabs to view the rank of favorites genres or the most popular directors and stars.
[gif dos tabs]


## Notes and Considerations

During the development of this program I had the opportunity to improve my web scrapping skills using the Bealtifulsoup and request libraries, as well as the Dash and Plotly libraries, particularly layout building and styling, and callbacks construction.
