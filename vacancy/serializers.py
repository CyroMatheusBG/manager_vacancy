from rest_framework import serializers
from django.forms import ModelForm
from .models import *

class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = '__all__'
