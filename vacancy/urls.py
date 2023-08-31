from rest_framework.routers import DefaultRouter
from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.vacancy, name="manager_vacancies"),
    path('<int:id_company>/manager_vacancies', views.company_manager_vacancies, name="company_manager_vacancies"),
    path('<int:id_company>/add_vacancy/', views.add_vacancy, name="add_vacancy"),
    path('<int:id_company>/company_list_vacancy/', views.company_list_vacancy, name="company_list_vacancy"),
    path('<int:id_company>/details_company_vacancy/<int:id_vacancy>/', views.details_company_vacancy, name="details_company_vacancy"),
    path('details_vacancy/<int:id_vacancy>/', views.details_vacancy, name="details_vacancy"),
    path('edit_vacancy/<int:id_vacancy>/basic_info/', views.EditBasicInfoVacancy.as_view(), name="edit_basic_info"),
    path('edit_vacancy/<int:id_vacancy>/requirements/', views.EditRequirementsVacancy.as_view(), name="edit_requirements"),
    path('edit_vacancy/<int:id_vacancy>/edit_pcd/', views.EditPCDVacancy.as_view(), name="edit_pcd"),
    path('edit_vacancy/<int:id_vacancy>/edit_benefits/', views.EditBenefitsVacancy.as_view(), name="edit_benefits"),
    path('edit_vacancy/<int:id_vacancy>/edit_details/', views.EditDetailsVacancy.as_view(), name="edit_details"),
    path('vacancy_completed/<int:id_vacancy>/', views.VacancyCompleted.as_view(), name="vacancy_completed"),
    path('list_vacancy/', views.list_vacancy, name="list_vacancy"),
]
