import streamlit as st

from logic.get_datos import getDatos
from page.menu import menu_tabs


PATH_DB = "./db/datos.csv"

def main():
    st.title("Trabajo final")


    datos = getDatos(PATH_DB)
    
    if datos.empty:
        return st.error("Dataframe vacio error en buscqueda de la db")
    st.write("### Tabla  de datos de casos de muerte por enfermedad")
    st.write("- pagina: https://www.kaggle.com/datasets/iamsouravbanerjee/cause-of-deaths-around-the-world")
    st.write(datos)

    menu_tabs(data=datos)



if __name__ == "__main__":
    main()
