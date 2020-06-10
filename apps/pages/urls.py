# apps/pages/urls.py
from django.urls import path
from . import views


# Link 'pages' app urls to views
urlpatterns = [
    path('', views.HomePageView.as_view(), name='homepage'),
]
