from django.db import models

# Create your models here.
class Comment(models.Model):
    video_id = models.TextField()
    comment_id = models.TextField()
    text = models.TextField()
    date = models.TextField()
    author = models.TextField()
    author_channel_url = models.URLField()
    like_count = models.IntegerField()
    replies_count = models.IntegerField() 
    has_sensitive_content = models.BooleanField(default=False)
    senstivite_info = models.TextField(default=None)
    sentiment_score = models.FloatField(default=0.0)
    sentiment_stat = models.TextField(default=None)
    lang = models.CharField(max_length=10,default='en')

class videoInfo(models.Model):
    channelId = models.TextField()
    channelIdTitle = models.TextField()
    videoId = models.TextField()
    name = models.TextField()
    description = models.TextField()
    thumbnail = models.TextField()
    viewsCount = models.IntegerField(default=0)
    likeCount = models.IntegerField(default=0)
    dislikeCount = models.IntegerField(default=0)
    favouriteCount = models.IntegerField(default=0)
    commentCount = models.IntegerField(default=0)