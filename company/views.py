from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions, generics
from django.db.models import Q, Count, Case, When
from django.views.generic.edit import UpdateView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib import messages
from vacancy.models import *
from .serializers import *
from .models import *
import requests, pprint
import company.form as form

class AddCompany(CreateView):
    permission_classes = [User.is_authenticated]
    model = Company
    form_class = form.FormCompany
    template_name = "company/add_company.html"
    success_url = reverse_lazy('list_companies')

    def get_success_url(self):
        return reverse_lazy('manager_contacts', kwargs={'id_company': self.kwargs['id_company']})

class AddContact(CreateView):
    permission_classes = [User.is_authenticated]
    model = Contact
    form_class = form.FormContact
    template_name = "company/add_contact.html"
    pk_url_kwarg = "id_company"

    def get_context_data(self, **kwargs):
        context = super(AddContact, self).get_context_data(**kwargs)
        context['id_company'] = self.kwargs.get('id_company')
        return context

    def get_success_url(self):
        return reverse_lazy('manager_contacts', kwargs={'id_company': self.kwargs['id_company']})

class EditContact(UpdateView):
    permission_classes = [User.is_authenticated]
    template_name = "company/edit_contact.html"
    model = Contact
    form_class = form.FormContact
    context_object_name = "Contact"
    pk_url_kwarg = "id_contact"

    def get_success_url(self):
        return reverse_lazy('manager_contacts', kwargs={'id_company': self.object.company.id})

class DeleteContact(DeleteView):
    permission_classes = [User.is_authenticated]
    model = Contact
    context_object_name = "Contact"
    pk_url_kwarg = "id_contact"
    template_name = "company/contact_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy('manager_contacts', kwargs={'id_company': self.object.company.id})

@login_required(login_url='/login')
def company(request):
    return render(request, 'company/index.html')

@login_required(login_url='/login')
def details_company(request, id):
    company = Company.objects.filter(id=id)
    details_company = {
        "company": company[0],
        "len_vacancies": len(list(Vacancy.objects.filter(company=id))),
        "completed_by_here": len(list(Vacancy.objects.filter(company=id).filter(completed_by_here=True)))
    }
    return render(request, 'company/details_company.html', details_company)

@login_required(login_url='/login')
def manager_contacts(request, id_company):
    contacts = Contact.objects.filter(company=id_company)

    data_contacts = {
        "id_company": id_company,
        "contacts": contacts,
    }

    return render(request, 'company/manager_contacts.html', data_contacts)

@login_required(login_url='/login')
def list_companies(request):
    companies = Company.objects.all()
    return render(request, 'company/list_companies.html', {"companies": companies})

@login_required(login_url='/login')
def search_company(request):
    cnpj = ""

    for value in request.POST["cnpj"]:
        if value.isnumeric():
            cnpj+=value

    print(cnpj)

    data_company = dict(requests.get(f'https://publica.cnpj.ws/cnpj/{cnpj}').json())
    if "status" in data_company and data_company["status"] == 400:
        data_company["form"] = CompanyForm
        messages.add_message(request, messages.ERROR, 'CNPJ INVALIDO!')
        return render(request, 'company/add_company.html', data_company)
    else:
        company_cnpj = request.POST["cnpj"]
        company_existing = Company.objects.filter(cnpj=company_cnpj)
        if len(list(company_existing)) != 0:
            data_company["form"] = CompanyForm
            messages.add_message(request, messages.ERROR, 'CNPJ JÁ CADASTRADO!')
            return render(request, 'company/add_company.html', data_company)
        cnpj = f'{data_company["estabelecimento"]["cnpj"][:2]}.{data_company["estabelecimento"]["cnpj"][2:5]}.' \
               f'{data_company["estabelecimento"]["cnpj"][5:8]}/{data_company["estabelecimento"]["cnpj"][8:12]}-' \
               f'{data_company["estabelecimento"]["cnpj"][12:]}'
        company = {
            "data_company":(
                ("razao_social", data_company["razao_social"]),
                ("nome_fantasia", data_company["estabelecimento"]["nome_fantasia"]),
                ("cnpj", cnpj),
                ("cep", data_company["estabelecimento"]["cep"]),
                ("cidade", data_company["estabelecimento"]["cidade"]["nome"]),
                ("bairro", data_company["estabelecimento"]["bairro"]),
                ("rua", data_company["estabelecimento"]["logradouro"]),
                ("estado", data_company["estabelecimento"]["estado"]["sigla"]),
                ("complemento", data_company["estabelecimento"]["complemento"]),
            ),
            "CompanyForm": CompanyForm
        }
        return render(request, 'company/add_company.html', company)

@login_required(login_url='/login')
def save_company(request):
    user = request.user
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.user = request.user
            company.save()
            return HttpResponseRedirect(reverse('details_company', kwargs={'id':company.id}))
