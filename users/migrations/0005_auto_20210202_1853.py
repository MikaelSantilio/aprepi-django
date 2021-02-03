# Generated by Django 3.1.5 on 2021-02-02 21:53

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210202_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='member', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profileregistrationdata',
            name='phone_number',
            field=models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="O número precisa estar nos formatos '99 99999-9999' ou '99 9999-9999'.", regex='(\\(?\\d{2}\\)?\\s)?(\\d{4,5}\\-\\d{4})')]),
        ),
        migrations.AlterField(
            model_name='profileregistrationdata',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='voluntary',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='voluntary', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]