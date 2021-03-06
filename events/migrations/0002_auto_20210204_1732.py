# Generated by Django 3.1.5 on 2021-02-04 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20210203_1643'),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='date_event',
        ),
        migrations.AddField(
            model_name='event',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='start_date',
            field=models.DateField(default='2021-01-01'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='volunteers',
            field=models.ManyToManyField(related_name='event_set', to='users.Voluntary', verbose_name='volunteers'),
        ),
    ]
