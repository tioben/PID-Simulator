import streamlit as st
import pandas as pd
import altair as alt


def render_charts(tempo, pv, cv, sp):
    df = pd.DataFrame({
        "Tempo": tempo,
        "Temperatura": pv,
        "Setpoint": sp,
        "VAG": cv
    })
    df_temp = df.melt(
        "Tempo",
        value_vars=["Temperatura", "Setpoint"],
        var_name="Tipo",
        value_name="Valor"
    )

    chart_temp = alt.Chart(df_temp).mark_line().encode(
        x=alt.X(
            "Tempo",
            title="Tempo (s)"
        ),
        y=alt.Y(
            "Valor",
            title="Temperatura (°C)"
        ),
        color=alt.Color(
            "Tipo",
            legend=alt.Legend(title="Legenda")
        )

    ).properties(
        height=350,
        title="Controle de Temperatura"
    )

    chart_vag = alt.Chart(df).mark_line(
        color="#FF4B4B"
    ).encode(
        x=alt.X(
            "Tempo",
            title="Tempo (s)"
        ),
        y=alt.Y(
            "VAG",
            title="Abertura VAG (%)",
            scale=alt.Scale(
                domain=[0, 100],
                clamp=True
            )
        )
    ).properties(
        height=220,
        title="Saída do Controlador PID"
    )
    st.altair_chart(
        chart_temp & chart_vag,
        use_container_width=True
    )