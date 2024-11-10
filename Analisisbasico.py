import streamlit as st
import pandas as pd
import plotly_express as px
import numpy as np
from scipy.stats import chi2_contingency

st.title('Análisis de Datos 🔎')

uploaded_file = st.file_uploader('Subir archivo Excel (.xlsx)', type='xlsx')

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.subheader('Primeras Filas del Dataset')
    st.dataframe(df.head())
    
    st.subheader('Tablas de frecuencias 📊')
    for i, col in enumerate (df.columns[1:]):
        st.write(f'Tabla de frecuencias para la columna: {col}')
        frecuencia = df[col].value_counts().reset_index()
        frecuencia.columns = [col, 'Frecuencia']
        st.dataframe(frecuencia)
        
        # Alternar gráficos de barras y sectores
        if i % 2 == 0:
            st.subheader(f'Diagrama de barras para la columna: {col}')
            fig = px.bar(frecuencia, x=col, y='Frecuencia', title=f'Diagrama de barras de {col}', text_auto=True,color=col)
        else:
            st.subheader(f'Diagrama de sectores para la columna: {col}')
            fig = px.pie(frecuencia, names=col, values='Frecuencia', title=f'Diagrama de sectores de {col}',color=col)
        
        st.plotly_chart(fig)
    
    st.subheader('Nombres de las Columnas')
    st.write(df.columns)
    
    st.subheader('Tipos de Datos')
    st.write(df.dtypes)
    
    st.subheader('Valores Nulos en el DataSet')
    st.write(df.isnull().sum())
    
    st.subheader('Filas Duplicadas')
    st.write(df.duplicated().sum())
    
    # Función para calcular la matriz de correlación de Cramér's V (omitiendo la primera columna)
    def cramers_v_matrix(df):
        cols = df.columns[1:]  # Omitir la primera columna
        corr_matrix = pd.DataFrame(index=cols, columns=cols)

        for col1 in cols:
            for col2 in cols:
                contingency_table = pd.crosstab(df[col1], df[col2])
                chi2, _, _, _ = chi2_contingency(contingency_table)
                n = contingency_table.sum().sum()
                phi2 = chi2 / n
                r, k = contingency_table.shape
                corr_matrix.loc[col1, col2] = np.sqrt(phi2 / min(k - 1, r - 1))

        return corr_matrix.astype(float)
# Generar y mostrar la matriz de correlación de Cramér's V (omitiendo la primera columna)
    st.subheader('Matriz de Correlación de Cramér\'s V 🔗')
    correlation_matrix = cramers_v_matrix(df)
    st.dataframe(correlation_matrix)
    
    # Visualización de la matriz de correlación como un heatmap
    st.subheader('Heatmap de la Matriz de Correlación')
    fig = px.imshow(correlation_matrix, text_auto=True, title='Matriz de Correlación de Cramér\'s V')
    st.plotly_chart(fig)
    
else:
    st.write('Por favor, sube un archivo Excel')
    