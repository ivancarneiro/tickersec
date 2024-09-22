from email.policy import default
from typing import Self
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django_quill.fields import QuillField
from django.utils import timezone
from core.utils import TicketType, TicketStatus, Severity, Impact


class TicketCategory(models.Model):
    
    name = models.CharField(verbose_name='Categoria', max_length=50, blank=False)
    subcategory = models.CharField(verbose_name='Subcategoria', max_length=50, unique=True, blank=False)
    description = models.CharField(verbose_name='Descripcion', max_length=500, blank=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    createdBy = models.ForeignKey(User, on_delete=models.PROTECT, null=False)
    active = models.BooleanField(verbose_name='Activo', null=False, default=True)
    
    def __str__(self):
        return f'{self.name} - {self.subcategory}'
    
    class Meta:
        ordering = ['name', 'subcategory']
        verbose_name_plural = 'Categorias'
        


class TicketReport(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    createdBy = models.ForeignKey(User, verbose_name='Remitente', related_name='created_reports', on_delete=models.PROTECT, blank=False)
    title = models.CharField(verbose_name='Titulo', max_length=50, blank=False)
    ticket = models.ForeignKey('Ticket', related_name='reportes', on_delete=models.PROTECT)
    report = QuillField(verbose_name='Reporte', blank=False, unique=True)
    
    def get_absolute_url(self):
        return reverse('core:detail-report', kwargs={'pk': self.pk})
    
    def __str__(self):
        return  f'Reporte {self.pk} - {self.title}'

    class Meta:
        ordering = ['createdAt']
        verbose_name_plural = 'Reportes'

class Ticket(models.Model):
    
    type = models.CharField(verbose_name='Tipo', max_length=50, choices=TicketType.choices, default=TicketType.INCIDENTE)
    category = models.ForeignKey(TicketCategory, verbose_name='Categoria', related_name='categorias', on_delete=models.PROTECT)
    title = models.CharField(verbose_name='Titulo', max_length=50, blank=False)
    createdAt = models.DateTimeField(auto_now_add=True) # auto_now_add: actualiza el valor con la hora y la fecha de creación del registro.
    lastUpdate = models.DateTimeField(auto_now=True) # auto_now: actualiza el valor del campo a la hora y fecha actuales cada vez que se llama a Model.save().
    resolution = models.DurationField(verbose_name='Resolucion', blank=True, null=True)
    severity = models.CharField(verbose_name='Severidad', choices=Severity.choices, default=Severity.NULA.name, max_length=7)
    impact = models.CharField(verbose_name='Impacto', choices=Impact.choices, default=Impact.NULO.name, max_length=10)
    status = models.CharField(verbose_name='Estado', choices=TicketStatus.choices, default=TicketStatus.ABIERTO.name, max_length=10)
    createdBy = models.ForeignKey(User, verbose_name='Remitente', related_name='created_tickets', on_delete=models.PROTECT, blank=False)
    assignedTo = models.ForeignKey(User, verbose_name='Responsable', related_name='assigned_tickets', on_delete=models.PROTECT, blank=False)
    resume = models.CharField(verbose_name='Resumen', max_length=300, blank=False)
    report = models.ForeignKey(TicketReport, verbose_name='Reporte', related_name='reportes', on_delete=models.PROTECT, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.status == 'CERRADO' and self.resolution is None:
            self.resolution = (timezone.now() - self.createdAt)
        super().save(*args, **kwargs)
    
    def resolution_display(self):
        '''Devuelve el tiempo de resolución de un ticket en formato entendible por humanos, Ej.: 2d 8h 3min'''
        if not self.resolution:
            return 'Sin resolver'
        else:
            total_seconds = int(self.resolution.total_seconds())
            days = total_seconds // 86400
            hours = (total_seconds % 86400) // 3600
            minutes = (total_seconds % 3600) // 60
            return f'{days}d {hours}h {minutes}min'
    
    def update_ticketStatus(self):
        '''Actualiza el estado del ticket al crear el primer reporte.'''
        if self.status == TicketStatus.ABIERTO and self.reportes.count() > 0:
            self.status = TicketStatus.TRAMITADO
        self.save()

    def get_absolute_url(self):
        return reverse('core:detail-ticket', kwargs={'pk': self.pk})
    
    def __str__(self):
        return  f'{self.type}{self.pk} - {self.title}'

    class Meta:
        ordering = ['-pk']
        verbose_name_plural = 'Tickets'
