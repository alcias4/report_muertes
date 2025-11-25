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


    nav_1, nav_2 , nav_3, nav_4=  st.tabs(["Descriptiva", "Inferencia" ,"Mapa global", "Herramintas"])


    estado = False




    with nav_1:
        descritve_info(data_fil=data_filtrada_enfer, enfermeda=res_enfermedad, pais=res_pais)

    with nav_2:
        pageInferenecia(df=data_filtrada, enferm=res_enfermedad)
    with nav_3:
        mapaMundo(dato=datos_fil_código, enfe=res_enfermedad, year=(min_year, max_yar))
    with nav_4:
        seccion_herramientas_usadas()




def seccion_herramientas_usadas():
    st.header("🛠️ Herramientas utilizadas")

    def card(title: str, emoji: str, subtitle: str):
        st.markdown(
            f"""
            <div style="
                border-radius: 16px;
                padding: 18px;
                border: 1px solid #44444455;
                text-align: center;
                margin-bottom: 16px;
                background: #11111171;
            ">
                <div style="font-size: 32px;">{emoji}</div>
                <div style="font-size: 20px; font-weight: 700; margin-top: 6px;">
                    {title}
                </div>
                <div style="font-size: 14px; color: #cccccc; margin-top: 8px;">
                    {subtitle}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Fila 1
    col1, col2, col3 = st.columns(3)
    with col1:
        card("pandas", "🐼", "Manejo de datos en DataFrames.")
    with col2:
        card("NumPy", "🔢", "Cálculo numérico y muestras aleatorias.")
    with col3:
        card("SciPy (stats)", "📐", "Intervalos de confianza y pruebas de hipótesis.")

    # Fila 2
    col4, col5, _ = st.columns(3)
    with col4:
        card("Plotly Express", "📊", "Gráficos interactivos (histogramas, boxplots).")
    with col5:
        card("Streamlit", "🌐", "Para crear el sitio web interactivo.")