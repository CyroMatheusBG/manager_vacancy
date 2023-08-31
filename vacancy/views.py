from django.http import HttpResponseRedirect, HttpResponse
from rest_framework import viewsets, permissions, generics
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.shortcuts import render
from datetime import datetime
from .models import *
import vacancy.form as form
import requests, pprint

@login_required(login_url='/login')
def company_manager_vacancies(request, id_company):
    vacancies = Vacancy.objects.filter(company=id_company)

    for key, value in enumerate(vacancies):
        if int(value.tipo_vaga) == 0:
            vacancies[key].tipo_vaga = "CLT"
        elif int(value.tipo_vaga) == 1:
            vacancies[key].tipo_vaga = "Contrato"
        elif int(value.tipo_vaga) == 2:
            vacancies[key].tipo_vaga = "Estágio"

    data_vacancies = {
        "id_company": id_company,
        "vacancies": vacancies
    }
    return render(request, 'vacancy/company_manager_vacancies.html', data_vacancies)

@login_required(login_url='/login')
def add_vacancy(request, id_company):
    data_company = {
        "id_company": id_company,
    }

    if not "date_time_start_session" in request.session.keys():
        for key in list(request.session.keys()):
            del request.session[key]

    if len(request.session.items()) == 0 and len(request.POST) == 0:
        data_company.update({"basicInfo": form.VacancyFormBasicInfo})


    if "ocupacao" in request.POST:
        FormBasicInfo = form.VacancyFormBasicInfo(request.POST)
        if FormBasicInfo.is_valid():
            set_session_vacancy(request, id_company)
            data_company.update({
                    "SavedBasicInfo": data_temp_save_in_session(request, 1)
                })
            data_company.update({"requeriments": form.VacancyFormRequirements})
        else:
            data_company.update({"basicInfo": form.VacancyFormBasicInfo})
    if "escolaridade" in request.POST:
        FormRequirements = form.VacancyFormRequirements(request.POST)
        if FormRequirements.is_valid():
            set_session_vacancy(request, id_company)
            data_company.update({
                "SavedBasicInfo": data_temp_save_in_session(request, 1)
            })
            data_company.update({
                "SavedRequirements": data_temp_save_in_session(request, 2)
            })
            data_company.update({"pcd": form.VacancyFormPCD})
        else:
            data_company.update({"requeriments": form.VacancyFormRequirements})
    if (len(request.POST) == 1 and "csrfmiddlewaretoken" and "escolaridade" in request.session.keys()) or ("checkBoxPcd" in request.POST):
        FormPCD = form.VacancyFormPCD(request.POST)
        if FormPCD.is_valid():
            fields_pcd = [
                'pcd_auditiva',
                'pcd_mental',
                'pcd_nanismo',
                'pcd_visao',
                'pcd_membros_superiores',
                'pcd_membros_inferiores',
            ]
            for field in fields_pcd:
                if field in request.POST:
                    request.session[field] = True
                else:
                    request.session[field] = False
            data_company.update({
                "SavedBasicInfo": data_temp_save_in_session(request, 1)
            })
            data_company.update({
                "SavedRequirements": data_temp_save_in_session(request, 2)
            })
            data_company.update({
                "SavedPcd": data_temp_save_in_session(request, 3)
            })
            data_company.update({"benefits": form.VacancyFormBenefits})
    if "salario_fixo" in request.POST:
        FormBenefits = form.VacancyFormBenefits(request.POST)
        if FormBenefits.is_valid():
            request.session["salario_fixo"] = request.POST["salario_fixo"]
            request.session["percentual"] = request.POST["percentual"]
            benedits_fields = ["comissao", "transporte", "refeicao", "transporte_empresa", "refeitorio_empresa", "ass_medica", "ass_odonto", "seguro_vida", "add_noturno", "cesta_basica", "add_periculosidade", "uniforme", "auxilio_creche"]
            for field in benedits_fields:
                if field in request.POST:
                    request.session[field] = True
                else:
                    request.session[field] = False
            data_company.update({
                "SavedBasicInfo": data_temp_save_in_session(request, 1)
            })
            data_company.update({
                "SavedRequirements": data_temp_save_in_session(request, 2)
            })
            data_company.update({
                "SavedPcd": data_temp_save_in_session(request, 3)
            })
            data_company.update({
                "SavedBenefits": data_temp_save_in_session(request, 4)
            })

            data_company.update({"details": form.VacancyFormDetails})
        else:
            data_company.update({"details": form.VacancyFormRequirements})
    if "data_entrevista" in request.POST:
        FormDetails = form.VacancyFormDetails(request.POST)
        if FormDetails.is_valid():
            set_session_vacancy(request, id_company)
            VacancyFormCompleted = form.VacancyFormCompleted(request.session)
            if VacancyFormCompleted.is_valid():
                vacancy = VacancyFormCompleted.save(commit=False)
                vacancy.user = request.user
                vacancy.save()
                for key in list(request.session.keys()):
                    del request.session[key]
                return HttpResponseRedirect(reverse('company_list_vacancy', kwargs={"id_company":vacancy.company.id}))
        else:
            data_company.update({"details": form.VacancyFormRequirements})
    return render(request, 'vacancy/add_user.html', data_company)

@login_required(login_url='/login')
def set_session_vacancy(request, id_company):
    fields = [
        'ocupacao', 'tipo_vaga', 'descricao_atividade', 'observacoes',
        'local_trabalho', 'local_entrevista', 'quantidade_vagas', 'jornada_trabalho',
        'experiencia_comprovada', 'tempo_experiencia', 'tipo_tempo', 'escolaridade',
        'curso', 'semestre', 'cnh', 'language', 'nivel', 'perfil_comportamental',
        'pcd_auditiva', 'pcd_mental', 'pcd_nanismo', 'pcd_visao', 'pcd_membros_superiores',
        'pcd_membros_inferiores', 'salario_fixo', 'comissao', 'percentual', 'transporte',
        'refeicao', 'transporte_empresa', 'refeitorio_empresa', 'ass_medica', 'ass_odonto',
        'seguro_vida', 'add_noturno', 'cesta_basica', 'add_periculosidade', 'uniforme',
        'auxilio_creche', 'exp_imprescindivel', 'exp_desejavel', 'extra_info', 'data_entrevista'
    ]

    if len(request.session.items()) == 0:
        request.session["date_time_start_session"] = str(datetime.now())[:19]
        request.session["company"] = id_company
        request.session["status"] = True
        request.session["completed_by_here"] = False
    if request.session["date_time_start_session"]:
        now = datetime.now()
        session_start = datetime.strptime(request.session["date_time_start_session"][2:19].replace("-", "/"), '%y/%m/%d %H:%M:%S')
        diference_days = now - session_start
        diference_minutes = int(str(diference_days).split(":")[1])

        if "days" in str(diference_days) or diference_minutes > 20:
            for key in list(request.session.keys()):
                del request.session[key]

            for data_vacancy in request.POST:
                if data_vacancy in fields and not data_vacancy in request.session.keys():
                    request.session[data_vacancy] = request.POST[data_vacancy]
        else:
            for data_vacancy in request.POST:
                if data_vacancy in fields and not data_vacancy in request.session.keys():
                    request.session[data_vacancy] = request.POST[data_vacancy]
                elif data_vacancy in request.session.keys() and diference_minutes < 20:
                    pass

@login_required(login_url='/login')
def getsession(request):
    # for key in list(request.session.keys()):
    #     del request.session[key]

    # VacancyFormCompleted = form.VacancyFormCompleted(request.session)
    # if VacancyFormCompleted.is_valid():
    #     vacancy = VacancyFormCompleted.save(commit=False)
    #     vacancy.user = request.user
    #     vacancy.save()
    #     print(vacancy.id)

    string_return = "<table>"
    for key in request.session.items():
        string_return += "<tr>"
        string_return += "<th>"+str(key[0])+"</th>"
        string_return += "<td>&emsp;&emsp;&emsp;</td><td>"+str(key[1])+"</td>"
        string_return += "</tr>"
    string_return += "</table>"

    return HttpResponse(string_return)

@login_required(login_url='/login')
def vacancy(request):
    return render(request, 'vacancy/index.html')

@login_required(login_url='/login')
def list_vacancy(request):
    vacancies = Vacancy.objects.filter(status=True)
    vacancies_completed_by_here = Vacancy.objects.filter(completed_by_here=True)
    vacancies_completed = Vacancy.objects.filter(completed_by_here=False, status=False)

    for key, value in enumerate(vacancies):
        if int(value.tipo_vaga) == 0:
            vacancies[key].tipo_vaga = "CLT"
        elif int(value.tipo_vaga) == 1:
            vacancies[key].tipo_vaga = "Contrato"
        elif int(value.tipo_vaga) == 2:
            vacancies[key].tipo_vaga = "Estágio"
    for key, value in enumerate(vacancies_completed_by_here):
        if int(value.tipo_vaga) == 0:
            vacancies_completed_by_here[key].tipo_vaga = "CLT"
        elif int(value.tipo_vaga) == 1:
            vacancies_completed_by_here[key].tipo_vaga = "Contrato"
        elif int(value.tipo_vaga) == 2:
            vacancies_completed_by_here[key].tipo_vaga = "Estágio"
    for key, value in enumerate(vacancies_completed):
        if int(value.tipo_vaga) == 0:
            vacancies_completed[key].tipo_vaga = "CLT"
        elif int(value.tipo_vaga) == 1:
            vacancies_completed[key].tipo_vaga = "Contrato"
        elif int(value.tipo_vaga) == 2:
            vacancies_completed[key].tipo_vaga = "Estágio"

    paginator_list_vacancy = Paginator(vacancies, 3)
    page_list_vacancy = request.GET.get('page')
    vacancy_list = paginator_list_vacancy.get_page(page_list_vacancy)

    paginator_list_vacancy_competed_by_here = Paginator(vacancies_completed_by_here, 3)
    page_list_vacancy_completed_by_here = request.GET.get('page')
    list_vacancy_completed_by_here = paginator_list_vacancy_competed_by_here.get_page(
        page_list_vacancy_completed_by_here)

    paginator_list_vacancy_completed = Paginator(vacancies_completed, 3)
    page_list_vacancy_completed = request.GET.get('page')
    list_vacancy_completed = paginator_list_vacancy_completed.get_page(page_list_vacancy_completed)

    data_vacancies = {
        "list_vacancy_open": vacancy_list,
        "list_vacancy_completed_by_here": list_vacancy_completed_by_here,
        "list_vacancy_completed": list_vacancy_completed,
    }
    return render(request, 'vacancy/list_vacancy.html', data_vacancies)

@login_required(login_url='/login')
def details_vacancy(request, id_vacancy):
    vacancy = Vacancy.objects.filter(id=id_vacancy)

    data_vacancy_session = {
        "ocupacao": vacancy[0].ocupacao,
        "tipo_vaga": vacancy[0].tipo_vaga,
        "descricao_atividade": vacancy[0].descricao_atividade,
        "observacoes": vacancy[0].observacoes,
        "local_trabalho": vacancy[0].local_trabalho,
        "local_entrevista": vacancy[0].local_entrevista,
        "quantidade_vagas": vacancy[0].quantidade_vagas,
        "jornada_trabalho": vacancy[0].jornada_trabalho,
        "experiencia_comprovada": vacancy[0].experiencia_comprovada,
        "tempo_experiencia": vacancy[0].tempo_experiencia,
        "tipo_tempo": vacancy[0].tipo_tempo,
        "escolaridade": vacancy[0].escolaridade,
        "curso": vacancy[0].curso,
        "semestre": vacancy[0].semestre,
        "cnh": vacancy[0].cnh,
        "language": vacancy[0].language,
        "nivel": vacancy[0].nivel,
        "perfil_comportamental": vacancy[0].perfil_comportamental,
        "pcd_auditiva": vacancy[0].pcd_auditiva,
        "pcd_mental": vacancy[0].pcd_mental,
        "pcd_nanismo": vacancy[0].pcd_nanismo,
        "pcd_visao": vacancy[0].pcd_visao,
        "pcd_membros_superiores": vacancy[0].pcd_membros_superiores,
        "pcd_membros_inferiores": vacancy[0].pcd_membros_inferiores,
        "salario_fixo": vacancy[0].salario_fixo,
        "comissao": vacancy[0].comissao,
        "percentual": vacancy[0].percentual,
        "transporte": vacancy[0].transporte,
        "refeicao": vacancy[0].refeicao,
        "transporte_empresa": vacancy[0].transporte_empresa,
        "refeitorio_empresa": vacancy[0].refeitorio_empresa,
        "ass_medica": vacancy[0].ass_medica,
        "ass_odonto": vacancy[0].ass_odonto,
        "seguro_vida": vacancy[0].seguro_vida,
        "add_noturno": vacancy[0].add_noturno,
        "cesta_basica": vacancy[0].cesta_basica,
        "add_periculosidade": vacancy[0].add_periculosidade,
        "uniforme": vacancy[0].uniforme,
        "auxilio_creche": vacancy[0].auxilio_creche,
        "exp_imprescindivel": vacancy[0].exp_imprescindivel,
        "exp_desejavel": vacancy[0].exp_desejavel,
        "extra_info": vacancy[0].extra_info,
        "data_entrevista": vacancy[0].data_entrevista
    }

    for data in data_vacancy_session:
        request.session[data] = data_vacancy_session[data]

    data_vacancy = {
        "id_company": vacancy[0].company.id,
        "id_vacancy": id_vacancy,
        "status": vacancy[0].status,
        "BasicInfo": data_temp_save_in_session(request, 1),
        "Requirements": data_temp_save_in_session(request, 2),
        "PCD": data_temp_save_in_session(request, 3),
        "Benefits": data_temp_save_in_session(request, 4),
        "Details": data_temp_save_in_session(request, 5),
    }

    for key in list(request.session.keys()):
        del request.session[key]

    return render(request, 'vacancy/details_vacancy.html', data_vacancy)

@login_required(login_url='/login')
def company_list_vacancy(request, id_company):
    vacancies = Vacancy.objects.filter(company=id_company, status=True)
    vacancies_completed_by_here = Vacancy.objects.filter(company=id_company, completed_by_here=True)
    vacancies_completed = Vacancy.objects.filter(company=id_company, completed_by_here=False, status=False)

    for key, value in enumerate(vacancies):
        if int(value.tipo_vaga) == 0:
            vacancies[key].tipo_vaga = "CLT"
        elif int(value.tipo_vaga) == 1:
            vacancies[key].tipo_vaga = "Contrato"
        elif int(value.tipo_vaga) == 2:
            vacancies[key].tipo_vaga = "Estágio"
    for key, value in enumerate(vacancies_completed_by_here):
        if int(value.tipo_vaga) == 0:
            vacancies_completed_by_here[key].tipo_vaga = "CLT"
        elif int(value.tipo_vaga) == 1:
            vacancies_completed_by_here[key].tipo_vaga = "Contrato"
        elif int(value.tipo_vaga) == 2:
            vacancies_completed_by_here[key].tipo_vaga = "Estágio"
    for key, value in enumerate(vacancies_completed):
        if int(value.tipo_vaga) == 0:
            vacancies_completed[key].tipo_vaga = "CLT"
        elif int(value.tipo_vaga) == 1:
            vacancies_completed[key].tipo_vaga = "Contrato"
        elif int(value.tipo_vaga) == 2:
            vacancies_completed[key].tipo_vaga = "Estágio"

    paginator_list_vacancy = Paginator(vacancies, 3)
    page_list_vacancy = request.GET.get('page')
    vacancy_list = paginator_list_vacancy.get_page(page_list_vacancy)

    paginator_list_vacancy_competed_by_here = Paginator(vacancies_completed_by_here, 3)
    page_list_vacancy_completed_by_here = request.GET.get('page')
    list_vacancy_completed_by_here = paginator_list_vacancy_competed_by_here.get_page(page_list_vacancy_completed_by_here)

    paginator_list_vacancy_completed = Paginator(vacancies_completed, 3)
    page_list_vacancy_completed = request.GET.get('page')
    list_vacancy_completed = paginator_list_vacancy_completed.get_page(page_list_vacancy_completed)

    data_vacancies = {
        "id_company": id_company,
        "list_vacancy_open": vacancy_list,
        "list_vacancy_completed_by_here": list_vacancy_completed_by_here,
        "list_vacancy_completed": list_vacancy_completed,
    }
    return render(request, 'vacancy/list_vacancy.html', data_vacancies)

@login_required(login_url='/login')
def details_company_vacancy(request, id_company, id_vacancy):
    vacancy = Vacancy.objects.filter(id=id_vacancy)

    data_vacancy_session = {
        "ocupacao": vacancy[0].ocupacao,
        "tipo_vaga": vacancy[0].tipo_vaga,
        "descricao_atividade": vacancy[0].descricao_atividade,
        "observacoes": vacancy[0].observacoes,
        "local_trabalho": vacancy[0].local_trabalho,
        "local_entrevista": vacancy[0].local_entrevista,
        "quantidade_vagas": vacancy[0].quantidade_vagas,
        "jornada_trabalho": vacancy[0].jornada_trabalho,
        "experiencia_comprovada": vacancy[0].experiencia_comprovada,
        "tempo_experiencia": vacancy[0].tempo_experiencia,
        "tipo_tempo": vacancy[0].tipo_tempo,
        "escolaridade": vacancy[0].escolaridade,
        "curso": vacancy[0].curso,
        "semestre": vacancy[0].semestre,
        "cnh": vacancy[0].cnh,
        "language": vacancy[0].language,
        "nivel": vacancy[0].nivel,
        "perfil_comportamental": vacancy[0].perfil_comportamental,
        "pcd_auditiva": vacancy[0].pcd_auditiva,
        "pcd_mental": vacancy[0].pcd_mental,
        "pcd_nanismo": vacancy[0].pcd_nanismo,
        "pcd_visao": vacancy[0].pcd_visao,
        "pcd_membros_superiores": vacancy[0].pcd_membros_superiores,
        "pcd_membros_inferiores": vacancy[0].pcd_membros_inferiores,
        "salario_fixo": vacancy[0].salario_fixo,
        "comissao": vacancy[0].comissao,
        "percentual": vacancy[0].percentual,
        "transporte": vacancy[0].transporte,
        "refeicao": vacancy[0].refeicao,
        "transporte_empresa": vacancy[0].transporte_empresa,
        "refeitorio_empresa": vacancy[0].refeitorio_empresa,
        "ass_medica": vacancy[0].ass_medica,
        "ass_odonto": vacancy[0].ass_odonto,
        "seguro_vida": vacancy[0].seguro_vida,
        "add_noturno": vacancy[0].add_noturno,
        "cesta_basica": vacancy[0].cesta_basica,
        "add_periculosidade": vacancy[0].add_periculosidade,
        "uniforme": vacancy[0].uniforme,
        "auxilio_creche": vacancy[0].auxilio_creche,
        "exp_imprescindivel": vacancy[0].exp_imprescindivel,
        "exp_desejavel": vacancy[0].exp_desejavel,
        "extra_info": vacancy[0].extra_info,
        "data_entrevista": vacancy[0].data_entrevista
    }

    for data in data_vacancy_session:
        request.session[data] = data_vacancy_session[data]

    print(vacancy[0].status)
    data_vacancy = {
        "id_company": id_company,
        "id_vacancy": id_vacancy,
        "status": vacancy[0].status,
        "BasicInfo": data_temp_save_in_session(request, 1),
        "Requirements": data_temp_save_in_session(request, 2),
        "PCD": data_temp_save_in_session(request, 3),
        "Benefits": data_temp_save_in_session(request, 4),
        "Details": data_temp_save_in_session(request, 5),
    }

    for key in list(request.session.keys()):
        del request.session[key]

    return render(request, 'vacancy/details_vacancy.html', data_vacancy)

@login_required(login_url='/login')
def edit_vacancy(request, id_vacancy, stage):
    vacancy = Vacancy.objects.filter(id=id_vacancy)

    data_vacancy_session = {
        "ocupacao": vacancy[0].ocupacao,
        "tipo_vaga": vacancy[0].tipo_vaga,
        "descricao_atividade": vacancy[0].descricao_atividade,
        "observacoes": vacancy[0].observacoes,
        "local_trabalho": vacancy[0].local_trabalho,
        "local_entrevista": vacancy[0].local_entrevista,
        "quantidade_vagas": vacancy[0].quantidade_vagas,
        "jornada_trabalho": vacancy[0].jornada_trabalho,
        "experiencia_comprovada": vacancy[0].experiencia_comprovada,
        "tempo_experiencia": vacancy[0].tempo_experiencia,
        "tipo_tempo": vacancy[0].tipo_tempo,
        "escolaridade": vacancy[0].escolaridade,
        "curso": vacancy[0].curso,
        "semestre": vacancy[0].semestre,
        "cnh": vacancy[0].cnh,
        "language": vacancy[0].language,
        "nivel": vacancy[0].nivel,
        "perfil_comportamental": vacancy[0].perfil_comportamental,
        "pcd_auditiva": vacancy[0].pcd_auditiva,
        "pcd_mental": vacancy[0].pcd_mental,
        "pcd_nanismo": vacancy[0].pcd_nanismo,
        "pcd_visao": vacancy[0].pcd_visao,
        "pcd_membros_superiores": vacancy[0].pcd_membros_superiores,
        "pcd_membros_inferiores": vacancy[0].pcd_membros_inferiores,
        "salario_fixo": vacancy[0].salario_fixo,
        "comissao": vacancy[0].comissao,
        "percentual": vacancy[0].percentual,
        "transporte": vacancy[0].transporte,
        "refeicao": vacancy[0].refeicao,
        "transporte_empresa": vacancy[0].transporte_empresa,
        "refeitorio_empresa": vacancy[0].refeitorio_empresa,
        "ass_medica": vacancy[0].ass_medica,
        "ass_odonto": vacancy[0].ass_odonto,
        "seguro_vida": vacancy[0].seguro_vida,
        "add_noturno": vacancy[0].add_noturno,
        "cesta_basica": vacancy[0].cesta_basica,
        "add_periculosidade": vacancy[0].add_periculosidade,
        "uniforme": vacancy[0].uniforme,
        "auxilio_creche": vacancy[0].auxilio_creche,
        "exp_imprescindivel": vacancy[0].exp_imprescindivel,
        "exp_desejavel": vacancy[0].exp_desejavel,
        "extra_info": vacancy[0].extra_info,
        "data_entrevista": vacancy[0].data_entrevista
    }

    for data in data_vacancy_session:
        request.session[data] = data_vacancy_session[data]

    data_vacancy = {
        "status": vacancy[0].status,
        "BasicInfo": data_temp_save_in_session(request, 1),
        "Requirements": data_temp_save_in_session(request, 2),
        "PCD": data_temp_save_in_session(request, 3),
        "Benefits": data_temp_save_in_session(request, 4),
        "Details": data_temp_save_in_session(request, 5),
    }

    if stage == "BasicInfo":
        data_vacancy.update({"FormBasicInfo": form.VacancyFormBasicInfo})
    elif stage == "Requirements":
        data_vacancy.update({"FormRequirements": form.VacancyFormRequirements})
    elif stage == "PCD":
        data_vacancy.update({"FormPCD": form.VacancyFormPCD})
    elif stage == "Benefits":
        data_vacancy.update({"FormBenefits": form.VacancyFormBenefits})
    elif stage == "Details":
        data_vacancy.update({"FormDetails": form.VacancyFormDetails})

    for key in list(request.session.keys()):
        del request.session[key]

    return render(request, 'vacancy/details_vacancy.html', data_vacancy)

class EditBasicInfoVacancy(UpdateView):
    permission_classes = [User.is_authenticated]
    template_name = "vacancy/edit_basic_info.html"
    model = Vacancy
    form_class = form.VacancyFormBasicInfo
    context_object_name = "Vacancy"
    pk_url_kwarg = "id_vacancy"

    def get_success_url(self):
        return reverse_lazy('details_vacancy', kwargs={'id_company': self.object.company.id, "id_vacancy": self.object.id})

class EditRequirementsVacancy(UpdateView):
    permission_classes = [User.is_authenticated]
    template_name = "vacancy/edit_requirements.html"
    model = Vacancy
    form_class = form.VacancyFormRequirements
    context_object_name = "Vacancy"
    pk_url_kwarg = "id_vacancy"

    def get_success_url(self):
        return reverse_lazy('details_vacancy', kwargs={'id_company': self.object.company.id, "id_vacancy": self.object.id})

class EditPCDVacancy(UpdateView):
    permission_classes = [User.is_authenticated]
    template_name = "vacancy/edit_pcd.html"
    model = Vacancy
    form_class = form.VacancyFormPCD
    context_object_name = "Vacancy"
    pk_url_kwarg = "id_vacancy"

    def get_success_url(self):
        return reverse_lazy('details_vacancy', kwargs={'id_company': self.object.company.id, "id_vacancy": self.object.id})

class EditBenefitsVacancy(UpdateView):
    permission_classes = [User.is_authenticated]
    template_name = "vacancy/edit_benefits.html"
    model = Vacancy
    form_class = form.VacancyFormBenefits
    context_object_name = "Vacancy"
    pk_url_kwarg = "id_vacancy"

    def get_success_url(self):
        return reverse_lazy('details_vacancy', kwargs={'id_company': self.object.company.id, "id_vacancy": self.object.id})

class EditDetailsVacancy(UpdateView):
    permission_classes = [User.is_authenticated]
    template_name = "vacancy/edit_benefits.html"
    model = Vacancy
    form_class = form.VacancyFormDetails
    context_object_name = "Vacancy"
    pk_url_kwarg = "id_vacancy"

    def get_success_url(self):
        return reverse_lazy('details_vacancy', kwargs={'id_company': self.object.company.id, "id_vacancy": self.object.id})

class VacancyCompleted(UpdateView):
    permission_classes = [User.is_authenticated]
    template_name = "vacancy/vacancy_completed.html"
    model = Vacancy
    form_class = form.FormVacancyCompleted
    context_object_name = "Vacancy"
    pk_url_kwarg = "id_vacancy"

    def get_success_url(self):
        return reverse_lazy('company_list_vacancy', kwargs={'id_company': self.object.company.id})

@login_required(login_url='/login')
def data_temp_save_in_session(request, stage):
    if stage == 1:
        tipo_vaga = request.session.get('tipo_vaga')
        if int(tipo_vaga) == 0:
            tipo_vaga = "CLT"
        elif int(tipo_vaga) == 1:
            tipo_vaga = "Contrato"
        elif int(tipo_vaga) == 2:
            tipo_vaga = "Estágio"

        SavedBasicInfo = (
            ("ocupacao", "Ocupação", request.session.get('ocupacao')),
            ("tipo_vaga", "Tipo da vaga", tipo_vaga),
            ("descricao_atividade", "Descrição da atividade", request.session.get('descricao_atividade')),
            ("observacoes", "Observações", request.session.get('observacoes')),
            ("local_trabalho", "Local do Trabalho", request.session.get('local_trabalho')),
            ("local_entrevista", "Local da Entrevista", request.session.get('local_entrevista')),
            ("quantidade_vagas", "Quantidade de vagas", request.session.get('quantidade_vagas')),
            ("jornada_trabalho", "Jornada de trabalho", request.session.get('jornada_trabalho')),
        )
        return SavedBasicInfo
    elif stage == 2:
        SavedRequirements = list

        if str(request.session.get("experiencia_comprovada")) != "":
            if int(request.session.get("experiencia_comprovada")) == 0:
                experiencia_comprovada = "CTPS"
            if int(request.session.get("experiencia_comprovada")) == 1:
                experiencia_comprovada = "Contrato"
            if int(request.session.get("experiencia_comprovada")) == 2:
                experiencia_comprovada = "Declaração"

            if int(request.session.get("tipo_tempo")) == 0:
                if int(request.session.get("tempo_experiencia")) > 1:
                    tipo_tempo = "meses"
                else:
                    tipo_tempo = "mes"
            elif int(request.session.get("tipo_tempo")) == 1:
                if int(request.session.get("tempo_experiencia")) > 1:
                    tipo_tempo = "anos"
                else:
                    tipo_tempo = "ano"
        else:
            experiencia_comprovada = "Sem experiência"

        if int(request.session.get("escolaridade")) == 0:
            escolaridade = "Ensino fundamental completo"
        elif int(request.session.get("escolaridade")) == 1:
            escolaridade = "Ensino médio completo"
        elif int(request.session.get("escolaridade")) == 2:
            escolaridade = "Cursando ensino médio"
        elif int(request.session.get("escolaridade")) == 3:
            escolaridade = "Cursando superior"
        elif int(request.session.get("escolaridade")) == 4:
            escolaridade = "Superior completo"
        elif int(request.session.get("escolaridade")) == 5:
            escolaridade = "Cursando técnico"
        elif int(request.session.get("escolaridade")) == 6:
            escolaridade = "Técnico completo"

        if request.session.get("cnh") != "":
            if int(request.session.get("cnh")) == 0:
                cnh = "CATEGORIA A"
            elif int(request.session.get("cnh")) == 1:
                cnh = "CATEGORIA B"
            elif int(request.session.get("cnh")) == 2:
                cnh = "CATEGORIA C"
            elif int(request.session.get("cnh")) == 3:
                cnh = "CATEGORIA D"
            elif int(request.session.get("cnh")) == 4:
                cnh = "CATEGORIA E"
        else:
            cnh = "Sem Habilitação"

        if request.session.get("language") != "":
            if int(request.session.get("language")) == 0:
                language = "Inglês"
            elif int(request.session.get("language")) == 1:
                language = "Espanhol"
            elif int(request.session.get("language")) == 2:
                language = "Francês"
            elif int(request.session.get("language")) == 3:
                language = "Chinês"
            elif int(request.session.get("language")) == 4:
                language = "Alemão"

            if int(request.session.get("nivel")) == 0:
                nivel = "Básico"
            elif int(request.session.get("nivel")) == 1:
                nivel = "Intermédiario"
            elif int(request.session.get("nivel")) == 2:
                nivel = "Avançado"
            elif int(request.session.get("nivel")) == 3:
                nivel = "Fluente"
        else:
            language = "Não Necessário"

        if int(request.session.get("perfil_comportamental")) == 0:
            perfil_comportamental = "Comunicador"
        elif int(request.session.get("perfil_comportamental")) == 1:
            perfil_comportamental = "Planejador"
        elif int(request.session.get("perfil_comportamental")) == 2:
            perfil_comportamental = "Executor"
        elif int(request.session.get("perfil_comportamental")) == 3:
            perfil_comportamental = "Comunicador"
        elif int(request.session.get("perfil_comportamental")) == 4:
            perfil_comportamental = "Analista"

        SavedRequirements = [
            ("experiencia_comprovada", "Experiencia Comprovada", experiencia_comprovada),
            ("escolaridade", "Escolaridade", escolaridade),
            ("cnh", "CNH", cnh),
            ("language", "Linguagem", language),
            ("perfil_comportamental", "Perfil Comportamental", perfil_comportamental),
        ]
        if request.session.get("experiencia_comprovada") != "":
            index = SavedRequirements.index(("experiencia_comprovada", "Experiencia Comprovada", experiencia_comprovada))
            SavedRequirements.insert(index+1, ("tempo_experiencia", "Tempo Experiência", request.session.get("tempo_experiencia")))
            SavedRequirements.insert(index+2, ("tipo_tempo", "Tipo de tempo", tipo_tempo))
        if request.session.get("escolaridade") == 3 or request.session.get("escolaridade") == 5:
            index = SavedRequirements.index(("escolaridade", "Escolaridade", escolaridade))
            SavedRequirements.insert(index+1, ("curso", "Curso", request.session.get("curso")))
            SavedRequirements.insert(index+2, ("semestre", "Semestre", request.session.get("semestre")))
        elif request.session.get("escolaridade") == 4 or request.session.get("escolaridade") == 6:
            index = SavedRequirements.index(("escolaridade", "Escolaridade", escolaridade))
            SavedRequirements.insert(index + 1, ("curso", "Curso", request.session.get("curso")))
        if request.session.get("language") != "":
            index = SavedRequirements.index(("language", "Linguagem", language))
            SavedRequirements.insert(index+1, ("nivel", "Nivel", nivel))
        return SavedRequirements
    elif stage == 3:
        SavedPCD = list()

        if request.session.get('pcd_auditiva') == True:
            SavedPCD.append(("pcd_auditiva", "Auditiva", True))
        else:
            SavedPCD.append(("pcd_auditiva", "Auditiva", False))
        if request.session.get('pcd_mental') == True:
            SavedPCD.append(("pcd_mental", "Mental", True))
        else:
            SavedPCD.append(("pcd_mental", "Mental", False))
        if request.session.get('pcd_nanismo') == True:
            SavedPCD.append(("pcd_nanismo", "Nanismo", True))
        else:
            SavedPCD.append(("pcd_nanismo", "Nanismo", False))
        if request.session.get('pcd_visao') == True:
            SavedPCD.append(("pcd_visao", "Visual", True))
        else:
            SavedPCD.append(("pcd_visao", "Visual", False))
        if request.session.get('pcd_membros_superiores') == True:
            SavedPCD.append(("pcd_membros_superiores", "Física: Membros superiores", True))
        else:
            SavedPCD.append(("pcd_membros_superiores", "Física: Membros superiores", False))
        if request.session.get('pcd_membros_inferiores') == True:
            SavedPCD.append(("pcd_membros_inferiores", "Física: Membros inferiores", True))
        else:
            SavedPCD.append(("pcd_membros_inferiores", "Física: Membros inferiores", False))

        return SavedPCD
    elif stage == 4:
        SavedBenefits = list()
        SavedBenefits.append(("salario_fixo", "Salário fixo", request.session.get('salario_fixo')))

        if request.session.get('comissao') == True:
            SavedBenefits.append(("comissao", "Comissão", True))
            SavedBenefits.append(("percentual", "Percentual", request.session.get('percentual')))
        else:
            SavedBenefits.append(("comissao", "Comissão", False))

        if request.session.get('transporte') == True:
            SavedBenefits.append(("transporte", "Transporte", True))
        else:
            SavedBenefits.append(("transporte", "Transporte", False))

        if request.session.get('refeicao') == True:
            SavedBenefits.append(("refeicao", "Refeição", True))
        else:
            SavedBenefits.append(("refeicao", "Refeição", False))

        if request.session.get('transporte_empresa') == True:
            SavedBenefits.append(("transporte_empresa", "Transporte da empresa", True))
        else:
            SavedBenefits.append(("transporte_empresa", "Transporte da empresa", False))

        if request.session.get('refeitorio_empresa') == True:
            SavedBenefits.append(("refeitorio_empresa", "Refeitório da empresa", True))
        else:
            SavedBenefits.append(("refeitorio_empresa", "Refeitório da empresa", False))

        if request.session.get('ass_medica') == True:
            SavedBenefits.append(("ass_medica", "Assistência médica", True))
        else:
            SavedBenefits.append(("ass_medica", "Assistência médica", False))

        if request.session.get('ass_odonto') == True:
            SavedBenefits.append(("ass_odonto", "Assistência odontológica", True))
        else:
            SavedBenefits.append(("ass_odonto", "Assistência odontológica", False))

        if request.session.get('seguro_vida') == True:
            SavedBenefits.append(("seguro_vida", "Seguro de vida", True))
        else:
            SavedBenefits.append(("seguro_vida", "Seguro de vida", False))

        if request.session.get('add_noturno') == True:
            SavedBenefits.append(("add_noturno", "Adicional noturno", True))
        else:
            SavedBenefits.append(("add_noturno", "Adicional noturno", False))

        if request.session.get('cesta_basica') == True:
            SavedBenefits.append(("cesta_basica", "Cesta básica", True))
        else:
            SavedBenefits.append(("cesta_basica", "Cesta básica", False))

        if request.session.get('add_periculosidade') == True:
            SavedBenefits.append(("add_periculosidade", "Adicional periculosidade", True))
        else:
            SavedBenefits.append(("add_periculosidade", "Adicional periculosidade", False))

        if request.session.get('uniforme') == True:
            SavedBenefits.append(("uniforme", "Uniforme", True))
        else:
            SavedBenefits.append(("uniforme", "Uniforme", False))

        if request.session.get('auxilio_creche') == True:
            SavedBenefits.append(("auxilio_creche", "Auxílio creche", True))
        else:
            SavedBenefits.append(("auxilio_creche", "Auxílio creche", False))

        return SavedBenefits
    elif stage == 5:
        SavedDetails = (
            ("exp_imprescindivel", "Experiência ou fator imprescindível", request.session.get('exp_imprescindivel')),
            ("exp_desejavel", "Experiência ou fator desejável", request.session.get('exp_desejavel')),
            ("extra_info", "Informações adicionais sobre a vaga", request.session.get('extra_info')),
            ("data_entrevista", "Data da entrevista", request.session.get('data_entrevista')),
        )
        return SavedDetails