from unicodedata import category
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User


class TicketCategory(models.Model):
    
    category = models.CharField(verbose_name="Categoria", max_length=50, blank=False)
    subcategory = models.CharField(verbose_name="Subcategoria", max_length=50, blank=False)
    desciption = models.CharField(verbose_name="Descipción", max_length=500, blank=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    createdBy = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False)
    
    def __str__(self):
        return f"{self.category} - {self.subcategory}"
    
    class Meta:
        ordering = ["pk", "category", "subcategory"]
        verbose_name_plural = "Categorias"
        

TICKET_TYPES = {
    "Incidente": {
        "INC": "Incidente",
    },
    "Vulnerabilidad": {
        "VUL": "Vulnerabilidad",
        "AVI": "Zero Day",
    },
    "Evento": {
        "EVE": "Evento",
    },
}

class Ticket(models.Model):
    
    type = models.CharField(verbose_name="Tipo", max_length=3, choices=TICKET_TYPES, default=INCIDENTE)
    category = models.ForeignKey(TicketCategory, verbose_name="Categoría", related_name="categorias", on_delete=models.PROTECT)