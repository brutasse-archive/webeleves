from django import forms
from django.contrib.admin import widgets

from trombi.models import UserProfile

class MainProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio', 'surname', 'picture', 'date_of_birth',
                'address', 'zip_code', 'town', 'country',
                'mobile_phone', 'landline', 'external_email',
        )

    def __init__(self, *args, **kwargs):
        super(MainProfileForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].widget = widgets.AdminDateWidget()


class NetworkForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('site', 'linkedin', 'facebook', 'twitter', 'openid', 'msn')

class ScholarshipForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('generic_axis_1', 'generic_axis_2', 'generic_axis_3',
                'option')
