# mealscountserver/views.py
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.views.generic.base import View
import csv
from .algorithm import processSchools
from .csvparser import parseCsv
from .dao import uploadInformation
from django.db import transaction
import pandas as pd
from django.shortcuts import redirect


# Create your views here.
class HomePageView(TemplateView):
    template_name = "index.html"


class AboutPageView(TemplateView):
    template_name = "about.html"


class CalculatePageView(TemplateView):
    template_name = "calculate.html"

    def post(self, request):
        try:
            data = pd.read_csv(request.POST)
            script, div = processSchools(data)
        except ValueError:
            raise
            # return "not formatted correctly with a nice error number"
        return redirect(ResultsPageView) #, {'script': script, 'div_data': div})


class ResultsPageView(TemplateView):
    template_name = "results.html"

    def post(self, **kwargs):
        return render(self.template_name, **kwargs)


class ContactPageView(TemplateView):
    template_name = "contact.html"


class SubmitSpreadsheetView(View):
    def dispatch(self, request, *args, **kwargs):
        email = request.GET.get('email')
        schoolData = parseCsv(request.body)
        try:
            uploadInformation(schoolData, email)
        except:
            transaction.rollback()
        else:
            transaction.commit()
        return HttpResponse(processSchools(schoolData))
