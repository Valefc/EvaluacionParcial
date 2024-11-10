import streamlit as st
import pandas as pd
import plotly_express as px
import os
import warnings
import seaborn as sns
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')

## Configuracion de la pagina
st.set_page_config(page_title='Productos Financieros', page_icon=":bar_chart", layout="wide")

st.title('Productos Financieros 💸')

st.markdown(
    """
        <style>
            .stMetric{
                
                background-color:floralwhite;
                border: 1px solidad #E0E0E0;
                padding:10px;
                border-radius: 10px;
                box-shadow:2px 2px 5px rgba(0,0,0,0.1)
                
            }
        </style>
    """
    ,unsafe_allow_html= True     
    )
st.markdown(
    """
        <style>        
            h1{
                background-color: limegreen;
                color: #FFFFFF;
                padding: 10px;
                border-radius: 10px;
                text-align:center;
                margin-bottom:20px;
            }
            h2,h3,h4,h5,h6{
                background-color: mediumorchid;
                color: white;
                padding: 10px;
                border-radius: 10px;
                text-align:center;
                margin-bottom:20px;
            }
            [data-testid="stFullScreenFrame"]{
                background-color: silver;
                border-top: 3px;
                border-bottom: 3px;
                border-left: 3px;
                border-radius: 15px 0px 0px 15px;
                padding: 5px;
                
            }
        </style>
    """
    ,unsafe_allow_html= True     
    )

df = pd.read_excel("df/economia_financiera.xlsx", header = 0)


#filtros
st.sidebar.header('Escoge tu opción')
edad = st.sidebar.multiselect('Seleccione el rango de edad', df['Rango_Edad'].unique())
filtered_df = df[df["Rango_Edad"].isin(edad)] if edad else df

genero = st.sidebar.multiselect('Seleccione el género', df['Genero'].unique())
filtered_df = filtered_df[filtered_df["Genero"].isin(genero)] if genero else filtered_df

distrito = st.sidebar.multiselect('Seleccione el distrito', df['Distrito'].unique())
filtered_df = filtered_df[filtered_df["Distrito"].isin(distrito)] if distrito else filtered_df

#Gráficos
col1,col2=st.columns((2))
with col1:
    st.subheader("Distribución de los Niveles Educativos entre los Géneros")
    fig = px.histogram(
        filtered_df,
        x='Nivel_educacion',
        color='Genero',
        title="Distribución de los Niveles Educativos entre los Géneros",
        labels={'Nivel_educacion': 'Nivel de Educación', 'count': 'Cantidad de Clientes'},
        barmode='group',
        text_auto=True)
    fig.update_layout(
        xaxis_title="Nivel de Educación",
        yaxis_title="Cantidad de Clientes",
        xaxis={'categoryorder': 'total descending'}    )
    st.plotly_chart(fig)
    
with col2:
    st.subheader("Responsables de las Decisiones Financieras entre los Rango de Edad")
    fig = px.histogram(
        filtered_df,
        x='responsable_familia',
        color='Rango_Edad',
        title="Responsables de las Decisiones Financieras entre los Rango de Edad",
        labels={'responsable_familia': 'responsable_familia', 'count': 'Cantidad de Clientes'},
        barmode='group',
        text_auto=True)
    fig.update_layout(
        xaxis_title="Responsable de Familia",
        yaxis_title="Cantidad de Clientes",
        xaxis={'categoryorder': 'total descending'}    )
    st.plotly_chart(fig)

col1,col2=st.columns((2))
with col1:
    st.subheader("Distribución de los Niveles Socioeconómicos")
    fig = px.pie(
        filtered_df,
        names='nivel_socieconomico',
        color='nivel_socieconomico',  
        title="Distribución de los Niveles Socioeconómicos",
        hole=0.3,  
        labels={'nivel_socieconomico': 'Nivel Socioeconómico'})
    st.plotly_chart(fig)
with col2:
    st.subheader("Porcentaje de Personas con Conocimientos Financieros")
    fig = px.pie(
        filtered_df,
        names='conceptos_ahorro_inversion',
        color='conceptos_ahorro_inversion',  
        title="Porcentaje de Personas con Conocimientos Financieros",
        hole=0.3,  
        labels={'conceptos_ahorro_inversion': 'Conociemientos Financieros'})
    st.plotly_chart(fig)
      
productos_financieros = ['tarjeta_debito', 'depositos_cuentas_ahorro', 'prestamos_personales', 'tarjeta_credito']

col1,col2=st.columns((2))
with col1:
    st.subheader("Productos Financieros por Nivel Socioeconómico")
    for producto in productos_financieros:
        filtered_df[producto] = filtered_df[producto].apply(lambda x: 1 if x == 'Si' else 0)
    productos_por_socioeconomico = filtered_df.groupby('nivel_socieconomico')[productos_financieros].mean() * 100
    fig = plt.figure()
    sns.heatmap(productos_por_socioeconomico, annot=True, cmap="YlGnBu", cbar_kws={'label': 'Porcentaje (%)'}, fmt='.2f')
    plt.title('Productos Financieros por Nivel Socioeconómico')
    plt.xlabel('Productos Financieros')
    plt.ylabel('Nivel Socioeconómico')
    st.pyplot(fig)
with col2:
    st.subheader("Situación Laboral por Nivel Socioeconómico")
    fig = px.bar(
    filtered_df,
    x='Situacion_Laboral',
    color='nivel_socieconomico',
    barmode='stack',
    title='Distribución de Nivel Socioeconómico por Situación Laboral',
    labels={'count': 'Cantidad de Personas', 'Situacion_Laboral': 'Situación Laboral'},
    text_auto=True)
    st.plotly_chart(fig)

col1,col2=st.columns((2))
with col1:
    st.subheader("Tendencia en el Uso de Productos Financieros por Rango de Edad")
    uso_productos = filtered_df.melt(
    id_vars=['Rango_Edad'],
    value_vars=productos_financieros,
    var_name='Producto_Financiero',
    value_name='Uso')

    uso_productos = uso_productos[uso_productos['Uso'] == 1]  # Filtrar solo los usos positivos

    fig = px.bar(
        uso_productos,
        x='Rango_Edad',
        color='Producto_Financiero',
        barmode='stack',
        title='Uso de Productos Financieros por Rango de Edad',
        labels={'Rango_Edad': 'Rango de Edad', 'count': 'Cantidad de Usos'},
        text_auto=True    )

    st.plotly_chart(fig)
        
with col2:
    st.subheader("Responsabilidad Financiera según el Nivel de Educación")
    fig = px.bar(
    filtered_df,
    x='plan_economico_mensual',
    color='Rango_Edad',
    barmode='group',
    title='Distribución del Plan Económico Mensual por Rango de Edad',
    labels={'Plan_Economico_Mensual': 'Plan Económico Mensual', 'count': 'Cantidad'})
    st.plotly_chart(fig)