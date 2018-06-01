# mealscountserver/views.py
import pandas as pd
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from django.views.generic.base import View

from .algorithm import processSchools
from .csvparser import parseCsv
from .dao import uploadInformation
from .forms import UploadCSVForm
from django.core.exceptions import ValidationError

# Create your views here.
class HomePageView(TemplateView):
    template_name = "index.html"


class AboutPageView(TemplateView):
    template_name = "about.html"


class CalculatePageView(FormView):
    template_name = "calculate.html"
    form_class = UploadCSVForm
    success_url = '/results/'

    def post(self, request):
        try:

            form = UploadCSVForm(request.POST, request.FILES)

            if form.is_valid():
                try:
                    data = pd.read_csv(request.FILES['file'])
                except (ValueError, KeyError):
                    raise ValidationError("Data File couldn't be parsed, make sure to keep the headers and don't leave blank lines.")
                try:
                    script, div = processSchools(data, state=form.cleaned_data['state'], district=form.cleaned_data['district'])
                except (ValueError, KeyError):
                    raise ValidationError("State or District was invalid")
            else:
                raise ValueError
        except (ValueError, KeyError):
            raise ValidationError("Are you sure you filled out the fields?")

            # return "not formatted correctly with a nice error number"
        return render(request, "results.html",
                      {'script': script, 'div_data': div})


# class ResultsPageView(TemplateView):
#     template_name = "results.html"
#
#     # def post(self, **kwargs):
#     #     return render(self.template_name, **kwargs)


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
