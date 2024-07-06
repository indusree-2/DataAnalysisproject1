import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

# Downloading IMDb top 250 movies' data
url = 'http://www.imdb.com/chart/top'
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Select relevant data
movies = soup.select('td.titleColumn')
crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
ratings = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]

# Create a list for storing movie information
movie_list = []

# Iterating over movies to extract each movie's details
for index in range(len(movies)):
    # Separating movie into: 'place', 'title', 'year'
    movie_string = movies[index].get_text()
    movie_string = ' '.join(movie_string.split()).replace('.', '')
    movie_title = movie_string[len(str(index)) + 1:-7].strip()
    year = re.search(r'\((\d{4})\)', movie_string).group(1)
    place = movie_string[:len(str(index)) + 1].strip()

    # Create a dictionary for each movie's details
    data = {
        "place": place,
        "movie_title": movie_title,
        "rating": ratings[index],
        "year": year,
        "star_cast": crew[index]
    }
    movie_list.append(data)

# Print the movie details with their ratings
for movie in movie_list:
    print(f'{movie["place"]} - {movie["movie_title"]} ({movie["year"]}) - Starring: {movie["star_cast"]}, Rating: {movie["rating"]}')

# Save the list as a DataFrame and convert it into a CSV file
df = pd.DataFrame(movie_list)
df.to_csv('imdb_top_250_movies.csv', index=False)
