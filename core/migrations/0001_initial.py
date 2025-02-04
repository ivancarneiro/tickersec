# Generated by Django 4.2.15 on 2024-09-19 10:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_quill.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('report', django_quill.fields.QuillField(verbose_name='Reporte')),
                ('createdBy', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_reports', to=settings.AUTH_USER_MODEL, verbose_name='Remitente')),
            ],
            options={
                'verbose_name_plural': 'Reportes',
                'ordering': ['-createdAt'],
            },
        ),
        migrations.CreateModel(
            name='TicketCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Categoria')),
                ('subcategory', models.CharField(max_length=50, unique=True, verbose_name='Subcategoria')),
                ('description', models.CharField(max_length=500, verbose_name='Descripcion')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True, verbose_name='Activo')),
                ('createdBy', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Categorias',
                'ordering': ['name', 'subcategory'],
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('INC', 'Incidente'), ('VUL', 'Vulnerabilidad'), ('EVE', 'Evento')], default='INC', max_length=50, verbose_name='Tipo')),
                ('title', models.CharField(max_length=50, verbose_name='Titulo')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('lastUpdate', models.DateTimeField(auto_now=True)),
                ('resolution', models.DurationField(blank=True, null=True, verbose_name='Resolucion')),
                ('severity', models.CharField(choices=[('CRITICA', 'Critica'), ('ALTA', 'Alta'), ('MEDIA', 'Media'), ('BAJA', 'Baja'), ('NULA', 'Nula')], default='NULA', max_length=7, verbose_name='Severidad')),
                ('impact', models.CharField(choices=[('CRITICO', 'Critica'), ('IMPORTANTE', 'Importante'), ('MODERADO', 'Moderado'), ('BAJO', 'Bajo'), ('NULO', 'Nulo')], default='NULO', max_length=10, verbose_name='Impacto')),
                ('status', models.CharField(choices=[('ABIERTO', 'Abierto'), ('TRAMITADO', 'Tramitado'), ('CERRADO', 'Cerrado')], default='ABIERTO', max_length=10, verbose_name='Estado')),
                ('resume', models.CharField(max_length=300, verbose_name='Resumen')),
                ('assignedTo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='assigned_tickets', to=settings.AUTH_USER_MODEL, verbose_name='Responsable')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='categorias', to='core.ticketcategory', verbose_name='Categoria')),
                ('createdBy', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_tickets', to=settings.AUTH_USER_MODEL, verbose_name='Remitente')),
                ('report', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='reportes', to='core.ticketreport', verbose_name='Reporte')),
            ],
            options={
                'verbose_name_plural': 'Tickets',
                'ordering': ['-pk'],
            },
        ),
    ]
