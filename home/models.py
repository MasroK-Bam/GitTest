from django.db import models

# Create your models here.

class movie(models.Model):
    #primaryKEY : 다른 줄(row)와 중복 될 수 없고, 값이 반드시 존재해야 하는 구분값
    movie_code = models.AutoField(primary_key=True)
    movie_name = models.CharField(max_length=20)
    movie_content = models.CharField(max_length=1000)

#모델을 만들었으면 이후 처리
    #1. admin.py에서 모델을 등록한다
    #2. python manage.py makemigration  (변경점을 읽어낸다)
    #3. python manage.py migrate        (변경점을 DB에 반영한다.)

