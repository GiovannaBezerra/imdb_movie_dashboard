# This program scrape data from IMDB's "Top 250" movies. After collecting and processing data, the dataset is available for creating
# various types of visualizations.

# The information I gather from each movie are:
# 1. The movie title
# 2. The link to access movie page
# 3. The year of release
# 4. The age classification
# 5. The genre of the movie
# 6. How long the movie is
# 7. IMDb’s rating of the movie
# 8. The Metascore of the movie
# 9. The movie summary
# 10. The directors
# 11. The star cast
# 12. How many votes the movie got
# 13. The U.S. gross earnings of the movie
# 14. The image of movie poster

# Import modules:
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Creating empty lists to store values:
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
grosses = []
images = []

# There are 250 movies and each page has 50 movies listed.
# Url1: 1-50, Url2: 51-100, Url3: 101-150, Url4: 151-200 and Url5: 201-250.
# Let's create a lis of pages:

urls = ['https://www.imdb.com/search/title/?groups=top_250',
        'https://www.imdb.com/search/title/?groups=top_250&start=51&ref_=adv_nxt',
        'https://www.imdb.com/search/title/?groups=top_250&start=101&ref_=adv_nxt',
        'https://www.imdb.com/search/title/?groups=top_250&start=151&ref_=adv_nxt',
        'https://www.imdb.com/search/title/?groups=top_250&start=201&ref_=adv_nxt'
       ]

# Creating request header config.:
headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3538.102 Safari/537.36 Edge/18.19582",
    'Accept-Language': 
    'en-US, en;q=0.5'
}

for url in urls:
    # Building the soup constructor:
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Splitting movies by content:
    movie_content = soup.find_all('div', class_ = 'lister-item mode-advanced')
    
    # Getting data for each content:
    for content in movie_content:

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

        # Getting Votes:
        if content.select('p[class~=sort-num_votes-visible] span[name~=nv]')[0] is not None:
            vote = content.select('p[class~=sort-num_votes-visible] span[name~=nv]')[0].text
            votes.append(vote)
        else:
            votes.append("")

        # Getting Gross Value:
        if content.select('p[class~=sort-num_votes-visible] span[name~=nv]')[1] is not None:
            gross = content.select('p[class~=sort-num_votes-visible] span[name~=nv]')[1].text
            grosses.append(gross)
        else:
            grosses.append("")

        # Gettting Images:
        if content.img.get('loadlate') is not None:
            image = content.img.get('loadlate')
            images.append(image)
        else:
            images.append("")

# Creating the data frame:
df = pd.DataFrame({'movie_title': movies,'link': links,'year': years,
                   'certificate': certificates,'runtime': runtimes,
                   'genre': genres,'rate': rates,'metascore':metascores,
                   'summary':summaries,'directors':directors,'stars':stars,
                   'votes':votes,'gross':grosses,'image':images})

print(df.shape)
print(df.head())



