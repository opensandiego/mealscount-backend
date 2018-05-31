from django import forms

class UploadCSVForm(forms.Form):
    state = forms.CharField(max_length=2,min_length=2,  label="two letter state/province abbreviation", initial='CA')
    district = forms.CharField(max_length=100, label='School district')
    file = forms.FileField(label="Once it's filled out, upload the district data file here and press submit.")