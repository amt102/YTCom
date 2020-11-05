from ComDisp.models import Comment, videoInfo

class DBHelper:
    # comment_helper
    # video_helper

    def __init__ (self):
        self.comment_helper = Comment.objects
        self.video_helper = videoInfo.objects

    # saving comments to the table
    def saveComments(self,coml):
        # vid = com['videoId']
        for com in coml:
            com.save()
        print("Done uploading comments to Database")

    # save video info in the videoInfo table 
    def saveVideoInfo(self,v):
        v.save()
        print('DONE saving the video info in table')

    # get all comments from the table of a VIDEOID
    def retriveAllComments(self,videoId):
        #returns zero or more comments
        try:
            comml = self.comment_helper.filter(video_id=videoId)
            print('RETRIEVED the comments = len'+str(len(comml)))
        except:
            comml=[]
            print('Error: In retrieving the comments')
        return comml
    
    def retrivePosComments(self,videoId):
        #returns zero or more comments
        try:
            comml = self.comment_helper.filter(video_id=videoId,sentiment_score__gte=0.5).order_by("-sentiment_score")
            print('RETRIEVED the pos comments = len'+str(len(comml)))
        except:
            comml=[]
            print('Error: In retrieving the pos comments')
        return comml

    def retriveNegComments(self,videoId):
        #returns zero or more comments
        try:
            comml = self.comment_helper.filter(video_id=videoId, sentiment_score__lte=0.5).order_by("sentiment_score")
            print('RETRIEVED the neg comments = len'+str(len(comml)))
        except:
            comml=[]
            print('Error: In retrieving the neg comments')
        return comml

    def retriveSortedComments(self,videoId,col_name):
        #returns zero or more comments
        print('colname given in retrive comments = '+str(col_name))
        try:
            comml = self.comment_helper.filter(video_id=videoId).order_by(col_name)
            print('RETRIEVED the neg comments = len'+str(len(comml)))
        except:
            comml=[]
            print('Error: In retrieving the sort comments')
        return comml

    def retriveSensitiveComments(self,videoId):
        #returns zero or more comments
        try:
            comml = self.comment_helper.filter(video_id=videoId, has_sensitive_content=True).order_by("date")
            print('RETRIEVED the sensiitive  comments = len'+str(len(comml)))
        except:
            comml=[]
            print('Error: In retrieving the sensitive comments')
        return comml

    def retriveSpamComments(self,videoId):
        #returns zero or more comments
        try:
            comml = self.comment_helper.filter(video_id=videoId, isSpam=True).order_by("date")
            print('RETRIEVED the spam comments = len'+str(len(comml)))
        except:
            comml=[]
            print('Error: In retrieving the spam comments')
        return comml

    def retriveNotSpamComments(self,videoId):
        #returns zero or more comments
        try:
            comml = self.comment_helper.filter(video_id=videoId, isSpam=False).order_by("date")
            print('RETRIEVED the spam comments = len'+str(len(comml)))
        except:
            comml=[]
            print('Error: In retrieving the spam comments')
        return comml

    def retriveHateComments(self,videoId):
        #returns zero or more comments
        try:
            comml = self.comment_helper.filter(video_id=videoId, hateType='hate').order_by("date")
            print('RETRIEVED the spam comments = len'+str(len(comml)))
        except:
            comml=[]
            print('Error: In retrieving the spam comments')
        return comml

    def retriveOffensiveComments(self,videoId):
        #returns zero or more comments
        try:
            comml = self.comment_helper.filter(video_id=videoId, hateType='offensive').order_by("date")
            print('RETRIEVED the spam comments = len'+str(len(comml)))
        except:
            comml=[]
            print('Error: In retrieving the spam comments')
        return comml
    # # get comments with positive sentiment
    # def retrivePosComments(self, videoId):
    #     try:
    #         comml = self.comment_helper.filter(video_id=videoId, sentiment_score>0)
    #         print('RETRIEVED the comments = len'+str(len(comml)))
    #     except:
    #         comml=[]
    #         print('Error: In retrieving the comments')
    #     return comml

    def retriveVideoInfo(self,videoId):
        #returns zero or more videoInfo
        try:
            v = self.video_helper.get(videoId=videoId)
            print('RETRIEVED the Video Id')
        except:
            v = None
            print('Error: In retrieving the videoInfo')
        return v

    # check whether the comments already exist for this VIDEOID
    def commentsExists(self,videoId):
        try:
            exist = self.comment_helper.filter(video_id=videoId).exists()
            if exist:
                print('In database.py :COMMENTS ALREADY EXIST')
                return True
            else:
                print('In database.py: COMMENTS DOESNT EXIST IN ELSE')
                return False
        except:
            print('In database.py :COMMENTS DOESNT EXIST IN EXCEPT')
            return False
        return False
    
    def videoExists(self,videoId):
        try:
            exist = self.video_helper.filter(videoId=videoId).exists()
            if exist:
                print('In database.py :video ALREADY EXIST')
                return True
            else:
                print('In database.py: video DOESNT EXIST IN ELSE')
                return False
        except:
            print('In database.py :video DOESNT EXIST IN EXCEPT')
            return False
        return False

    # deleting all comments 
    def deleteComments(self,videoId):
        try:
            self.comment_helper.filter(video_id=videoId).delete()
        except:
            print('Error: Indeleting comments, id may not exist')

    def deleteVideoInfo(self,videoId):
        try:
            self.video_helper.filter(videoId=videoId).delete()
        except:
            print('Error: Indeleting videoInfo, id may not exist')