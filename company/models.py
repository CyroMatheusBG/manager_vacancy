from django.forms import ModelForm
from django.db import models

class Company(models.Model):
    #data_company
    razao_social = models.CharField(max_length=255)
    nome_fantasia = models.CharField(max_length=255, verbose_name="Nome fantasia")
    cnpj = models.CharField(max_length=18)

    #data_address
    cep = models.CharField(max_length=9, verbose_name="CEP")
    cidade = models.CharField(max_length=100, verbose_name="Cidade")
    bairro = models.CharField(max_length=100, verbose_name="Bairro")
    rua = models.CharField(max_length=255, verbose_name="Rua")
    estado = models.CharField(max_length=2, verbose_name="Estado")
    complemento = models.CharField(max_length=255, verbose_name="Complemento", blank=True)
    ponto_referencia = models.CharField(max_length=255, verbose_name="Ponto de referência")
    email = models.EmailField(max_length=255, verbose_name="E-mail para contato")

    def __str__(self):
        return "{} {}".format(self.nome_fantasia, self.cnpj)

class Contact(models.Model):
    phone = models.CharField(max_length=15, verbose_name="Telefone")
    whatsapp = models.BooleanField(blank=True, verbose_name="Esse telefone é Whatsapp?")
    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    def __str__(self):
        return "{} {}".format(self.phone, self.whatsapp)