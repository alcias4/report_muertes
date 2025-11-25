from pandas import DataFrame
import streamlit as st
import plotly.express as px


def mapaMundo(dato: DataFrame, enfe: str, year: tuple[int, int]):

    variable = False

    col1, col2 = st.columns(2)

    with col1: 
        cargar_map =  st.button("Cargar mapa",width="stretch")
    with col2:
        quitar_map =  st.button("Quitar mapa",width="stretch")


    if cargar_map:
        variable = True

    if quitar_map:
        variable = False

    min_year, max_yar = year
    data_filtrada =  dato[(dato["Año"] >= min_year ) & (dato["Año"] <= max_yar)]



    texto = f"en {min_year}" if min_year == max_yar else f"en {min_year} and {max_yar}"

    tabla = data_filtrada.groupby(["Codigo","Pais_Territorio"])[enfe].sum().reset_index(name=f"{enfe}")
    fig = px.choropleth( # type: ignore
        tabla, 
        locations="Codigo",
        hover_name="Pais_Territorio",
        hover_data=[enfe],
        color_continuous_scale="Viridis",  # escala de color
        projection="natural earth",        # cómo se ve el mapamundi
        labels={"valor": "Casos"},         # nombre bonito para la barra de color
        title=f"Mapa mundial de casos de muerte por {enfe}: {texto}",
    ) 

    
    fig.update_geos(  # ✅ método correcto # type: ignore
    showcoastlines=True,
    coastlinecolor="white",
    showland=True,
    landcolor="rgb(230, 230, 230)",
    showcountries=True,
    countrycolor="black",
    )

    # Mejora de layout: márgenes y barra de color
    fig.update_layout( # type: ignore
        margin=dict(l=0, r=0, t=40, b=0),
        coloraxis_colorbar=dict(
            title="Casos",
        ),
    )

    if variable:
        st.plotly_chart(fig,use_container_width=True) # type: ignore
    