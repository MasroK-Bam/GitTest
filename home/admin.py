from django.contrib import admin
from .models import Member
from .models import Review

# Register your models here.

from .models import movie

admin.site.register(movie)
admin.site.register(Member)
admin.site.register(Review)