# mealscountserver/views.py
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from .forms import DistrictForm
from . import backend_utils as bu
from . import config_parser as cp
from .national_program_algorithm import mcAlgorithmV2, CEPSchoolGroupGenerator
from pathlib import Path
import json

config = json.load(Path(__file__).parent.parent.joinpath('config', 'national_config.json').open())

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
                    data = bu.mcXLSchoolDistInput(form.cleaned_data['district_data_file'])
                except (ValueError, KeyError):
                    raise ValidationError("Data File couldn't be parsed, " +
                                          "make sure to keep the headers and don't leave blank lines.")
                try:
                    # TODO do something with form.cleaned_data['email']

                    CONFIG_FILE = "national_config.json"


                    cfg = cp.mcModelConfig(Path(__file__).parent.parent.joinpath('config',CONFIG_FILE))

                    strategy = mcAlgorithmV2() if cfg.model_variant() == "v2" else None

                    grouper = CEPSchoolGroupGenerator(cfg, strategy)

                    html_data = grouper.get_group_bundles(data, "html")

                except (ValueError, KeyError):
                    raise ValidationError("State or District was invalid")
            else:
                raise ValueError('form was invalid')
        except (ValueError, KeyError):
            raise ValidationError("Are you sure you filled out the fields?")

        try:
            form.save()
        except:
            raise
        return render(request, "results.html",
                      {'html_data': html_data})



class ContactPageView(TemplateView):
    template_name = "contact.html"

