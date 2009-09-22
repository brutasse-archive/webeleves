# -*- coding: utf-8 -*-
from django import forms

from datetime import datetime

from trombi.models import UserProfile

class DateWidget(forms.TextInput):
    def render(self, name, value, attrs=None):
        # This is an ugly hack but I didn't find another way to do it...
        if '%s' % type(value) == '<type \'datetime.date\'>':
            value = value.strftime("%d/%m/%Y")

        return super(DateWidget, self).render(name, value, attrs)

class MainProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio', 'surname', 'date_of_birth', 'corridor', 'room',
                'address', 'zip_code', 'town', 'country',
                'mobile_phone', 'landline', 'external_email',
        )

    def __init__(self, *args, **kwargs):
        super(MainProfileForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].widget = DateWidget()
        self.fields['date_of_birth'].input_formats = ['%d/%m/%Y']
        self.fields['address'].widget.attrs['rows'] = 3

class MEForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('corridor', 'room')


class NetworkForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('site', 'linkedin', 'facebook', 'twitter', 'openid', 'msn')

    #def __init__(self, *args, **kwargs):
    #    super(NetworkForm, self).__init__(*args, **kwargs)

class ScholarshipForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('generic_axis_1', 'generic_axis_2', 'generic_axis_3',
                'option')


class SearchForm(forms.Form):
    q = forms.CharField(help_text='Nom, prénom, login')
