import streamlit as st
import pandas as pd 

import matplotlib as plt
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

import numpy as np
from PIL import Image
import seaborn as sns

import psycopg2
import streamlit as st

from sklearn.datasets import load_iris

#Cargar data iris y formar el data frame



@st.experimental_singleton
def init_connection():
    return psycopg2.connect(**st.secrets['postgres'])

conn=init_connection()

@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()
    
users=run_query('SELECT * FROM users')
courses=run_query('SELECT * FROM courses')
consimption=run_query('SELECT * FROM consumption')
labels=run_query('SELECT * FROM labels')
favorites=run_query('SELECT * FROM favorites')


df_users=pd.DataFrame(users,columns=['user_id','user_name','email','HiV_relation','age','identity','creation_date','password','role','log_in_bool','update_date'])
df_courses=pd.DataFrame(courses,columns=['course_id','course_title','course_description','course_url','course_format','course_length','creator','creation_date','update_day'])
df_consumption=pd.DataFrame(consimption,columns=['course_id','user_id','acces_date'])
df_labels=pd.DataFrame(labels,columns=['course_id','label'])
df_favorites=pd.DataFrame(favorites,columns=['course_title','course_id','user_id'])


menu = st.sidebar.selectbox("Selecciona la página", ['Inicio','Clase','Usuario'])

#Primera ventana en donde se vera info de la app y datos rapidos

if menu == 'Inicio':
    
    st.title('# Inicio')
    st.markdown('Aqui se explicara las funcionalidades de la aplicacion de manera breve para facilitar el uso a aquelllos administradores.')

    df_counts = df_consumption.groupby(["user_id"]).size().reset_index(name="watched_courses")
    df_courses = pd.merge(df_users,df_counts , on='user_id', how='outer')
    df_courses['watched_courses'].fillna(0, inplace=True)
        
    opciones = ['Todos'] + df_users['user_name'].unique().tolist()
    buscador = st.sidebar.selectbox('Selecciona un usuario', opciones)

   
    if buscador == 'Todos':
        # calcular totales y medias para todas las flores
        alumnos=len(df_users['user_id'])

        media_cursos=df_courses['watched_courses'].mean()

        # mostrar resultados

        st.title(f'Ejemplo para {buscador}')
        st.markdown('##')
        left_column, middle_column , right_column=st.columns(3)

        with left_column:
            st.subheader('Cantidad de alumnos')
            st.subheader(f':mortar_board:  {alumnos:}')
        with middle_column:
            st.subheader('Media de cursos llevados')
            st.subheader(f':books: {media_cursos:}')
        # with right_column:
        #     st.subheader('Media de ancho del petalo')
        #     st.subheader(f':left_right_arrow: {:}')

    else:

        df_filtrado = df_users[df_users['user_name'] == buscador]


        cursos_totales=df_filtrado['watched_courses']
        Genero=df_filtrado['identity']
        # media_ancho= round(df_filtrado['petal width (cm)'].mean(),2)


        st.title(f'Ejemplo para {buscador}')
        st.markdown('##')
        left_column, middle_column , right_column=st.columns(3)

        with left_column:
            st.subheader('Género')
            st.subheader(f':mortar_board: {Genero:}')
        with middle_column:
            st.subheader('Cursos vistos') 
            st.subheader(f':books: {cursos_totales:}')
        # with right_column:
        #     st.subheader('Media de ancho del petalo')
        #     st.subheader(f':left_right_arrow: {media_ancho:}')


elif menu == "Clase": 



    graficos = st.selectbox('Selecciona una flor', ['Usuarios', 'creacion de cuentas','cursos'])

    if graficos == 'Usuarios':

        st.title('Distribucion de flores')
        st.markdown('##')

        users_age_group=[]
        for i in df_users['age']:
            if 15< i <20:
                users_age_group.append(1)
            if 19< i <30:
                users_age_group.append(2)
            if 29< i <40:
                users_age_group.append(3)
            if 39< i <50:
                users_age_group.append(4)
            if 49< i <60:
                users_age_group.append(5)
            if 59< i <70:
                users_age_group.append(6)
            if 69< i <80:
                users_age_group.append(7)
            if 79< i <90:
                users_age_group.append(8)


        df_users['age_group']=users_age_group

        colors = sns.color_palette("Spectral").as_hex()
    
        cantidad_2 = df_users['age_group'].value_counts(normalize=True)
        cantidad_3 = df_users['HiV_relation'].value_counts(normalize=True)


        fig_1 = px.histogram(df_users, x='identity', nbins=15, title='Distribución Genero')
        st.plotly_chart(fig_1, use_container_width=True)

        fig_2 = px.pie(values = cantidad_2.values, names = ['17 - 19', '20 - 29', '30 - 39','40 - 49','50 - 59','60 - 69','70 - 79','80 - 90'], color_discrete_sequence=colors)
        st.plotly_chart(fig_2)

        fig_3 = px.pie(values = cantidad_3.values, names = ['Otros', 'Interesado', 'Afectado', 'Profesional', 'Familiar','Amigo'], color_discrete_sequence=colors)
        st.plotly_chart(fig_3)




    elif graficos == 'creacion de cuentas':
        
        df_users["creation_date"] = pd.to_datetime(df_users["creation_date"], format='%Y-%m-%d')
        df_users.sort_values(by='creation_date', inplace=True)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_users["creation_date"].unique(), y=df_users['creation_date'].value_counts(), mode='lines', name='Creacion de cuentas'))

        fig.update_layout(
            title="Creacion de cuentas",
            xaxis_title="Fecha",
            yaxis_title="cuentas"
        )


        st.plotly_chart(fig)

        st.markdown('Debajo de cada grafica irá una breve exlpicacion de la tabla  ')

    elif graficos == 'cursos':
        df_courses = pd.merge(df_courses,df_labels , on='course_id', how='left')
                
        fig_4 = px.histogram(df_courses, x='course_format', nbins=15, title='Distribución formato')
        st.plotly_chart(fig_4, use_container_width=True)


        cantidad_4= df_courses['label'].value_counts(normalize=True)

        fig_5 = px.pie(values = cantidad_4.values, names =['Charla', 'Campaña', 'Entrevista', 'Corto', 'Canción','Documental', 'Reportaje'])
        st.plotly_chart(fig_5)



        st.markdown('Debajo de cada grafica irá una breve exlpicacion de la tabla  ')
    
    


elif menu == "Usuario":

    usuarios = df_users['user_name'].unique()

    
    selected_user = st.selectbox('Selecciona un usuario', usuarios)

    # # Filtramos los datos del DataFrame para obtener solo las filas con la flor seleccionada
    # selected_data = df_users[df_users['user_name'] == selected_user]

    # # Creamos un gráfico de pastel para la distribución de las longitudes del pétalo
    # fig1 = px.histogram(selected_data, x='petal length (cm)', nbins=15, title=f'Distribución de longitudes de pétalo para {selected_user}')
    # st.plotly_chart(fig1, use_container_width=True)

    # # Creamos un gráfico de pastel para la distribución de las anchuras del pétalo
    # fig2 = px.histogram(selected_data, x='petal width (cm)', nbins=15, title=f'Distribución de anchuras de pétalo para {selected_user}')
    # st.plotly_chart(fig2, use_container_width=True