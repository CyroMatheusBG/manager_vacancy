from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
import vacancy.views as vacancy

urlpatterns = [
    path(r'^search_company', views.search_company, name='search_company'),
    path(r'^save_company', views.save_company, name='save_company'),
    path('', views.company, name="manager_companies"),
    path('add_company/', views.AddCompany.as_view(), name="add_company"),
    path('<int:id_company>/manager_contacts/', views.manager_contacts, name="manager_contacts"),
    path('<int:id_company>/manager_contacts/add_contact/', views.AddContact.as_view(), name="add_contact"),
    path('<int:id_company>/manager_contacts/edit_contact/<int:id_contact>', views.EditContact.as_view(), name="edit_contact"),
    path('<int:id_company>/manager_contacts/delete_contact/<int:id_contact>', views.DeleteContact.as_view(), name="delete_contact"),
    path('list_companies/', views.list_companies, name="list_companies"),
    path('<int:id>/', views.details_company, name="details_company"),
]