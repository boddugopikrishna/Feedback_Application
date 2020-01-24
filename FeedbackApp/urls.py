"""Feedback_Application URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from . import views
urlpatterns = [
    path('', views.index,name = 'index'),
    path('login/',views.logIn,name = "login"),
    path('logout/', views.logOut, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('feedback/',views.feedback,name ='feedback'),
    path('teacher_analytics/',views.teacher_analytics,name ='teacher_analytics'),
    path('teacher_view/',views.teacher_view,name ='teacher_view'),
    path('feedbackStatus/',views.feedbackStatus,name ='feedbackStatus'),
    path('feedbackStatus_view/',views.feedbackStatus_view,name ='feedbackStatus_view'),
    path('principle_analytics/',views.principle_analytics,name ='principle_analytics'),
    path('analytics/',views.analytics,name = 'analytics'),
    path('top_five_teachers/',views.top_five_teachers,name = 'top_five_teachers')
]
