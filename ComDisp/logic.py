# import json
import re
# import urllib.request
# import requests
from googleapiclient.discovery import build
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from pytube import YouTube
import random
import string
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
# import pymongo
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from langdetect import detect
from ComDisp.models import Comment, videoInfo
# url_original = "https://www.youtube.com/watch?v=ZyyYQoXr6PQ"
# video_id = url_original.rsplit("=")[1]
from ComDisp.database import *

import pandas as pd
import numpy as np
import pickle
# from sklearn.externals import joblib
import joblib
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, roc_curve
from sklearn.naive_bayes import MultinomialNB
import os

from hatesonar import Sonar
from nltk.corpus import stopwords

# from matplotlib import pyplot as plt
# from wordcloud import WordCloud


class Helper:
    def __init__(self):
        pass

    # def title_to_underscore_title(self, title: str):
    #     title = re.sub('[\W_]+', "_", title)
    #     return title.lower()

    # def id_from_url(self, url: str):
    #     return url.rsplit("/", 1)[1]
    
    def htmlCleanup(self,text):
        yummysoup=BeautifulSoup(text,'lxml')
        html_free_text =yummysoup.get_text()
        return html_free_text

    # takes a string, removes the punctuations and returns a string
    def removePunctuations(self,text):
        temp = ["-"]
        punc_free = "".join([c for c in text if c not in string.punctuation and c not in temp]) 
        return punc_free

    # # takes a list, removes the stopwords and returns a list
    # def stopwordsRemove(self,textList):
    #     words =[]
    #     for w in textList:
    #         if (w not in stopwords.words('english')):
    #             words.append(w.lower())
    #     # words = [w for w in textList if w not in stopwords.words('english')]
    #     # print(words)
    #     return words

    # def lemmatizeWords(self,text):
    #     lemmatized_text = [self.lemmatizer.lemmatize(i) for i in text]
    #     return lemmatized_text

    # def stemmWords(self,text):
    #     stem_text = [self.stemmer.stem(i) for i in text]
    #     return stem_text

    def preProcessing(self,text):
        # removing html content and punctuations
        text = self.htmlCleanup(text)
        text = self.removePunctuations(text)
#         text= text.str.split(" ", n = -1, expand = False)
#         text = self.stopwordsRemove(text)
#         text = self.lemmatizeWords(text)
#         text = self.stemmWords(text)
        return text


def check(vurl):
    checklink = vurl.split("/watch?v=")
    print(checklink)
    if len(checklink)==2 and checklink[0]=="https://www.youtube.com":
        print('valid id')
        return True
    print('invalid id')
    return False

def returnId(vurl):
    vurl=vurl.strip()
    video_id = vurl.rsplit("=")[1]
    return video_id


def get_sentiment(analyzer,sentence,lan):
    if lan=='en':
        vs = analyzer.polarity_scores(sentence)
        return vs
    else:
        return None

def createCommentObject(com):
    c = Comment(
        video_id = com['videoId'],
        comment_id = com['topLevelComment']['id'],
        text = com['topLevelComment']['snippet']["textOriginal"],
        date = com['topLevelComment']['snippet']["publishedAt"],
        author = com['topLevelComment']['snippet']["authorDisplayName"],
        author_channel_url = com['topLevelComment']['snippet']["authorChannelUrl"],
        like_count = com["topLevelComment"]["snippet"]["likeCount"],
        replies_count = com["totalReplyCount"],
        has_sensitive_content = com["isSensitive"],
        senstivite_info = str(com['sensitive_info']),
        sentiment_score = com["score"] if com["score"] else 0.0,
        sentiment_stat = str(com["score_dict"]) if com["score_dict"] else "NA",
        lang=com['lang'] if com['lang'] else "NA",
    )
    return c

def load_comments(final_list,match,ids,repeat,analyzer):
    helper = Helper()
    if match:
        for item in match["items"]:
            comment_id = item['snippet']['topLevelComment']['id']
            if comment_id in ids:
                repeat+=1
#                 print(item["snippet"]["topLevelComment"]["snippet"]["textDisplay"])
            else:
                ids.add(comment_id)
                text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                text = helper.preProcessing(text)
#                 print(text)
                try:
                    lan = detect(text)
                except:
                    lan='No_text'                
                score_dict = get_sentiment(analyzer,text,lan)
                if score_dict:
                    score = score_dict['compound']
                else:
                    score =None
                
                pattern2 = '[0-9]{2,3}-?[0-9]{8,10}'
                lno = re.findall(pattern2,item["snippet"]["topLevelComment"]["snippet"]["textDisplay"])
                sensitive_info=False
                if len(lno)!=0:
                    sensitive_info=True
                    print('Sensitive info is present in a comment')
                    # print(lno)
                    # print(item["snippet"]["topLevelComment"]["snippet"]["textDisplay"])
                    # print()
                else:
                    lno=None
                item['snippet']['isSensitive'] = sensitive_info
                item['snippet']['sensitive_info'] = lno
                item['snippet']['score_dict']=score_dict
                item['snippet']['score'] = score
                item['snippet']['lang'] = lan
                c = createCommentObject(item['snippet'])
                final_list.append(c)
                # collection.insert_one(item['snippet'])
    return (ids,repeat,final_list)

def get_comment_thread(youtube, video_id,next_page_token):
    if next_page_token:
        results = youtube.commentThreads().list(
            part="snippet",
            maxResults=100,
            videoId=video_id,
            textFormat="plainText",
            pageToken=next_page_token
        ).execute()
    else:
        results= youtube.commentThreads().list(
            part="snippet",
            maxResults=100,
            videoId=video_id,
            textFormat="plainText"
        ).execute() 
    return results


def getComments(video_id):
    api_key = "AIzaSyAoI2MkdcP2mI1okW5iEDip8hEC8ZNpy4E"
    youtube = build('youtube','v3',developerKey=api_key)
    # helper = Helper()
    analyzer = SentimentIntensityAnalyzer()
    # connection = pymongo.MongoClient('localhost',27017)
    # db = connection['youtube_comments']
    final_list=[]
    error=False
    ids={'abc'}
    repeat=0

    next_page_token=None
    # collection.delete_many({})
    match = get_comment_thread(youtube, video_id,next_page_token)
    try:
        next_page_token = match["nextPageToken"]
    except:
        error = True
        print('Error: Next_page_taken is not present')
        # print(next_page_token)
        
    # ids,repeat = load_comments(match,collection,ids,repeat)
    ids,repeat,final_list = load_comments(final_list,match,ids,repeat,analyzer)
    d = DBHelper()
    if len(final_list)!=0:
        final_list = detectspam(final_list)
        final_list = hateSpeech(final_list)
        d.saveComments(final_list)
        final_list=[]


    if next_page_token and not error:
        print('HERE in the while loop')
        while next_page_token:
            match = get_comment_thread(youtube, video_id,next_page_token)
            try:
                next_page_token = match["nextPageToken"]
            except:
                error=True
                print('Error: Next page token is not present in while')
                # print(next_page_token)
            # ids,repeat = load_comments(match,collection,ids,repeat)
            ids,repeat,final_list = load_comments(final_list,match,ids,repeat,analyzer)
            if len(final_list)!=0:
                final_list = detectspam(final_list)
                # final_list = hateSpeech(final_list)
                d.saveComments(final_list)
                final_list=[]
            if(repeat>20):
                print('GETTING OUT: repetition is happening')
                break
    return final_list

def createVideoObject(vjson):
    v = videoInfo(
        channelId = vjson["items"][0]["snippet"]["channelId"],
        channelIdTitle = vjson["items"][0]["snippet"]["channelTitle"],
        videoId = vjson["items"][0]["id"],
        name = vjson["items"][0]["snippet"]["title"],
        description = vjson['items'][0]['snippet']['description'],
        thumbnail = vjson["items"][0]["snippet"]["thumbnails"]["standard"]["url"],
        viewsCount = vjson["items"][0]["statistics"]["viewCount"],
        likeCount = vjson["items"][0]["statistics"]["likeCount"],
        dislikeCount = vjson["items"][0]["statistics"]["dislikeCount"],
        favouriteCount = vjson["items"][0]["statistics"]["favoriteCount"],
        commentCount = vjson["items"][0]["statistics"]["commentCount"],
    )
    return v 

def getInfoAboutVideo(video_id):
    api_key = "AIzaSyAoI2MkdcP2mI1okW5iEDip8hEC8ZNpy4E"
    youtube = build('youtube','v3',developerKey=api_key)
    s = youtube.videos().list(id = video_id,part = "snippet,statistics",).execute()
    if(s['items'] == []):
        return None
    title = s['items'][0]['snippet']['channelTitle']
    # description = s['items'][0]['snippet']['description']
    # statistics = s['items'][0]['statistics']
    # date = s['items'][0]['snippet']['publishedAt']
    # print(s)
    # print('SNIPPET ********')
    # print(s['items'][0]['snippet'])
    print('TITLE************')
    print(title)
    # print('DESCRIPTION******')
    # print(description)
    # print('STATISTICS*******')
    # print(statistics)
    # print('DATE*************')
    # print(date)
    v = createVideoObject(s)
    return v

def detectspam(model_list):
    print("Detecting spam: Inside the function")
    Array = []
    for i in range(0,len(model_list)):
        Array.append(model_list[i].text)
    print('checking length in detect spam')
    print('model list ' + str(len(model_list)))
    print('array length '+ str(len(Array)))
    modulePath = os.path.dirname(__file__)  # get current directory
	# filePath = os.path.join(modulePath, 'MV1')
	# with open(filePath, 'rb') as f:
	# 	obj=pickle.load(f)
    vectorizer = pickle.load(open(os.path.join(modulePath, 'MV1'), 'rb'))
    tranformer = pickle.load(open(os.path.join(modulePath, 'MT1'), 'rb'))
    model = pickle.load(open(os.path.join(modulePath, 'M1'), 'rb'))
    rf = pickle.load(open(os.path.join(modulePath, 'M2'), 'rb'))
    random_search = pickle.load(open(os.path.join(modulePath, 'M3'), 'rb'))
    count_vect = pickle.load(open(os.path.join(modulePath, 'MCV1'), 'rb'))
    vectorizer.transform(Array)
    x_train_counts = count_vect.transform(Array)
    new = tranformer.transform(x_train_counts)
    Pred_M = model.predict(new)
    Pred_RF = rf.predict(new)
    Pred_RS = random_search.predict(new)
    print('Inside detect spam: PRINTING Pred')
    # print(Pred_M)
    # print('NEXT')
    # print(Pred_RF)
    # print('NEXT 2')
    # print(Pred_RS)
    # print('For loop 2')
    for i in range(len(Pred_M)):
        if Pred_M[i]==1 or Pred_RS[i]==1 or Pred_RF[i]==1:
            model_list[i].isSpam =True
            # print(Array[i])
            # print()
    return model_list

def hateSpeech(comments):
    sonar = Sonar()
    print('Inside hatespeech')
    print('Comments len ='+str(len(comments)))
    for i in range(len(comments)):
        x = sonar.ping(text=comments[i].text)
        if x['top_class'] == "hate_speech":
            comments[i].hateType = 'hate'
        elif x['top_class'] == "offensive_language":
            comments[i].hateType = 'offensive'
        else:
            comments[i].hateType = 'neutral'
    return comments