from django import forms

class StartRentalForm(forms.Form):
    username = forms.CharField(max_length=150)
    title = forms.CharField(max_length=255)
