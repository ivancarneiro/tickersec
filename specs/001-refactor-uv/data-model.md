# Data Model: refactor-uv

Esta refactorización está centrada exclusivamente en la infraestructura de dependencias y entornos del proyecto mediante `uv`. 

## 1. Cambios en Base de Datos
- **Impacto**: Ninguno. No hay modificaciones a los modelos relacionales de Django.
- **Esquema de Base de Datos**: Se mantiene idéntico al documentado en la wiki (SQLite en desarrollo local y PostgreSQL para producción).

## 2. Modelos Existentes (sin cambios)
- **Ticket**: Entidad principal de incidentes, vulnerabilidades y eventos.
- **TicketCategory**: Categorización jerárquica.
- **TicketReport**: Reportes ricos (django-quill-editor) asociados a cada ticket.
