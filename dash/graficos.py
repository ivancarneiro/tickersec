import pandas as pd
from .models import Ticket
from django_echarts.entities import EChart, Bar, Pie

# Definir los colores para cada severidad
colores_severidad = {
    'CRITICA': '#FF0000',  # Red
    'ALTA': '#FFA500',     # Orange
    'MEDIA': '#FFFF00',    # Yellow
    'BAJA': '#33FF00',     # Green
    'NULA': '#808080'      # Gray
}

# Función para convertir números de mes a nombres abreviados
def obtener_nombre_mes_abreviado(numero_mes):
    meses = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return meses[numero_mes - 1]

def barTicketSeveritiesXmonth():
    # Obtener los datos
    tickets = Ticket.objects.all()
    data = [{
        'month': obtener_nombre_mes_abreviado(ticket.createdAt.month),
        'severity': ticket.severity
    } for ticket in tickets]
    df = pd.DataFrame(data)
    df_grouped = df.groupby(['month', 'severity']).size().reset_index(name='count')

    # Crear el gráfico de barras
    echart = EChart('Cantidad de Tickets por Severidad Distribuidos en los 12 Meses del Año')
    bar = Bar('Tickets por Severidad')
    for severity, color in colores_severidad.items():
        datos_severidad = df_grouped[df_grouped['severity'] == severity]
        bar.add(severity, datos_severidad['month'].tolist(), datos_severidad['count'].tolist(), itemstyle_opts={'color': color})
    
    echart.use(bar)
    return echart

def pieTicketSeverities():
    # Obtener los datos
    tickets = Ticket.objects.all()
    data = [{
        'severity': ticket.severity
    } for ticket in tickets]
    df = pd.DataFrame(data)
    df_grouped = df.groupby(['severity']).size().reset_index(name='count')

    # Crear el gráfico de torta
    echart = EChart('Distribución de Tickets por Severidad')
    pie = Pie('Tickets por Severidad')
    pie.add('', df_grouped['severity'].tolist(), df_grouped['count'].tolist(), itemstyle_opts={
        'color': [colores_severidad[severity] for severity in df_grouped['severity']]
    })
    
    echart.use(pie)
    return echart

def pieTicketCategories():
    # Obtener los datos
    tickets = Ticket.objects.all()
    data = [{
        'category': ticket.category.name
    } for ticket in tickets]
    df = pd.DataFrame(data)
    df_grouped = df.groupby(['category']).size().reset_index(name='count').nlargest(10, 'count')

    # Crear el gráfico de torta
    echart = EChart('Distribución de Tickets por Categoría (Top 10)')
    pie = Pie('Tickets por Categoría')
    pie.add('', df_grouped['category'].tolist(), df_grouped['count'].tolist())
    
    echart.use(pie)
    return echart