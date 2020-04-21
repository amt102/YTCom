from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from ComDisp.logic import *
from ComDisp.database import *
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt


def home(request):
    return render(request, 'comments/home.html') 

# def search(request):
#     if 'com_btn' in request.POST:
#         pass
#     elif 'anal_btn' in request.POST:
#         pass


def search(request):
    vurl = request.POST['vid_url']
    if check(vurl):
        video_id = returnId(vurl)
        print(video_id)
        d = DBHelper()
        if d.commentsExists(video_id):
            # we can delete them and then retrieve again or work on them only
            print('In Views: Comments exist')
            comments = d.retriveAllComments(video_id) #database.py
            v = d.retriveVideoInfo(video_id)          #database.py
        else:
            print("In views: Inside else block")
            v = getInfoAboutVideo(video_id)   #logic.py
            comments = getComments(video_id)  #logic.py
            d.saveComments(comments)   #database.py
            d.saveVideoInfo(v)         #database.py
        
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
        
    else:
        print('ERROR OCCURED: Invalid link given')
        return HttpResponse("Error")
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

    if d.commentsExists(video_id):
        comments_rtv = d.retriveAllComments(video_id) #database.py
        v = d.retriveVideoInfo(video_id)          #database.py
    else:
        print("In views: Inside else block")
        v = getInfoAboutVideo(video_id)   #logic.py
        comments_rtv = getComments(video_id)  #logic.py
        d.saveComments(comments_rtv)   #database.py
        d.saveVideoInfo(v)         #database.py

    # getting positive or negative comments
    comments = []
    if btn == 'pos_btn':
        for comment in comments_rtv:
            if comment.sentiment_score > 0:
                comments.append(comment)
    elif btn == 'neg_btn':
        for comment in comments_rtv:
            if comment.sentiment_score < 0:
                comments.append(comment)
    
    try:
        ser_comments = serializers.serialize('json', comments)
        return JsonResponse({"comments": ser_comments}, status=200)
    except Exception as e:
        exp = type(e).__name__
        return JsonResponse({"wohowo": exp}, status=200)

    

