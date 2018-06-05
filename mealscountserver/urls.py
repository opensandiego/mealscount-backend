# mealscountserver/urls.py
from django.conf.urls import url
from mealscountserver import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    url(r'^about/$', views.AboutPageView.as_view()), # Add this /about/ route
    url(r'^calculate/$', views.CalculatePageView.as_view()), # Initial calculate step
    url(r'^results/$', views.ResultsPageView.as_view()), # Results page
    url(r'^contact/$', views.ContactPageView.as_view()), # Add this /contact/ route
]
