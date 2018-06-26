from django import forms
from .models import state_or_province_choices

from django import forms
from .models import District


class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = ('district_name', 'state_or_province', 'district_qualifies_for_performance_based_cash_assistance',
                  'district_data_file')
