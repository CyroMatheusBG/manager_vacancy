# Generated by Django 4.1.4 on 2023-02-27 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_company_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='email',
            field=models.EmailField(max_length=255, verbose_name='E-mail para contato'),
        ),
    ]