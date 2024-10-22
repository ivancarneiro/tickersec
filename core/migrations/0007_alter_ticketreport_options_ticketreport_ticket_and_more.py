# Generated by Django 4.2.15 on 2024-09-22 01:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_ticketreport_report_alter_ticketreport_title'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticketreport',
            options={'ordering': ['createdAt'], 'verbose_name_plural': 'Reportes'},
        ),
        migrations.AddField(
            model_name='ticketreport',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reportes', to='core.ticket'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='severity',
            field=models.CharField(choices=[('CRITICA', 'Critica'), ('ALTA', 'Alta'), ('MEDIA', 'Media'), ('BAJA', 'Baja'), ('NULA', 'Nula')], default='NULA', max_length=7, verbose_name='Severidad'),
        ),
    ]
