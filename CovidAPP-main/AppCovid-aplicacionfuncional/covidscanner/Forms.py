from django import forms

from covidscanner.models import Passports

class ImageForm(forms.ModelForm):
    class Meta:
        model = Passports
        fields = ("passports","email")
    

class EmailForm(forms.Form):
    email_field = forms.EmailField()

