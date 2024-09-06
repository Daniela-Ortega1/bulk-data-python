import streamlit as st
import pandas as pd
#from course_db_helper import get_all_the_courses
from import_db_helper import insert_data_in_bulk

st.title("Upload data")

def extract_data_from_excel(excel_file, pqrs_file):
    """Extracts data information from the provided Excel file."""
    try:
        df = pd.read_excel(excel_file)
        df2 = pd.read_excel(pqrs_file)

    except Exception as e:
        st.write(f"Error reading the Excel file: {e}")
        return []

    df = df.rename(columns={
        'NombreCompleto': 'NombreCompleto',
        'Sexo': 'Sexo',
        'Edad': 'Edad',
        'Ciudad': 'Ciudad'
    })

    df['NombreCompleto'] = df['NombreCompleto'].astype(str)
    df['Sexo'] = df['Sexo'].astype(str)
    df['Edad'] = df['Edad'].astype(str)
    df['Ciudad'] = df['Ciudad'].astype(str)

    df2 = df2.rename(columns={
        'Tipo': 'Tipo',
        'ClienteFk': 'ClienteFk',
        'FechaCaso': 'FechaCaso',
        'Asunto': 'Asunto',
        'Estado': 'Estado',
        'FechaCierre': 'FechaCierre',
        'Urgencia': 'Urgencia',
    })

    df = df[['NombreCompleto', 'Sexo', 'Edad', 'Ciudad']]
    df2 = df2[['Tipo', 'ClienteFk', 'FechaCaso', 'Asunto','Estado','FechaCierre','Urgencia']]

    print(df)
    print(df2)

    df_joined = pd.concat([df,df2], axis=1)

    print('Todos juntos')
    print(df_joined)

    insert_data_in_bulk(df_joined, table_name='clientes', second_table_name="pqrs")
    
    st.write(df_joined)

# Obtener los cursos
# courses = get_all_the_courses()

# Crear un diccionario para mapear IDs de cursos a sus nombres
# course_dict = {course['id']: course['name'] for course in courses}
# course_ids = list(course_dict.keys())

# Crear el dropdown con los IDs como valor de selección y los nombres como valor de visualización
# selected_course_id = st.selectbox("Select a course", course_ids, format_func=lambda id: course_dict[id])

# Subir el archivo de Excel
uploaded_client_file = st.file_uploader("Client list", type=["xls", "xlsx"])
uploaded_pqrs_file = st.file_uploader("Pqrs list", type=["xls", "xlsx"])

# Botón para procesar la carga y mostrar los valores
if st.button("Import data"):
    if uploaded_client_file and uploaded_pqrs_file is not None:
        extract_data_from_excel(uploaded_client_file, uploaded_pqrs_file)
        st.write("Clients and pqrs have been imported successfully")
    else:
        st.write("You must upload both excels files to import the data")
    