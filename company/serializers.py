from rest_framework import serializers
from django.forms import ModelForm
from .models import *

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = "__all__"
