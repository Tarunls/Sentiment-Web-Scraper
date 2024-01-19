'''
Tarun Sankar
1/18/24
Program using BeautifulSoup to scrape info off of IMDB's reviews, accessed by the OpenMovieDB API
and comparing the score given vs the sentimental analysis of the reviews using the VADER model
'''

# Import the required libraries.
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import requests
import re
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
plt.style.use('ggplot')
#from tqdm.notebook import tqdm

# Gets API key for OpenMovieDB
apikey = Path('API_KEY.txt').read_text()

# Instantiate the Bert Model
tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

# Uses the search query to search the open movie database for the imdbID of the movie and url
def get_url(searchquery,starnumber):
     movieID = (requests.get(f'https://www.omdbapi.com/?t={searchquery}&apikey={apikey}').json())['imdbID']
     return f'https://www.imdb.com/title/{movieID}/reviews?spoiler=hide&sort=curated&dir=desc&ratingFilter={starnumber}'

# Defines the function in order to use Bert to analyze the reviews
def sentiment_score(review):
    tokens = tokenizer.encode(review, return_tensors='pt',truncation=True)
    result = model(tokens)
    return int(torch.argmax(result.logits))+1



# Get the URL based on the movie, as well as initialize the user agent and the VADER analyzer
moviename = 'avengers_endgame'
user_agent = {'User-agent': 'Mozilla/5.0'}
finaldf = pd.DataFrame()

# Function for getting page contents
def get_page_contents(url):
    page = requests.get(url, headers = user_agent)
    return BeautifulSoup(page.text, 'html.parser')

for x in range(10):
     url = get_url(moviename,x+1)

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
          polarities.append(sentiment_score(blurb)) #Appends the Bert sentiment scores to the list

     movie_dict = {'Name': names, 'Score': scores, 'Rating': polarities, 'Review': blurbs}       # Create dictionary for importing into a dataframe with the four main elements
     movies = pd.DataFrame.from_dict(movie_dict, orient='index')  
     df = movies.transpose() # Permute array
     finaldf = finaldf._append(df)

print(finaldf)
ax = sns.barplot(data=finaldf, x='Score', y='Rating')
ax.set_title('Bert Sentiment Scores vs IMDB Ratings')
plt.show()






