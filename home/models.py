from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.

class movie(models.Model):
    #primaryKEY : 다른 줄(row)와 중복 될 수 없고, 값이 반드시 존재해야 하는 구분값
    movie_code = models.AutoField(primary_key=True)
    movie_name = models.CharField(max_length=20)
    movie_content = models.CharField(max_length=1000)

class Member(models.Model):
    userid = models.CharField(max_length=20, primary_key=True)
    userpw = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    birth = models.DateTimeField()
    phonenum = models.IntegerField()
    useremail = models.EmailField()

class Review(models.Model):
    writer = models.CharField(max_length=100)
    category = models.IntegerField(default=0)
    post_date=models.DateTimeField(auto_now_add=True)
    post_title=models.CharField(max_length=100)
    post_contents=models.TextField(blank=True,help_text='Post Contents')

    class Meta:
        ordering = ['-post_date']

    def __str__(self):
        return self.post_title
    
    def get_abolute_url(self):
        return reverse('post-detail',args=[str(self.id)])
        
#모델을 만들었으면 이후 처리
    #1. admin.py에서 모델을 등록한다
    #2. python manage.py makemigrations (변경점을 읽어낸다)
    #3. python manage.py migrate        (변경점을 DB에 반영한다.)

