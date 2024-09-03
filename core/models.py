import os

from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime


class TicketCategory(models.Model):
    
    category = models.CharField(verbose_name="Categoria", max_length=50, blank=False)
    subcategory = models.CharField(verbose_name="Subcategoria", max_length=50, blank=False)
    description = models.CharField(verbose_name="Descipcion", max_length=500, blank=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    createdBy = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False)
    active = models.BooleanField(verbose_name="Activo", blank=False, default=True)
    
    def __str__(self):
        return f"{self.category} - {self.subcategory}"
    
    class Meta:
        ordering = ["pk", "category", "subcategory"]
        verbose_name_plural = "Categorias"
        

def ticket_capture_upload_to(instance, filename):
    # Obtener la fecha actual
    now = datetime.now()
    # Construir la ruta del archivo
    path = f"ticket_captures/{now.year}/{now.month}/{now.day}/{instance.pk}"
    return os.path.join(path, filename)

class Ticket(models.Model):
    
    class TicketType(models.TextChoices):
        INCIDENTE       = "INC", "Incidente"
        VULNERABILIDAD  = "VUL", "Vulnerabilidad"
        EVENTO          = "EVE", "Evento"

    class TicketStatus(models.TextChoices):
        ABIERTO     = "ABIERTO", "Abierto"
        TRAMITADO   =  "TRAMITADO", "Tramitado"
        CERRADO     = "CERRADO", "Cerrado"

    class Severity(models.TextChoices):
        CRITICA = "CRITICA"
        ALTA    = "ALTA"
        MEDIA   = "MEDIA"
        BAJA    = "BAJA"
        NULA    = "NULA"
    
    class Impact(models.TextChoices):
        CRITICA     = "CRITICO"
        IMPORTANTE  = "IMPORTANTE"
        MODERADO    = "MODERADO"
        BAJO        = "BAJO"
        NULO        = "NULO"
    
    type = models.CharField(verbose_name="Tipo", max_length=50, choices=TicketType.choices, default=TicketType.INCIDENTE)
    category = models.ForeignKey(TicketCategory, verbose_name="Categoria", related_name="categorias", on_delete=models.PROTECT)
    title = models.CharField(verbose_name="Titulo", max_length=50, blank=False)
    createdAt = models.DateTimeField(auto_now=True)
    lastUpdate = models.DateTimeField(auto_now_add=True)
    resolution = models.DurationField(verbose_name="Resolucion", null=True, blank=True)
    severity = models.CharField(verbose_name="Severidad", max_length=7, blank=False, default=Severity.NULA.name)
    impact = models.CharField(verbose_name="Impacto", max_length=10, blank=False, default=Impact.NULO.name)
    status = models.CharField(verbose_name="Estado", max_length=9, blank=False, default=TicketStatus.ABIERTO.name)
    createdBy = models.ForeignKey(User, verbose_name="Remitente", related_name="created_tickets", on_delete=models.PROTECT, null=False, blank=False)
    assignedTo = models.ForeignKey(User, verbose_name="Responsable", related_name="assigned_tickets", on_delete=models.PROTECT, null=False, blank=False)
    resume = models.CharField(verbose_name="Resumen", max_length=300, blank=False)
    captures = models.ImageField(verbose_name="Capturas", upload_to=ticket_capture_upload_to)
    
    def save(self, *args, **kwargs):
        if self.status == "CERRADO" and self.resolution is None:
            self.resolution = (timezone.now() - self.createdAt)
        super().save(*args, **kwargs)
    
    def resolution_display(self):
        if self.resolution:
            total_seconds = int(self.resolution.total_seconds())
            days = total_seconds // 86400
            hours = (total_seconds % 86400) // 3600
            minutes = (total_seconds % 3600) // 60
            return f"{days}d {hours}h {minutes}min"
        return "No resuelto"
    
    def get_absolute_url(self):
        return reverse("ticket:detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return  """{self.type}{self.pk} | {self.title} | Categoría: {self.category}\n
                Severidad: {self.severity} | Impacto. {self.impact}\n
                Creado: {self.createdAt} - Actualizado: {self.updatedAt} - Resolución: {resolution_display}\n
                Estado: {self.status}\n | Registrado por: {self.createdBy} | Responsable: {self.assignedTo}"""

    class Meta:
        ordering = ["pk"].reverse()
        verbose_name_plural = 'Tickets'
