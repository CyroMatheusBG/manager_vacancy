from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index, name="index"),
    path('login/', views.login_manager, name="login"),
    path(r'^check_login_valid', views.check_login_valid, name='check_login_valid'),
    # path('logout', views.logout_session, name="logout_session"),
    path('company/', include('company.urls')),
    path('vacancy/', include('vacancy.urls')),
    path('users/', include('users.urls')),
]