# Generated by Django 4.2.15 on 2024-09-19 18:05

from django.db import migrations, models
import django_quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_ticketreport_ticket_ticketreport_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketreport',
            name='report',
            field=django_quill.fields.QuillField(unique=True, verbose_name='Reporte'),
        ),
        migrations.AlterField(
            model_name='ticketreport',
            name='title',
            field=models.CharField(max_length=50, verbose_name='Titulo'),
        ),
    ]
