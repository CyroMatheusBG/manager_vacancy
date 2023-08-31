from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import permissions
from django.urls import reverse_lazy
from django.shortcuts import render
from .form import *

@login_required(login_url='/login')
def manager_users(request):
    all_users = User.objects.all()
    return render(request, 'users/manager_users.html', {"users":all_users})

class EditUser(UpdateView):
    permission_classes = [User.is_authenticated]
    template_name = "users/edit_user.html"
    model = User
    form_class = UserForm
    context_object_name = "User"
    pk_url_kwarg = "id_user"

    def get_success_url(self):
        return reverse_lazy('manager_users')

class DeleteUser(DeleteView):
    permission_classes = [User.is_authenticated]
    model = User
    context_object_name = "User"
    pk_url_kwarg = "id_user"
    template_name = "users/user_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy('manager_users')

@login_required(login_url='/login')
def add_user(request):
    return render(request, 'users/add_user.html', {"form": UserForm})

@login_required(login_url='/login')
def save_user(request):
    user = request.user
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.user = request.user
            new_user.save()
            users = User.objects.all()
            print(user)
            # return HttpResponseRedirect(reverse('manager_users'))
