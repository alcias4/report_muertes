import streamlit as st
from pandas import DataFrame
import plotly.express as px
import pandas as pd
from plotly.graph_objects import Figure # type: ignore

def descritve_info(data_fil:DataFrame, enfermeda: str, pais: str):


    
    fig: Figure =  px.line(data_fil, x="Año", y=enfermeda, title=f"Cantidad de muertos por {enfermeda} en {pais}") # type: ignore


    st.plotly_chart(fig,use_container_width=True) # type: ignore


    promedio_muertos =  round(data_fil[enfermeda].mean(), 2)
    max_muertos =  round(data_fil[enfermeda].max(), 2)
    min_muertos =  round(data_fil[enfermeda].min(), 2)
    desviciona_muerto = round(data_fil[enfermeda].std(),2)
    varianza_muerto = round((data_fil[enfermeda].var()), 2) # type: ignore

    tabla_descritiva = pd.DataFrame({
        "promedio muertos": promedio_muertos,
        "maximo de muertos": max_muertos,
        "mínimo de muertos": min_muertos,
        "Desviación estandar": desviciona_muerto,
        "Varianza": varianza_muerto
    }, index=["Estadísticas"])

    st.write(f"### Tabla descriptiva:")
    st.write(tabla_descritiva)



