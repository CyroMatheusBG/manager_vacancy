from django import forms
from .views import *

class FormContact(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"
        widgets = {'phone': forms.TextInput(attrs={'data-mask': "(00) 00000-0000"})}

class FormCompany(forms.ModelForm):
    class Meta:
        model = Company
        fields = "__all__"
        widgets = {'cnpj': forms.TextInput(attrs={'data-mask': "00.000.000/0000-00"})}