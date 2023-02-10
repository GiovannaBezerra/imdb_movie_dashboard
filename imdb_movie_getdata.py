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

# Index:
page_index = [a.text.strip('.') for a in soup.select('h3.lister-item-header span[class~=lister-item-index]')]
print(len(page_index))
print(page_index[0:5])

# Movies:
movies = [a.text.strip() for a in soup.select('h3.lister-item-header a')]
print(len(movies))
print(movies[0:5])

# Year:
year = [a.text.strip('()') for a in soup.select('h3.lister-item-header span[class~=lister-item-year]')]
print(len(year))
print(year[0:5])

# Run time:
runtime = [a.text.strip() for a in soup.select('p.text-muted span[class~=runtime]')]
print(len(runtime))
print(runtime[0:5])

# Genre:
genre = [a.text.strip() for a in soup.select('p.text-muted span[class~=genre]')]
print(len(genre))
print(genre[0:5])

# Rating:
rate = [a.text.strip() for a in soup.select('div.inline-block span[class~=value]')]
print(len(rate))
print(rate[0:5])

# Summary:
summary = [a.text.strip() for a in soup.select('div.lister-item-content p:nth-of-type(2)')]
print(len(summary))
print(summary[0:5])

# Votes:
votes = [a.attrs.get('data-value') for a in soup.select(
            'div.lister-item-content p[class~=sort-num_votes-visible] span:nth-of-type(2)')]
print(len(votes))
print(votes[0:5])

# Gross:
gross = [a.attrs.get('data-value') for a in soup.select(
            'div.lister-item-content p[class~=sort-num_votes-visible] span:nth-of-type(5)')]
print(len(gross))
print(gross[0:5])

# Top 250 rank:
rank = [a.attrs.get('data-value') for a in soup.select(
            'div.lister-item-content p[class~=sort-num_votes-visible] span:nth-of-type(8)')]
print(len(rank))
print(rank[0:5])

# URL images:
images = [a.img.get('loadlate') for a in soup.select('div.lister-item-image a')]
print(len(images))
print(images[0:5])

### CERTIFICATE: NEEDS IMPROVEMENT
# ver https://gist.github.com/alexanderldavis/628d51405d38bc1d6c45c7eaec9bbd4b para resolver a 
# questão do filme sem a classificacao etaria

# Certificate:
cert = [a.text.strip() for a in soup.select('p.text-muted span[class~=certificate]')]

### METASCORE: NEEDS IMPROVEMENT
# Metascore:
metascore = [a.text.strip() for a in soup.select('div.inline-block span[class~=metascore]')]

### DIRECTOR AND STARS: NEEDS IMPROVEMENT
# Director:
director = [a.text.strip() for a in soup.select('div.lister-item-content p:nth-of-type(3) a:nth-of-type(1)')]

crew1 = [a.text.strip() for a in soup.select('div.lister-item-content p:nth-of-type(3) a:nth-of-type(2)')]
crew2 = [a.text.strip() for a in soup.select('div.lister-item-content p:nth-of-type(3) a:nth-of-type(3)')]
crew3 = [a.text.strip() for a in soup.select('div.lister-item-content p:nth-of-type(3) a:nth-of-type(4)')]
crew4 = [a.text.strip() for a in soup.select('div.lister-item-content p:nth-of-type(3) a:nth-of-type(5)')]

soup.select('div.lister-item-content p:nth-of-type(3) a:nth-of-type(6)')