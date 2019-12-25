#! usr/bin/env python3
import praw
import pandas as pd
import datetime as dt
import re
import heapq
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from contractions import CONTRACTION_MAP
import string

num = 501

reddit = praw.Reddit(client_id='F7D0F0RLEx5dOQ',
					 client_secret='LJ6g4ADGtAFqDjkrOJ4Z9EekDMU',
					 user_agent='horrorAnalysis',
					 username='redditcrawler001',
					 password='RedditCrawler123!')

subreddit = reddit.subreddit('TwoSentenceHorror')

top_subreddit = subreddit.top(limit = num)

# Create storage for each post
topics_dict = { "title":[],
				"score":[],
				"id":[], "url":[],
				"comms_num": [],
				"created": [],
				"body":[]}

# Parse through the top 500 posts in the subreddit
for submission in top_subreddit:
	if submission.title == "[deleted]":
		pass
	else:
	    topics_dict["title"].append(submission.title)
	    topics_dict["score"].append(submission.score)
	    topics_dict["id"].append(submission.id)
	    topics_dict["url"].append(submission.url)
	    topics_dict["comms_num"].append(submission.num_comments)
	    topics_dict["created"].append(submission.created)
	    topics_dict["body"].append(submission.selftext)

topics_data = pd.DataFrame(topics_dict)
print(len(topics_dict["title"]))
print(len(topics_dict["body"]))

fullHorror = []
for idx in range(len(topics_dict["title"])):
	print(idx)
	fullHorror.append([topics_dict["title"][idx], topics_dict["body"][idx]])

print(fullHorror)

'''
Stuck right here. Not sure best way to pre-proccess for analysis or what to analyze for
'''

def cleaner(sentence):
	if sentence[0] == sentence[-1] and sentence[0] in ["'",'"',"*"]:
		return sentence[1:len(sentence)-1]
	elif sentence[-1] == ",":
		return sentence[:len(sentence)-1]
	else:
		return sentence

lastCharDict = {}

def remove_special_characters(text):
    pattern = r'[^a-zA-z0-9\s]'
    text = re.sub(pattern, '', text)
    return text.replace("\n",'')

for first_sen in topics_data["title"]:
	first_sen = cleaner(first_sen)
	lastChar = first_sen[-1]
	if lastChar in lastCharDict.keys():
		lastCharDict[lastChar] += 1
	else:
		lastCharDict[lastChar] = 1

lastCharDict2 = {}
for first_sen in topics_data["body"]:
	first_sen = remove_special_characters(first_sen)
	#print(first_sen)
	if first_sen == '':
		pass
	else:
		lastChar = first_sen[-1]
		if lastChar in lastCharDict2.keys():
			lastCharDict2[lastChar] += 1
		else:
			lastCharDict2[lastChar] = 1
		if lastChar in ["*","'",",","]"]:
			print(first_sen)

'''
https://towardsdatascience.com/a-practitioners-guide-to-natural-language-processing-part-i-processing-understanding-text-9f4abfd13e72
'''

#print(lastCharDict2)


