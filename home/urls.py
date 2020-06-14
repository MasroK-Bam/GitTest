from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf.urls import url

urlpatterns = [
    path('',views.home),
    path('review/<int:param>', views.review),
    path('join/', views.Join.as_view(), name="Join"),
    path('login/', views.Login.as_view(), name = "Login"),
    path('changePassword/', views.ChangePassword.as_view(), name="ChangPassword"),
    path('logout/', views.logout),
    path('myinfo/', views.MyInfo.as_view(), name="MyInfo"),
    path('reviewpage/<int:pk>/', views.reviewpage),
    path('newwrite/<int:code>/',views.Newwrite.as_view()),
    path('reviewlist/', views.reviewlist),
]