from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'home/index.html')

from .models import movie

def review(request, param):

    context = {
        'movie' : movie.objects.get(movie_code=param)
    }

    return render(request, 'home/review.html', context)

