# Generated by Django 3.1.5 on 2021-02-03 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20210202_1853'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profileregistrationdata',
            name='address_complement',
        ),
        migrations.RemoveField(
            model_name='profileregistrationdata',
            name='address_number',
        ),
        migrations.RemoveField(
            model_name='profileregistrationdata',
            name='city',
        ),
        migrations.RemoveField(
            model_name='profileregistrationdata',
            name='neighborhood',
        ),
        migrations.RemoveField(
            model_name='profileregistrationdata',
            name='state',
        ),
        migrations.RemoveField(
            model_name='profileregistrationdata',
            name='street',
        ),
        migrations.RemoveField(
            model_name='profileregistrationdata',
            name='zip_code',
        ),
        migrations.AlterField(
            model_name='member',
            name='scholarity',
            field=models.CharField(choices=[(None, '---Escolaridade---'), ('ANF', 'Analfabeto'), ('EFI', 'Ensino fundamental incompleto'), ('EFC', 'Ensino fundamental completo'), ('EMI', 'Ensino médio incompleto'), ('EMC', 'Ensino médio completo'), ('ESC', 'Superior completo')], max_length=4),
        ),
        migrations.AlterField(
            model_name='member',
            name='treatment',
            field=models.CharField(choices=[(None, '---Tratamento---'), ('HM', 'Hemodiálise'), ('DP', 'Diálise Peritoneal'), ('TP', 'Transplantado')], max_length=3),
        ),
    ]
