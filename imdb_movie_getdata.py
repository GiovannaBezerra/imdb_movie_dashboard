# Este programa coleta dados detalhados dos 250 filmes mais populares de acordo com a IMDB. Após o tratamento dos dados
# a informação fica disponível e organizada para que sejam criados diversos tipos de visualizações.

# Import modules:
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Building the soup constructor:
url = 'https://www.imdb.com/search/title/?groups=top_250&sort=user_rating'
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Creating empty lists to store values:
indexes = []
movies = []
links = []
years = []
certificates = []
genres = []
runtimes = []
rates = []
metascores = []
summaries = []
directors = []
stars = []
votes = []
gross = []
rank = []
images = []

# Getting page 1:
headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3538.102 Safari/537.36 Edge/18.19582"
}
url = 'https://www.imdb.com/search/title/?groups=top_250&sort=user_rating'
response = requests.get(url,headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Splitting movies by content:
movie_content = soup.find_all('div', class_ = 'lister-item mode-advanced')

# Getting data for each content:
for content in movie_content:
    # Getting the index:
    if content.h3.find('span', class_='lister-item-index') is not None:
        index = content.h3.find('span', class_='lister-item-index').text.strip('.')
        indexes.append(index)
    else:
        indexes.append("")
    
    # Getting Movie Title and Link:
    if content.h3.a is not None:
        movie = content.h3.a.text
        movies.append(movie)
        link = 'https://www.imdb.com'+ content.h3.a.get('href')
        links.append(link)
    else:
        movies.append("")
        links.append("")
        
    # Getting Year:
    if content.h3.find('span', class_='lister-item-year') is not None:
        year = content.h3.find('span', class_='lister-item-year').text.strip('()')
        years.append(year)
    else:
        years.append("")
    
    # Getting Certificate:
    if content.p.find('span', class_ = 'certificate') is not None:
        certificate = content.p.find('span', class_ = 'certificate').text
        certificates.append(certificate)
    else:
        certificates.append("")
    
    # Getting Run Time:
    if content.p.find('span', class_='runtime') is not None:
        runtime = content.p.find('span', class_='runtime').text
        runtimes.append(runtime)
    else:
        runtimes.append(runtime)
    
    # Getting Genre:
    if content.p.find('span', class_='genre') is not None:
        genre = content.p.find('span', class_='genre').text.strip()
        genres.append(genre)
    else:
        genres.append("")
    
    # Getting Rate:
    if content.strong is not None:
        rate = content.strong.text
        rates.append(rate)
    else:
        rates.append("")
    
    # Getting Metascore:
    if content.find('span', class_='metascore favorable') is not None:
        metascore = content.find('span', class_='metascore favorable').text
        metascores.append(metascore)
    else:
        metascores.append("")
        
    # Getting Summary:
    if content.find_all('p', class_='text-muted')[1] is not None:
        summary = content.find_all('p', class_='text-muted')[1].text.strip()
        summaries.append(summary)
    else:
        summaries.append("")
    
    # Getting Directors:
    if content.select('a[href*="_dr_"]') is not None:
        director = [x.text for x in content.select('a[href*="_dr_"]')]
        directors.append(director)
    else:
        directors.append("")
    
    # Getting Stars:
    if content.select('a[href*="_st_"]') is not None:
        star = [x.text for x in content.select('a[href*="_st_"]')]
        stars.append(star)
    else:
        stars.append("")


# Votes:
#conteudo.select('p[class~=sort-num_votes-visible] span[name~=nv]')[0]

# Gross:
#conteudo.select('p[class~=sort-num_votes-visible] span[name~=nv]')[1]

# Rank:
#conteudo.select('p[class~=sort-num_votes-visible] span[name~=nv]')[2]


# Images:
#conteudo.select('div.lister-item-image a')

df = pd.DataFrame({'index': indexes,'movie_title': movies,
                   'link': links,'year': years,
                   'certificate': certificates,'runtime': runtimes,
                   'genre': genres,'rate': rates,
                   'metascore':metascores,'summary':summaries,
                   'directors':directors,'stars':stars})

print(df.head())



