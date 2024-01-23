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
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scraper
from scrapy.selector import Selector
from scrapy.selector import Selector
from tqdm import tqdm
import numpy as np
plt.style.use('ggplot')

# Gets API key for OpenMovieDB
apikey = Path('API_KEY.txt').read_text()

# Instantiate the Bert Model
try:
     tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

     model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
except: print("Failed to retrieve the tokenizer or model")

# Uses the search query to search the open movie database for the imdbID of the movie and url
def get_url(searchquery,ratingnumber):
     try:
          movieID = (requests.get(f'https://www.omdbapi.com/?t={searchquery}&apikey={apikey}').json())['imdbID']
          return f'https://www.imdb.com/title/{movieID}/reviews?spoiler=hide&sort=curated&dir=desc&ratingFilter={ratingnumber}'
     except: print("Movie not found")

# Defines the function in order to use Bert to analyze the reviews
def sentiment_score(review):
     try:
          tokens = tokenizer.encode(review, return_tensors='pt',truncation=True)
          result = model(tokens)
          return int(torch.argmax(result.logits))+1
     except: print("Too many tokens")

# Get the URL based on the movie, as well as initialize the user agent and the VADER analyzer
moviename = 'godzilla_minus_one'
user_agent = {'User-agent': 'Mozilla/5.0'}
finaldf = pd.DataFrame()

rating_list = []
author_list = []
review_list = []
score_list = []
error_url_list = []
error_msg_list = []

reviews = scraper.fetchFullReviews(get_url(moviename,0))

for d in tqdm(reviews):
        try:
            sel2 = Selector(text = d.get_attribute('innerHTML'))
            try:
                rating = sel2.css('.rating-other-user-rating span::text').extract_first()
            except:
                rating = np.NaN
            try:
                review = sel2.css('.text.show-more__control::text').extract_first()
            except:
                review = np.NaN  
            try:
                author = sel2.css('.display-name-link a::text').extract_first()
            except:
                author = np.NaN  
            rating_list.append(rating)
            author_list.append(author)
            review_list.append(review)
        except Exception as e:
            error_url_list.append(get_url(moviename,0))
            error_msg_list.append(e)

for review in review_list:
     score_list.append(sentiment_score(review))

review_df = pd.DataFrame({
        'Name':author_list,
        'Rating':rating_list,
        'Review':review_list,
        'Score':score_list
        })

review_df = review_df.sort_values(by='Rating',ascending=True, key=pd.to_numeric)

review_df.dropna(inplace=True)
print(review_df)
ax = sns.barplot(data=review_df, x='Rating', y='Score')
ax.set_title('Bert Sentiment Scores vs IMDB Ratings')
plt.show()







