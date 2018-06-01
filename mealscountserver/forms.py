from django import forms
from .models import state_or_province_choices


class UploadCSVForm(forms.Form):
    state = forms.ChoiceField(
                              choices=state_or_province_choices,
                              label="Which state/province is this school district?",
                              initial='CA',
                              required=True)
    district = forms.CharField(max_length=100, label='School district')
    file = forms.FileField(label="Once it's filled out, upload the district data file here and press submit.")