import pandas as pd
import plotly.express as px
from core.models import Ticket

# Definir los colores para cada severidad
colores_severidad = {
    'CRITICA': 'red',
    'ALTA': 'orange',
    'MEDIA': 'yellow',
    'BAJA': '#33ff00',
    'NULA': 'gray'
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
    fig = px.bar(df_grouped, x='month', y='count', color='severity',
                 color_discrete_map=colores_severidad,
                 labels={'month': 'Mes', 'count': 'Cantidad de Tickets', 'severity': 'Severidad'},
                 title='Cantidad de Tickets por Severidad Distribuidos en los 12 Meses del Año')

    # Establecer el modo de barras a 'group'
    fig.update_layout(barmode='group')

    # Configurar el autoscale
    fig.update_xaxes(autorange=True)
    fig.update_yaxes(autorange=True)

    # Convertir el gráfico a HTML
    graph_html = fig.to_html(full_html=False)
    return graph_html

def pieTicketSeverities():
    # Obtener los datos
    tickets = Ticket.objects.all()
    data = [{
        'severity': ticket.severity
    } for ticket in tickets]
    df = pd.DataFrame(data)
    df_grouped = df.groupby(['severity']).size().reset_index(name='count')

    # Crear el gráfico de torta
    fig = px.pie(df_grouped, values='count', names='severity',
                 color_discrete_map=colores_severidad,
                 labels={'severity': 'Severidad', 'count': 'Cantidad de Tickets'},
                 title='Distribución de Tickets por Severidad')

    # Convertir el gráfico a HTML
    graph_html = fig.to_html(full_html=False)
    return graph_html


def pieTicketCategories():
    # Obtener los datos
    tickets = Ticket.objects.all()
    data = [{
        'category': ticket.category.name
    } for ticket in tickets]
    df = pd.DataFrame(data)
    df_grouped = df.groupby(['category']).size().reset_index(name='count').nlargest(10, 'count')

    # Crear el gráfico de torta
    fig = px.pie(df_grouped, values='count', names='category',
                 labels={'category': 'Categoría', 'count': 'Cantidad de Tickets'},
                 title='Distribución de Tickets por Categoría (Top 10)')

    # Convertir el gráfico a HTML
    graph_html = fig.to_html(full_html=False)
    return graph_html