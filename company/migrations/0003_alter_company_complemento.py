# Generated by Django 4.1.5 on 2023-02-18 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_rename_nome_company_nome_fantasia_alter_company_cnpj'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='complemento',
            field=models.CharField(blank=True, max_length=255, verbose_name='Complemento'),
        ),
    ]
