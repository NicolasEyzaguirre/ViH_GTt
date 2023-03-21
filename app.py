import streamlit as st
from streamlit_lottie import st_lottie
import pandas as pd 
import requests
import json

import matplotlib as plt
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

import numpy as np
from PIL import Image
import seaborn as sns

import psycopg2
import pickle



with open('Modelo/rfmodel', 'rb') as archivo_entrada:
    loaded_model = pickle.load(archivo_entrada)

def load_lottieurl(url:str):
    r=requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()

def load_lottiefile(filepath:str):
    with open(filepath, 'r') as f:
        return json.load(f)


imagen= Image.open('images/minilogo.png')

lottie_hello=load_lottiefile('images/86199-business-analytics.json')
lottie_he=load_lottiefile('images/57946-profile-user-card.json')
lottie_h=load_lottiefile('images/86878-creation-de-site-webdesign.json')


@st.experimental_singleton
def init_connection():
    # st.write("dbname:", st.secrets["dbname"])
    # st.write("password:", st.secrets["password"])
    # st.write("host:", st.secrets['host'])
    # st.write("user:", st.secrets['user'])
    return psycopg2.connect(dbhost = st.secrets['host'],
                            user = st.secrets['user'],
                            dbname = st.secrets['dbname'],
                            port = 5432,
                            password = st.secrets['password'])

# psycopg2.connect(**st.secrets['postgres'])

# @st.experimental_singleton
# def init_connection():
#     return psycopg2.connect(**st.secrets['postgres'])



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
df_consumption=pd.DataFrame(consimption,columns=['course_id','user_id','acces_date','completed'])
df_labels=pd.DataFrame(labels,columns=['course_id','label'])
df_favorites=pd.DataFrame(favorites,columns=['course_title','course_id','user_id'])

imagen_sidebar = st.sidebar.image(imagen, use_column_width=True)
menu = st.sidebar.selectbox("Selecciona la página", ['Inicio','Clase','Usuario'])



if menu == 'Inicio':
    left_column,right_column=st.columns(2)
    with left_column:
        st_lottie(lottie_hello,key='hello')


    with right_column:
        st.write(" ") 
        st.write(" ") 
        st.title('XOX* Estadisticas')
        st.markdown('#')
        st.markdown('Tiene la libertad de ver las estidisticas tanto individuales como grupales de los usuarios logueados a la página')

    df_counts = df_consumption.groupby(["user_id"]).size().reset_index(name="watched_courses")
    df_courses = pd.merge(df_users,df_counts , on='user_id', how='outer')
    df_courses['watched_courses'].fillna(0, inplace=True)
        
    opciones = ['Todos'] + df_users['user_name'].unique().tolist()
    buscador = st.sidebar.selectbox('Selecciona un usuario', opciones)

   
    if buscador == 'Todos':
        
        alumnos=len(df_users['user_id'])

        media_cursos=df_courses['watched_courses'].mean().__round__(2)

        # mostrar resultados

        st.title(f'Clase {buscador}')
        st.markdown('####')
        left_column,right_column=st.columns(2)

        with left_column:
            st.subheader('Cantidad de alumnos')
            st.subheader(f':mortar_board:  {alumnos:}')
        with right_column:
            st.subheader('Media de cursos llevados')
            st.subheader(f':books: {media_cursos:}')


    else:

        df_filtrado = df_courses[df_courses['user_name'] == buscador]


        cursos_totales=int(df_filtrado['watched_courses'])
        Genero=df_filtrado['identity'].iloc[0]


        st.title(f'Estudiante {buscador}')
        st.markdown('####')
        left_column, right_column=st.columns(2)

        with left_column:
            st.subheader('Género')
            st.subheader(f':mortar_board: {Genero:}')
        with right_column:
            st.subheader('Cursos vistos') 
            st.subheader(f':books: {cursos_totales:}')



elif menu == "Clase": 



    graficos = st.selectbox('Seleccione un área que desee ver', ['Usuarios', 'Creación de cuentas','Cursos'])

    if graficos == 'Usuarios':

        st.title('Distribución de usuarios ')
        st.markdown('####')

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


        # cantidad_2 = df_users['age_group'].value_counts(normalize=True)
        # cantidad_3 = df_users['HiV_relation'].value_counts(normalize=True)

        # fig_2 = px.pie(values=cantidad_2.values, names=['17 - 19', '20 - 29', '30 - 39','40 - 49','50 - 59','60 - 69','70 - 79','80 - 90'], color_discrete_sequence=px.colors.qualitative.Pastel)
        # fig_2.update_layout(title={'text': 'Edades'})
        # fig_3 = px.pie(values=cantidad_3.values, names=['Otros', 'Interesado', 'Afectado', 'Profesional', 'Familiar', 'Amigo'], color_discrete_sequence=px.colors.qualitative.Pastel)
        # fig_3.update_layout(title={'text': 'Conexión con el ViH'})
        # fig_1 = px.histogram(df_users, x='identity', nbins=15, title='Distribución Genero', color_discrete_sequence=px.colors.qualitative.Pastel)

        # # Agregar interactividad entre gráficas
        # fig_1.update_traces(selectedpoints=[0], selector=dict(type='histogram'))
        # fig_2.update_traces(hoverinfo='label+percent+name', textinfo='none')
        # fig_3.update_traces(hoverinfo='label+percent+name', textinfo='none')


        # # Agregar la interactividad
        # fig_1.for_each_trace(lambda trace: trace.update(visible='legendonly') if 'marker' in trace else ())
        # fig_2.for_each_trace(lambda trace: trace.update(visible='legendonly') if 'marker' in trace else ())
        # fig_3.for_each_trace(lambda trace: trace.update(visible='legendonly') if 'marker' in trace else ())

        # fig_1.for_each_trace(lambda trace: trace.update(visible=True) if trace.name == 'M' else ())
        # fig_2.for_each_trace(lambda trace: trace.update(visible=True) if trace.name == 'M' else ())
        # fig_3.for_each_trace(lambda trace: trace.update(visible=True) if trace.name == 'M' else ())

        # col1, col2 = st.columns(2)

        
        # with col1:
        #     st.plotly_chart(fig_2,use_container_width=True)
        # with col1:
        #     st.plotly_chart(fig_3,use_container_width=True)
        # # Mostrar la figura general en Streamlit
        # st.plotly_chart(fig_1)



    
        cantidad_2 = df_users['age_group'].value_counts(normalize=True)
        cantidad_3 = df_users['HiV_relation'].value_counts(normalize=True)

        col1, col2 = st.columns(2)

        with col1:
            fig_2 = px.pie(values = cantidad_2.values, names = ['17 - 19', '20 - 29', '30 - 39','40 - 49','50 - 59','60 - 69','70 - 79','80 - 90'], color_discrete_sequence=colors)
            fig_2.update_layout(title={'text': 'Edades '})
            st.plotly_chart(fig_2,use_container_width=True)

        with col2:
            fig_3 = px.pie(values = cantidad_3.values, names = ['Otros', 'Interesado', 'Afectado', 'Profesional', 'Familiar','Amigo'], color_discrete_sequence=colors)
            fig_3.update_layout(title={'text': 'Conexión con el ViH '})
            st.plotly_chart(fig_3,use_container_width=True)

        fig_1 = px.histogram(df_users, x='identity', nbins=15, title='Distribución Genero',color_discrete_sequence=colors)
        st.plotly_chart(fig_1, use_container_width=True)



    elif graficos == 'Creación de cuentas':
        left_column,right_column=st.columns(2)
        with left_column:
            st.title('Creación de cuentas')
            st.markdown('####')

        
        with right_column:
            st_lottie(lottie_h,key='h')


        
        df_users["creation_date"] = pd.to_datetime(df_users["creation_date"], format='%Y-%m-%d')
        df_users.sort_values(by='creation_date', inplace=True)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_users["creation_date"].unique(), y=df_users['creation_date'].value_counts(), mode='lines', name='Creacion de cuentas'))

        fig.update_layout(
            xaxis_title="Fecha",
            yaxis_title="cuentas"
        )
        st.plotly_chart(fig)


    elif graficos == 'Cursos':
        st.title('Cursos')
        st.markdown('####')

        colors = sns.color_palette("Spectral").as_hex()
        df_courses = pd.merge(df_courses,df_labels , on='course_id', how='left')
                
        fig_4 = px.histogram(df_courses, x='course_format', nbins=15, title='Distribución formato', color_discrete_sequence=colors)
        st.plotly_chart(fig_4, use_container_width=True)


        cantidad_4= df_courses['label'].value_counts(normalize=True)

        fig_5 = px.pie(values = cantidad_4.values, names =['Charla', 'Campaña', 'Entrevista', 'Corto', 'Canción','Documental', 'Reportaje'], color_discrete_sequence=colors)
        fig_5.update_layout(title={'text': 'Tipos de Cursos'})
        st.plotly_chart(fig_5)



        st.markdown('Debajo de cada grafica irá una breve exlpicacion de la tabla  ')
    
    


elif menu == "Usuario":
    

    df_favorites = pd.merge(df_favorites,df_users[['user_id','user_name']], on='user_id', how='left')

    usuarios = df_users['user_name'].unique()
  
    selected_user = st.sidebar.selectbox('Selecciona un usuario', usuarios)

    left_column,right_column=st.columns(2)
    with left_column:
        st_lottie(lottie_he,key='he')


    with right_column:
        st.write(" ") 
        st.write(" ") 
        st.title(f'Alumno {selected_user}')
        st.markdown('##')


        
        df_consumption['user_id'] = df_consumption['user_id'] + 1
        df_consumption['course_id'] = df_consumption['course_id'] + 1
        df_consumption = pd.merge(df_consumption,df_users[['user_id','user_name']], on='user_id', how='left')

        df_counts = df_consumption.groupby(["user_id"]).size().reset_index(name="Cursos apuntados")
        df_counts_2=df_consumption[df_consumption['completed']].groupby('user_id').size().reset_index(name="Insignias")

        df_courses = pd.merge(df_users,df_counts , on='user_id', how='outer')
        df_courses['Cursos apuntados'].fillna(0, inplace=True)
        df_courses = pd.merge(df_courses,df_counts_2 , on='user_id', how='outer')
        df_courses['Insignias'].fillna(0, inplace=True)

        mappingrel = {
            'Otros': 1,
            'Afectado': 2,
            'Profesional': 3,
            'Familiar': 4,
            'Amigo': 5,
            'Interesado': 6
        }

        df_courses['Relación VIH'] = df_courses['HiV_relation'].replace(mappingrel)
        df_courses = pd.get_dummies(df_courses, columns=['identity'])

        df_courses = df_courses.drop(['user_id','email','creation_date','password','role','log_in_bool','update_date','HiV_relation'], axis=1)

        df_courses.set_index('user_name',inplace=True)

        df_courses = df_courses.reindex(columns=['Relación VIH', 'age', 'Cursos apuntados','Insignias','identity_Hombre','identity_Mujer','identity_Otros'])

        egresion=loaded_model.predict(df_courses)

        df_courses['egresion']=egresion
        Egresion=df_courses.loc[selected_user,'egresion']
        if Egresion==2:
            st.subheader(f'{selected_user} abandonara el curso')
        elif Egresion==4 or Egresion==3:
            st.subheader(f'{selected_user} no abandonara el curso pero tiene cursos pendientes')
        elif Egresion==5:
            st.subheader(f'{selected_user} no abandonara el curso pero no ha iniciado ningun curso')
        else:
            st.subheader(f'{selected_user} no abandonara el curso')



    df_consumption_user=df_consumption[df_consumption['user_name']==selected_user]
    

    datos = [{'x': ['Cursos'], 'y':[df_consumption_user['course_id'].count()] , 'type': 'bar', 'name': 'Iniciados', 'marker': {'color': '#ff6700', 'opacity': 0.5}},
             {'x':['Cursos'] , 'y':[df_consumption_user[df_consumption_user['completed']==True]['completed'].count()], 'type': 'bar', 'name': 'Terminados', 'marker': {'color': '#f7fd04'}}]

    layout = go.Layout(barmode='overlay')

    fig = go.Figure(data=datos, layout=layout)

    
    st.plotly_chart(fig)
