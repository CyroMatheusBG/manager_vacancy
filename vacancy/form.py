from rest_framework.exceptions import ValidationError
from django.forms import ModelForm
from django import forms
from .models import *
from .views import *
import requests

class VacancyFormBasicInfo(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = [
            'ocupacao',
            'tipo_vaga',
            'descricao_atividade',
            'observacoes',
            'local_trabalho',
            'local_entrevista',
            'quantidade_vagas',
            'jornada_trabalho',
        ]

class VacancyFormRequirements(ModelForm):
    class Meta:
        model = Vacancy
        fields = [
            'experiencia_comprovada',
            'tempo_experiencia',
            'tipo_tempo',
            'escolaridade',
            'curso',
            'semestre',
            'cnh',
            'language',
            'nivel',
            'perfil_comportamental',
        ]

class VacancyFormPCD(ModelForm):
    class Meta:
        model = Vacancy
        fields = [
            'pcd_auditiva',
            'pcd_mental',
            'pcd_nanismo',
            'pcd_visao',
            'pcd_membros_superiores',
            'pcd_membros_inferiores',
        ]

class VacancyFormBenefits(ModelForm):
    class Meta:
        model = Vacancy
        fields = [
            'salario_fixo',
            'comissao',
            'percentual',
            'transporte',
            'refeicao',
            'transporte_empresa',
            'refeitorio_empresa',
            'ass_medica',
            'ass_odonto',
            'seguro_vida',
            'add_noturno',
            'cesta_basica',
            'add_periculosidade',
            'uniforme',
            'auxilio_creche',
        ]

class VacancyFormDetails(ModelForm):
    class Meta:
        model = Vacancy
        fields = [
            'exp_imprescindivel',
            'exp_desejavel',
            'extra_info',
            'data_entrevista',
        ]

class VacancyFormCompleted(ModelForm):
    class Meta:
        model = Vacancy
        fields = "__all__"

class FormVacancyCompleted(ModelForm):
    class Meta:
        model = Vacancy
        fields = [
            "status",
            "completed_by_here"
        ]