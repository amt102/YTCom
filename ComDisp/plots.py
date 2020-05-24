import plotly.graph_objects as go 
import plotly.express as px
import pandas as pd
from plotly.offline import plot
from plotly.graph_objs import Scatter
from datetime import datetime
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import numpy as np
import os
# datetime.strptime('2020-05-04T06:54:33Z','%Y-%m-%dT%H:%M:%SZ')
class Plotter:

    def __init__(self):
        self.a =4

    def collectStats(self,comments):
        pos =0
        neg=0
        neutral=0
        neut =0
        hate=0
        offensive=0
        sensitive =0
        spam =0
        total =0
        s =[]
        d =[]
        likes =[]
        replies =[]
        spaml=[]
        dtemp = []
        text=[]
        for comment in comments:
            # print(type(comment.date))
            s.append(comment.sentiment_score)
            d.append(comment.date)
            dtemp.append(comment.date.strftime("%Y-%m-%d"))
            likes.append(comment.like_count)
            text.append(comment.text)
            replies.append(comment.replies_count)

            total+=1
            if comment.sentiment_score>=0.5:
                pos+=1
            elif comment.sentiment_score <= -0.5:
                neg+=1
            else:
                neutral+=1

            if comment.hateType == 'hate':
                hate+=1
            elif comment.hateType == 'offensive':
                offensive+=1
            else:
                neut+=1

            if comment.has_sensitive_content:
                sensitive+=1
            if comment.isSpam:
                spam+=1
                spaml.append(1)
            else:
                spaml.append(0)
        dict2 = {'date':d,'sentiment_score':s,'like_count':likes,'replies':replies,"isSpam":spaml,'dates':dtemp,'text':text}
        df2 = pd.DataFrame(dict2)
        dict ={'type' : ['Positive', 'Negative', 'Neutral', 'Has Sensitive Info', 'No Senstive Info', 'Spam', 'Not A Spam','Hate Speech','Offensive Language','Neutral', 'Total'],
        'number':[pos,neg,neutral,sensitive,int(total-sensitive),spam,int(total-spam),hate,offensive,neut,total] }
        df  = pd.DataFrame(dict)
        return df,df2

    def sentimentPlot(self,df):
        t = df['type']
        n = df['number']
        # colors=['rgb(100,200,100)','rgb(280,100,100)','rgb(100,100,200)']
        colors=['green','red','blue']
        sentiment_fig = go.Figure([go.Bar(x=t[0:3], y=n[0:3],text=n[0:3],
            textposition='auto',hovertext=['Cheer up','Woah! Some Diff perspective :(', 'meh..Whats the point'],marker_color=colors)])
        sentiment_fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        sentiment_fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        sentiment_fig.update_layout(title_text='Sentiment Distribution in comments')
        return plot(sentiment_fig,auto_open=False, output_type='div')

    def sensitivePLot(self,df):
        color2=['crimson','white']
        t = df['type']
        n = df['number']
        SI_fig = go.Figure([go.Bar(x=t[3:5], y=n[3:5],text=n[3:5],
            textposition='auto',hovertext=['vv senti boi','sakht launda'],marker_color=color2)])
        SI_fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        SI_fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        SI_fig.update_layout(title_text='Sensitive Info Distribution in comments')
        return plot(SI_fig,auto_open=False, output_type='div')

    def spamPlot(self,df):
        color2=['crimson','white']
        t = df['type']
        n = df['number']
        SI_fig = go.Figure([go.Bar(x=t[5:7], y=n[5:7],text=n[5:7],
            textposition='auto',hovertext=['spam','not a spam'],marker_color=color2)])
        SI_fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        SI_fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        SI_fig.update_layout(title_text='Spam comments Distribution')
        return plot(SI_fig,auto_open=False, output_type='div')

    def twoBarGraph(self,x,y,title,h,c):
        SI_fig = go.Figure([go.Bar(x=x, y=y,text=y,
            textposition='auto',hovertext=h,marker_color=c)])
        SI_fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        SI_fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        SI_fig.update_layout(title_text=title)
        return plot(SI_fig,auto_open=False, output_type='div')

    def pieChart(self,labels,values,c):
        # pull is given as a fraction of the pie radius
        fig = go.Figure(data=[go.Pie(labels=labels, values=values,pull=[0.1, 0, 0.2, 0])])
        if c:
            fig = go.Figure(data=[go.Pie(labels=labels, values=values,
            marker_colors=c,pull=[0.1, 0, 0.2, 0])])            
        return plot(fig,auto_open=False, output_type='div')

    def timegraph(self,df,xname,yname,title,htext):
        fig = px.scatter(df, x=xname, y=yname, title=title,hover_name=htext)
        fig.update_xaxes(rangeslider_visible=True)  
        return plot(fig,auto_open=False, output_type='div')      

    def histogram(self,df):
        # counts, bins = np.histogram(df.dates, bins=range(0, 60, 5))
        # bins = 0.5 * (bins[:-1] + bins[1:])
        # fig = px.bar(x=bins, y=counts, labels={'x':'total_bill', 'y':'count'})

        fig = px.histogram(df, x="dates",title="Number of comments distribution over Days",color="dates")
        return plot(fig,auto_open=False, output_type='div')

    def startPLot(self,comments,btn):
        df,df2= self.collectStats(comments)
        print('plotting in startPLot')
        print(df)

        title = 'Sentiment Distribution in comments'
        hovertext=['Cheer up','Woah! Some Diff perspective :(', 'meh..Whats the point']
        color2=['rgb(100,200,100)','rgb(280,100,100)','rgb(100,100,200)']
        sentiment_bar = self.twoBarGraph(df['type'][0:3],df['number'][0:3],title,hovertext,color2)
        # color_discrete_map={df['type'][0]:color2[0],
        #                          df['type'][1]:color2[1],
        #                          df['type'][2]:color2[2]}
        sentiment_pie = self.pieChart(df['type'][0:3],df['number'][0:3],color2)

        title = 'Sensitive Info Distribution in comments'
        hovertext=['Sensitive info can be useful','Smart People']
        color2=['crimson','white']
        si_bar = self.twoBarGraph(df['type'][3:5],df['number'][3:5],title,hovertext,color2)
        si_pie = self.pieChart(df['type'][3:5],df['number'][3:5],None)

        title = 'Spam Comments Distribution'
        hovertext=['spam','not a spam']
        color2=['crimson','white']
        spam_bar = self.twoBarGraph(df['type'][5:7],df['number'][5:7],title,hovertext,color2)
        spam_pie = self.pieChart(df['type'][5:7],df['number'][5:7],None)

        likes_series = self.timegraph(df2,'date','like_count','Analysing Likes Count of Comments','text')
        replie_series = self.timegraph(df2,'date','replies','Analysing Replies Count of Comments','text')
        
        frequency = self.histogram(df2)

        color2= ['red', 'gold', 'yellowgreen']
        hate_pie = self.pieChart(df['type'][7:10],df['number'][7:10],color2)

        return [sentiment_bar,si_bar,spam_bar,sentiment_pie,si_pie,spam_pie,likes_series,replie_series,frequency,hate_pie]
        # sentiment_fig.show()

    def makeWordCloud(self,s):
        print('In word cloud')
        modulePath = os.path.dirname(__file__)
        print('Path is '+ str(modulePath))
        maskArray = np.array(Image.open(os.path.join(modulePath, 'static/img/youtube.png')))
        cloud = WordCloud(background_color = "white", max_words = 200, mask = maskArray, stopwords = set(STOPWORDS))
        cloud.generate(s)
        cloud.to_file(os.path.join(modulePath, 'static/img/wordcloud.png'))
        print('Exiting word cloud')
