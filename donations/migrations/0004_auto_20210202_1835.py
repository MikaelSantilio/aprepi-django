# Generated by Django 3.1.5 on 2021-02-02 21:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0003_auto_20210202_1015'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='creditcard',
            options={'verbose_name': 'Credit Card', 'verbose_name_plural': 'Credit Cards'},
        ),
        migrations.AlterModelOptions(
            name='recurringdonation',
            options={'verbose_name': 'Recurring Donation', 'verbose_name_plural': 'Recurring Donations'},
        ),
    ]