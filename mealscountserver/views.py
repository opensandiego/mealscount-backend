 # mealscountserver/views.py
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.views.generic.base import View
import csv

# Create your views here.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)

class AboutPageView(TemplateView):
    template_name = "about.html"

class CalculatePageView(TemplateView):
    template_name = "calculate.html"

class ResultsPageView(TemplateView):
    template_name = "results.html"

class ContactPageView(TemplateView):
    template_name = "contact.html"

class SubmitSpreadsheetView(View):
    def dispatch(self, request, *args, **kwargs):
        response_text = "Hello World Response Method: " + str(request.method)
        request_body = request.body
        lines = request_body.splitlines()
        response_text = response_text + " CSV Lines: " + str(lines)  
        return HttpResponse(response_text)
