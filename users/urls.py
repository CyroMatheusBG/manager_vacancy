from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('manager_users/', views.manager_users, name="manager_users"),
    path('add_user/', views.add_user, name="add_user"),
    path('edit_user/<int:id_user>', views.EditUser.as_view(), name="edit_user"),
    path('delete_user/<int:id_user>', views.DeleteUser.as_view(), name="delete_user"),
    path(r'^save_user', views.save_user, name='save_user'),
]