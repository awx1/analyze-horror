#! usr/bin/env python3
import praw
import pandas as pd
import datetime as dt
import re
import heapq
import nltk
nltk.download('averaged_perceptron_tagger')

reddit = praw.Reddit(client_id='F7D0F0RLEx5dOQ',
					 client_secret='LJ6g4ADGtAFqDjkrOJ4Z9EekDMU',
					 user_agent='horrorAnalysis',
					 username='redditcrawler001',
					 password='RedditCrawler123!')

subreddit = reddit.subreddit('TwoSentenceHorror')

top_subreddit = subreddit.top(limit = 500)

'''
for submission in subreddit.top(limit=1):
	print(submission.title, submission.id)
'''

topics_dict = { "title":[],
				"score":[],
				"id":[], "url":[],
				"comms_num": [],
				"created": [],"body":[]}

for submission in top_subreddit:
    topics_dict["title"].append(submission.title)
    topics_dict["score"].append(submission.score)
    topics_dict["id"].append(submission.id)
    topics_dict["url"].append(submission.url)
    topics_dict["comms_num"].append(submission.num_comments)
    topics_dict["created"].append(submission.created)
    topics_dict["body"].append(submission.selftext)

topics_data = pd.DataFrame(topics_dict)
#print(topics_data)

commonWords = {}

for firstSentence in topics_dict["title"] + topics_dict["body"]:
	token = nltk.word_tokenize(firstSentence)
	tokenized = nltk.pos_tag(token)
	for word, wordToken in tokenized:
		if wordToken in ['PRP$', 'IN', 'DT']:
			pass
		else:
			if word not in commonWords:
				commonWords[word] = 1
			else:
				commonWords[word] += 1	

#topWords = dict(sorted(commonWords.iteritems(), key=operator.itemgetter(1), reverse=True)[:20])

max(commonWords, key=commonWords.get)
sorted(commonWords, key=commonWords.get, reverse=True)[:5]
topWords = heapq.nlargest(20, commonWords, key=commonWords.get)

print(topWords)