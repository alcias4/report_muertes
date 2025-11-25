from pandas import  DataFrame
from scipy import stats
import numpy as np
import streamlit as st
import plotly.express as px



def pageInferenecia(df: DataFrame, enferm: str):


    x = df[enferm].dropna()

    # 2. Estadísticos descriptivos básicos
    media = x.mean() # type: ignore

    # 3. Intervalo de confianza 95% para la media
    ic_low, ic_high = stats.t.interval(
        confidence=0.95,
        df=len(x) - 1,
        loc=media,
        scale=stats.sem(x) #type: ignore
    )

    st.write(
        f"IC 95% para la media: **({ic_low:.2f}, {ic_high:.2f})**"
    )



    # Bootstrap de la media
    n_boot = 200
    medias_boot = []

    for _ in range(n_boot):
        muestra = np.random.choice(x, size=len(x), replace=True)
        medias_boot.append(muestra.mean())

    medias_boot = np.array(medias_boot)

    # Media de las medias bootstrap
    media_boot = medias_boot.mean()

    # IC 95% bootstrap (percentiles 2.5% y 97.5%)
    ic_boot_low, ic_boot_high = np.percentile(medias_boot, [2.5, 97.5])

    # Histograma de las medias bootstrap
    fig_boot = px.histogram(
        medias_boot,
        nbins=20,
        title=f"Gráfico de la media de muertes por {enferm}",
        labels={"value": f"Media de muertes por {enferm}", "count": "Frecuencia"},
    )

    fig_boot.update_layout(template="simple_white")

    # Línea verde: media bootstrap
    fig_boot.add_vline(
        x=media_boot,
        line_dash="dash",
        line_color="green",
        line_width=2,
        annotation_text=f"{media_boot:.2f}",
        annotation_position="top"
    )

    # Líneas rojas: IC 95% bootstrap
    fig_boot.add_vline(
        x=ic_boot_low,
        line_dash="dash",
        line_color="green",
        line_width=2,
        annotation_text=f"IC: {ic_boot_low:.2f}",
        annotation_position="top left"
    )

    fig_boot.add_vline(
        x=ic_boot_high,
        line_dash="dash",
        line_color="green",
        line_width=2,
        annotation_text=f"IC: {ic_boot_high:.2f}",
        annotation_position="top right",
        
    )

    st.plotly_chart(fig_boot, use_container_width=True)
    st.divider()
    calHipotesis(df=df, enferm=enferm)
    st.divider()
    muestreo(df=df, enferm=enferm)



def calHipotesis(df: DataFrame, enferm: str):
    # Datos de la variable seleccionada (por ejemplo "Meningitis")
    x = df[enferm].dropna()

    if len(x) == 0:
        st.warning(f"No hay datos para {enferm}")
        return

    # Estadísticos descriptivos básicos
    media = x.mean()
    desviacion = np.std(x, ddof=1)

    st.subheader(f"Estadísticos para {enferm}")
    st.write(f"Media muestral: **{media:.2f}**")
    st.write(f"Desviación estándar muestral: **{desviacion:.2f}**")

    # -----------------------------
    # 3. Prueba de hipótesis
    #    ¿La media es mayor que mu0?
    # -----------------------------
    valor_ref: str | None = st.text_input("Valor de media de hipotesis", placeholder="2500")
    handle_click = st.button("nuevo valor")
    mu0 =  2500

    if handle_click:
        if valor_ref != None:
            mu0 = float(valor_ref)  # valor de referencia (cámbialo según tu análisis)
    alpha = 0.05  # nivel de significancia

    # t de Student una muestra
    t_stat, p_two_sided = stats.ttest_1samp(x, popmean=mu0)

    # Convertir a prueba de una cola H1: mu > mu0
    if media > mu0:
        p_val = p_two_sided / 2
    else:
        # caso raro: si la media < mu0, la cola que nos interesa está al otro lado
        p_val = 1 - p_two_sided / 2

    st.subheader("Prueba de hipótesis sobre la media")

    st.markdown(f"""
**Planteamiento**

- H₀: μ = {mu0:.2f}  → la media anual de muertes por **{enferm}** es igual a {mu0:.0f}.
- H₁: μ > {mu0:.2f}  → la media anual de muertes por **{enferm}** es **mayor** que {mu0:.0f}.

**Resultados (t de Student, una muestra)**

- Estadístico t = **{t_stat:.3f}**
- Valor p (una cola) = **{p_val:.4f}**
- Nivel de significancia α = **{alpha:.2f}**
""")

    # Conclusión automática
    if p_val < alpha:
        st.success(
            f"Como p = {p_val:.4f} < α = {alpha:.2f}, **rechazamos H₀**.\n\n"
            f"Conclución que hay evidencia estadística al 95% de confianza,"
            f"de que la media anual de muertes por {enferm} es **mayor que {mu0:.0f}**."
        )
    else:
        st.error(
            f"Como p = {p_val:.4f} ≥ α = {alpha:.2f}, **no rechazamos H₀**.\n\n"
            f"Los datos **no aportan evidencia suficiente** para afirmar que la media anual "
            f"de muertes por {enferm} sea mayor que {mu0:.0f}. "
            f"Aunque la media muestral es {media:.2f}"

        )


def muestreo(df: DataFrame, enferm: str):
    x = df[enferm].dropna()
     # 4. Muestreo y diferencias
    # ==========================
    st.subheader("Muestreo y comparación de medias")

    # convertimos a array NumPy para usar choice sin líos
    valores = x.to_numpy(dtype=float)

    # tamaño de cada muestra (puedes cambiar 8 por 10, 12, etc.)
    tam_muestra = 8

    # dos muestras aleatorias del MISMO conjunto de datos
    muestra1 = np.random.choice(valores, size=tam_muestra, replace=True)
    muestra2 = np.random.choice(valores, size=tam_muestra, replace=True)

    media_m1 = np.mean(muestra1)
    media_m2 = np.mean(muestra2)

    st.write(f"Media muestra 1: **{media_m1:.2f}**")
    st.write(f"Media muestra 2: **{media_m2:.2f}**")

    # armamos DataFrame para el boxplot
    df_muestras = DataFrame({
        "Grupo": ["Muestra 1"] * tam_muestra + ["Muestra 2"] * tam_muestra,
        "Valor": np.concatenate([muestra1, muestra2])
    })

    fig_muestras = px.box(
        df_muestras,
        x="Grupo",
        y="Valor",
        title=f"Comparación entre dos muestras aleatorias de muertes por {enferm}",
        points="all"  # para ver también los puntos individuales
    )

    fig_muestras.update_layout(
        template="simple_white",
        yaxis_title=f"Muertes por {enferm}"
    )

    st.plotly_chart(fig_muestras, use_container_width=True)

