# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FxsU4HEadGSnsFe5aKo4gAV1BNtsUYDt
"""

import re             
import nltk           
import pandas as pd   
import numpy as np   
import matplotlib.pyplot as plt  
import seaborn as sns

def remove_pattern(input_txt, pattern):   
    r = re.findall(pattern, input_txt)   
    for i in r:        
        input_txt = re.sub(i, '', input_txt)     
                       
    return input_txt



df = pd.read_csv('Angry.csv')
df = df.astype(str)
df['result'] = np.vectorize(remove_pattern)(df['text'], "@[\w]*") 
df['result'] = [re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', a,flags=re.MULTILINE)for a in df['result']]
df['result'] = [x.lower() for x in df['result']]
df['result'] = df['result'].str.replace("[^a-zA-Z#]", " ") 
df['result'] = df['result'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>3]))
df.head()
df.to_csv('angry_angry.csv')

tokenized_tweet = df['result'].apply(lambda x: x.split())
tokenized_tweet.head()

from nltk.stem.porter import *
stemmer = PorterStemmer()

tokenized_tweet = tokenized_tweet.apply(lambda x: [stemmer.stem(i) for i in x]) # stemming
tokenized_tweet.head()

all_words = ' '.join([text for text in df['result']])
from wordcloud import WordCloud
wordcloud = WordCloud(width=800, height=500, random_state=21, max_font_size=110).generate(all_words)

plt.figure(figsize=(10, 7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.show()

def hashtag_extract(x):
    hashtags = []
    # Loop over the words in the tweet
    for i in x:
        ht = re.findall(r"#(\w+)", i)
        hashtags.append(ht)

    return hashtags

# extracting hashtags from non racist/sexist tweets

HT_regular = hashtag_extract(df['result'])

# unnesting list
HT_regular = sum(HT_regular,[])

a = nltk.FreqDist(HT_regular)
d = pd.DataFrame({'Hashtag': list(a.keys()),
                  'Count': list(a.values())})
# selecting top 10 most frequent hashtags     
d = d.nlargest(columns="Count", n = 10) 
plt.figure(figsize=(16,5))
ax = sns.barplot(data=d, x= "Hashtag", y = "Count")
ax.set(ylabel = 'Count')
plt.show()