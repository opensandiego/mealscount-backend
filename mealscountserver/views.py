# mealscountserver/views.py
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from .forms import DistrictForm
from . import backend_utils as bu
from . import national_rates_config_parser as cp
from .national_program_algorithm import mcAlgorithmV2, CEPSchoolGroupGenerator
from pathlib import Path
from config import *
from pandas_django import PandasSimpleView


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
                data = self.etl(form)

            else:
                raise ValueError('form was invalid')
        except (ValueError, KeyError):
            raise ValidationError("Are you sure you filled out the fields?")

        try:
            form.save()
        except:
            raise

        return render(request, "results.html",
                      {'html_data': data})

    def etl(self, form):
        data = self.dataframe_and_metadata(form)
        try:
            self.assistance = form.cleaned_data['district_qualifies_for_performance_based_cash_assistance']
        except:
            raise ValidationError("the checkbox for performance based cash assistance was invalid")

        try:
            # TODO do something with form.cleaned_data['email']

            strategy = mcAlgorithmV2() if model_version_info['model_variant'] == "v2" else None

            # grouper is just an object that has not groupbed anything yet.
            grouped_data = CEPSchoolGroupGenerator(funding_rules, strategy).get_groups(data)

            summary_df = summarize_group(grouped_data, cfg)
            data = grouper.get_group_bundles(data)

        except (ValueError, KeyError):
            raise ValidationError("State or District was invalid")
        return data

    def dataframe_and_metadata(self, form):
        try:
            data = bu.dataFrameAndMetadataFromXL(form.cleaned_data['district_data_file'])
        except (ValueError, KeyError):
            raise ValidationError("Data File couldn't be parsed, " +
                                  "make sure to keep the headers and don't leave blank lines.")
        return data

class SchoolGroup(PandasSimpleView):

    def get_data(self, df, *args, **kwargs):
        return df


class ContactPageView(TemplateView):
    template_name = "contact.html"

