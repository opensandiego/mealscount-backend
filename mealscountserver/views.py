# mealscountserver/views.py
import pandas as pd
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from django.views.generic.base import View

from .national_program_algorithm import processSchools
from .csvparser import parseCsv
from .dao import uploadInformation
from .forms import DistrictForm


# Create your views here.
class HomePageView(TemplateView):
    template_name = "index.html"


class AboutPageView(TemplateView):
    template_name = "about.html"


class CalculatePageView(FormView):
    template_name = "calculate.html"
    form_class = DistrictForm

    def post(self, request):
        try:
            form = DistrictForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    data = pd.read_csv(form.cleaned_data['district_data_file'])
                except (ValueError, KeyError):
                    raise ValidationError("Data File couldn't be parsed, " +
                                          "make sure to keep the headers and don't leave blank lines.")
                try:
                    # TODO do something with form.cleaned_data['email']
                    html_data = processSchools(
                        data,
                        state=form.cleaned_data['state_or_province'],
                        district=form.cleaned_data['district_name'],
                        assistance=form.cleaned_data['district_qualifies_for_performance_based_cash_assistance']
                        )
                except (ValueError, KeyError):
                    raise ValidationError("State or District was invalid")
            else:
                raise ValueError('form was invalid')
        except (ValueError, KeyError):
            raise ValidationError("Are you sure you filled out the fields?")

            # return "not formatted correctly with a nice error number"
        try:
            form.save()
        except:
            raise
        return render(request, "results.html",
                      {'html_data': html_data})



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
