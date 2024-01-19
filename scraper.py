'''
Tarun Sankar
1/18/24
Program using BeautifulSoup to scrape info off of IMDB's reviews, accessed by the OpenMovieDB API
and comparing the score given vs the sentimental analysis of the reviews using the VADER model
'''

# Import the required libraries.
import requests
import re
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd
#import matplotlib.pyplot as plt
#import seaborn as sns
import nltk
import json
from nltk.sentiment import SentimentIntensityAnalyzer
#from tqdm.notebook import tqdm

#Gets API key for OpenMovieDB
apikey = Path('API_KEY.txt').read_text()

#Uses the search query to search the open movie database for the imdbID of the movie
searchquery = 'avengers_endgame' 
movieID= (requests.get(f'https://www.omdbapi.com/?t={searchquery}&apikey={apikey}').json())['imdbID']

# Get the URL based on the movie, as well as initialize the user agent and the VADER analyzer
url = f'https://www.imdb.com/title/{movieID}/reviews?spoiler=hide&sort=curated&dir=desc&ratingFilter=0'
user_agent = {'User-agent': 'Mozilla/5.0'}
sia = SentimentIntensityAnalyzer()

# Function for getting page contents
def get_page_contents(url):
    page = requests.get(url, headers = user_agent)
    return BeautifulSoup(page.text, 'html.parser')


soup = get_page_contents(url)   # Pull page contents

names = []  #Initializes a list for the names

#For every link that BS4 finds that fits the <span> tag with the class described

for links in soup.find_all('span', class_='display-name-link'):
     name = links.get_text().strip()    #Text is stripped
     names.append(name)                 #Added to list

#List for the actual user given scores
scores = []
for links in soup.find_all('span', class_='rating-other-user-rating'):
     score = links.get_text().strip()
     scores.append(int(str(score)[0:-3]))


blurbs = []     #List for the review text
polarities = [] #List for VADER's analysis score of the text

for links in soup.find_all('div', class_='text show-more__control'):
     blurb = links.get_text().strip()
     blurbs.append(blurb)
     polarities.append(float((sia.polarity_scores(blurb))['compound']))           # Converts the 'compound' score in the polarity score json to a float, then adds to the list

movie_dict = {'Name': names, 'Score': scores, 'Rating': polarities, 'Review': blurbs}       # Create dictionary for importing into a dataframe with the four main elements

print(len(names),len(scores),len(polarities),len(blurbs))  # Testing length of each list to see what wasn't grabbed (Likely due to BeautifulSoup's static issue)

movies = pd.DataFrame.from_dict(movie_dict, orient='index')  
df = movies.transpose() # Permute array
'''
df = pd.DataFrame()
df['Name']=names
df['Scores']=scores
#df['Summary']=blurbs
df['Sentiment Analysis Score']=polarities
'''
matching = df[((df['Score'] >= 5) & (df['Rating'] >= 0)) | (df['Score'] <= 5) & (df['Rating'] <= 0)]            # Dataframe which selects the VADER results being positive to >= 5 reviews and negative to <= 5 reviews
outliers = df[~(((df['Score'] >= 5) & (df['Rating'] >= 0)) | (df['Score'] <= 5) & (df['Rating'] <= 0))]         # Dataframe which takes anything that doesn't fit the criteria above.

print(matching)
print(outliers)



