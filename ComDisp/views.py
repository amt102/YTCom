from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from ComDisp.logic import *
from ComDisp.database import *
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from ComDisp.topic_modeling import *
from django.contrib import messages
from ComDisp.plots import *

def home(request):
    return render(request, 'comments/home.html') 

# def search(request):
#     if 'com_btn' in request.POST:
#         pass
#     elif 'anal_btn' in request.POST:
#         pass

def getAptComments(btn,video_id):
    d = DBHelper()
    comments_rtv=[]
    if btn == 'pos_btn':
        if d.commentsExists(video_id):
            print('Button presssed and we are just retrieving the comments, not from api')
            comments_rtv = d.retrivePosComments(video_id) #database.py
            # v = d.retriveVideoInfo(video_id)          #database.py
        else:
            print("In views: Inside else block")
            comments_rtv=[]
            # v = getInfoAboutVideo(video_id)   #logic.py
            # comments_rtv = getComments(video_id)  #logic.py
            # d.saveComments(comments_rtv)   #database.py
            # d.saveVideoInfo(v)    
    elif btn == 'neg_btn':
        if d.commentsExists(video_id):
            print('Button presssed and we are just retrieving the comments, not from api')
            comments_rtv = d.retriveNegComments(video_id) #database.py
            # v = d.retriveVideoInfo(video_id)          #database.py
        else:
            print("In views: Inside else block")
            comments_rtv=[]
    elif btn in ["like_count","replies_count"]:
        if d.commentsExists(video_id):
            print('Button presssed and we are just retrieving the comments, not from api')
            pat = "-"+btn
            comments_rtv = d.retriveSortedComments(video_id,pat) #database.py
            # v = d.retriveVideoInfo(video_id)          #database.py
        else:
            print("In views: Inside else block")
            comments_rtv=[]
    elif btn == 'sensitive':
        if d.commentsExists(video_id):
            print('Button presssed and we are just retrieving the comments, not from api')
            comments_rtv = d.retriveSensitiveComments(video_id) #database.py
            # v = d.retriveVideoInfo(video_id)          #database.py
        else:
            print("In views: Inside else block")
            comments_rtv=[]
    elif btn == 'spam':
        if d.commentsExists(video_id):
            print('Button presssed and we are just retrieving the comments, not from api in spam')
            comments_rtv = d.retriveSpamComments(video_id) #database.py
            # v = d.retriveVideoInfo(video_id)          #database.py
        else:
            comments_rtv=[]
    else:
        print("In views: Inside else block of spam")
        comments_rtv = d.retriveAllComments(video_id)
    return comments_rtv


@csrf_exempt
def graph(request):
    print('PLotting graphs in views')
    pn_btn = request.POST['btn_type']
    vid = request.POST['video_id']
    print(pn_btn)
    d = DBHelper()
    p = Plotter()
    # comments = getAptComments(pn_btn,vid)
    try:
        comments =d.retriveAllComments(vid)
    except:
        comments=[]
    # if pn_btn =='neutral':
    plots = p.startPLot(comments,pn_btn)
    return render(request,'comments/allPlots.html',context = {'sentibar':plots[0],'sibar':plots[1],'spambar':plots[2],'sentipie':plots[3],'sipie':plots[4],'spampie':plots[5],'likes':plots[6],'replies':plots[7],'frequency':plots[8]})
    # return render(request, 'comments/trial.html')

def plotit(request):
    data = ["I love to study in my school. The teacher is not that cool though",
        "A bigram or digram is a sequence of two adjacent elements from a string of tokens, which are typically letters, syllables, or words.",
        "The NBA's draft lottery won't take place Tuesday in Chicago as originally planned, but whenever it does happen, it is likely to look the same as it did last year, league sources told ESPN.",
            "Since play was suspended March 11 due to the coronavirus pandemic, teams at the top of the standings have been curious about the league restarting because they are in pursuit of a championship. For teams at the bottom of the standings, the focus has been on what the lottery will look like.",
            "I love to code. My teacher is soo cool"
    ]
    vis = modelTopic(data)
    return render(request, 'comments/LDA.html', context={'vis': vis})

def trial(request):
    print('IN trial')
    return render(request, 'comments/LDA.html')

def search(request):
    # storage = messages.get_messages(request)
    # storage.used = True
    vurl = request.POST['vid_url']
    if check(vurl):
        video_id = returnId(vurl)
        print(video_id)
        d = DBHelper()
        if d.videoExists(video_id):
            # we can delete them and then retrieve again or work on them only
            print('In Views: Comments exist')
            comments = d.retriveAllComments(video_id) #database.py
            v = d.retriveVideoInfo(video_id)          #database.py
        else:
            print("In views: Inside else block")
            v = getInfoAboutVideo(video_id)   #logic.py
            if v==None:
                messages.error(request, f"Unable to retrieve for this url. Try another one.")
                return render(request, 'comments/home.html', {'show_message': True})
            comments = getComments(video_id)  #logic.py
            print('DONE WITH EXTRACTION')
            # d.saveComments(comments)   #database.py
            d.saveVideoInfo(v)         #database.py
            comments = d.retriveAllComments(video_id)
            print('DONE SAVING IT')
        # detectspam(comments)
        
        # v = getInfoAboutVideo(video_id)   #logic.py
        # comments = getComments(video_id)  #logic.py
        # print('FINAL LEN OF RESULT IS')
        # print(len(comments))
        # print('Uploading to DATABASE')
        # saveComments(comments)
        # saveVideoInfo(v)
        # work on comments and video Info
        # comments = retriveAllComments(video_id) #database.py
        # v = retriveVideoInfo(video_id)          #database.py
        print('FINAL LEN OF RESULT IS')
        print(len(comments))
        print('Uploading to DATABASE')
        print('Checking videoInfo object = ')
        print(v)
        print(v.name)

        act_url = 'search_sent/' + str(video_id)

        
        if 'com_btn' in request.POST:
            return render(request,'comments/display_comments.html', {'comments':comments, 'videoInfo':v, 'act_url': act_url, 'vid_id': video_id})
        elif 'anal_btn' in request.POST:
            pass
            # messages.error(request, f"Analysed")
            # return render(request, 'comments/home.html', {'show_message': True})
        
    else:
        print('ERROR OCCURED: Invalid link given')
        messages.error(request, f"Invalid format entered. Enter the complete link of the video. eg: https://www.youtube.com/watch?v=4lWyYVL-X1I")
        # messages.info(request, 'Your password has been changed successfully!')
        return render(request, 'comments/home.html', {'show_message': True})
    return HttpResponse("Done")


def search_sent_page(request, video_id):
    print('-----------------------I AM HERE---------------------')
    # d = DBHelper()
    # btn = request.POST['btn_pressed']

    # if d.commentsExists(video_id):
    #     comments = d.retriveAllComments(video_id) #database.py
    #     v = d.retriveVideoInfo(video_id)          #database.py
    # else:
    #     print("In views: Inside else block")
    #     v = getInfoAboutVideo(video_id)   #logic.py
    #     comments = getComments(video_id)  #logic.py
    #     d.saveComments(comments)   #database.py
    #     d.saveVideoInfo(v)         #database.py
    
    # if 'pos_btn' == btn:
    #     print("pos dabaya")
    #     return HttpResponse("<h1>positive comments</h1>")
    # elif 'neg_btn' == btn:
    #     return HttpResponse("<h1>negative comments</h1>")
        
    return HttpResponse("Done")

@csrf_exempt
def search_sent(request):
    video_id = request.POST['video_id']
    btn = request.POST['btn_pressed']

    d = DBHelper()

    if btn == 'pos_btn':
        if d.commentsExists(video_id):
            print('Button presssed and we are just retrieving the comments, not from api')
            comments_rtv = d.retrivePosComments(video_id) #database.py
            # v = d.retriveVideoInfo(video_id)          #database.py
        else:
            print("In views: Inside else block")
            comments_rtv=[]
            # v = getInfoAboutVideo(video_id)   #logic.py
            # comments_rtv = getComments(video_id)  #logic.py
            # d.saveComments(comments_rtv)   #database.py
            # d.saveVideoInfo(v)    
    elif btn == 'neg_btn':
        if d.commentsExists(video_id):
            print('Button presssed and we are just retrieving the comments, not from api')
            comments_rtv = d.retriveNegComments(video_id) #database.py
            # v = d.retriveVideoInfo(video_id)          #database.py
        else:
            print("In views: Inside else block")
            comments_rtv=[]
    elif btn in ["like_count","replies_count"]:
        if d.commentsExists(video_id):
            print('Button presssed and we are just retrieving the comments, not from api')
            pat = "-"+btn
            comments_rtv = d.retriveSortedComments(video_id,pat) #database.py
            # v = d.retriveVideoInfo(video_id)          #database.py
        else:
            print("In views: Inside else block")
            comments_rtv=[]
    elif btn == 'sensitive':
        if d.commentsExists(video_id):
            print('Button presssed and we are just retrieving the comments, not from api')
            comments_rtv = d.retriveSensitiveComments(video_id) #database.py
            # v = d.retriveVideoInfo(video_id)          #database.py
        else:
            print("In views: Inside else block")
            comments_rtv=[]
    elif btn == 'spam':
        if d.commentsExists(video_id):
            print('Button presssed and we are just retrieving the comments, not from api in spam')
            comments_rtv = d.retriveSpamComments(video_id) #database.py
            # v = d.retriveVideoInfo(video_id)          #database.py
        else:
            print("In views: Inside else block of spam")
            comments_rtv=[]
    else:
        print('Control is coming here')
        comments_rtv=[]


    # if d.commentsExists(video_id):
    #     print('Button presssed and we are just retrieving the comments, not from api')
    #     comments_rtv = d.retriveAllComments(video_id) #database.py
    #     v = d.retriveVideoInfo(video_id)          #database.py
    # else:
    #     print("In views: Inside else block")
    #     v = getInfoAboutVideo(video_id)   #logic.py
    #     comments_rtv = getComments(video_id)  #logic.py
    #     d.saveComments(comments_rtv)   #database.py
    #     d.saveVideoInfo(v)         #database.py

    # getting positive or negative comments
    # if btn == 'pos_btn':
    #     for comment in comments_rtv:
    #         print(comment.date)
    #         if comment.sentiment_score > 0:
    #             comments.append(comment)
    # elif btn == 'neg_btn':
    #     for comment in comments_rtv:
    #         if comment.sentiment_score < 0:
    #             comments.append(comment)
    
    comments = comments_rtv
    try:
        ser_comments = serializers.serialize('json', comments)
        return JsonResponse({"comments": ser_comments}, status=200)
    except Exception as e:
        exp = type(e).__name__
        return JsonResponse({"wohowo": exp}, status=200)