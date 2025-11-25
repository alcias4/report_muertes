import streamlit as st
from page.descritive import descritve_info
from page.mapa_mundo import mapaMundo
from page.inferencia import pageInferenecia

from pandas import DataFrame

def menu_tabs(data: DataFrame):

    col_pais = data["Pais_Territorio"].unique()
    col_year = data["Año"].unique()
    col_enfermadad = data.columns[3::]

    res_pais: str =  st.selectbox("Ingresa el pais", col_pais)
    min_year, max_yar =  st.slider(
        "Selecciona el año",
        min_value=col_year.min(),
        max_value=col_year.max(),   # valor inicial
        value=(2006, 2019),
        step=1        # de 1 en 1
    )
    res_enfermedad: str =  st.selectbox("Ingresa el pais", col_enfermadad)

    data_filtrada =  data[(data["Pais_Territorio"] == res_pais) & (data["Año"] >= min_year ) & (data["Año"] <= max_yar)]

    data_filtrada_enfer = data_filtrada[["Pais_Territorio", "Año", res_enfermedad]]

    datos_fil_código = data[["Pais_Territorio", "Codigo", "Año", res_enfermedad]]


    nav_1, nav_2 , nav_3=  st.tabs(["Descriptiva", "Inferencia" ,"Mapa global"])

    with nav_1:
        descritve_info(data_fil=data_filtrada_enfer, enfermeda=res_enfermedad, pais=res_pais)

    with nav_2:
        pageInferenecia(df=data_filtrada, enferm=res_enfermedad)
    with nav_3:
        mapaMundo(dato=datos_fil_código, enfe=res_enfermedad, year=(min_year, max_yar))