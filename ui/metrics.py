import streamlit as st


def render_metrics(pv, cv, erro, componentes, tempo):

    st.subheader("Dados de Processo")

    c1, c2, c3 = st.columns(3)

    c1.metric("Temperatura Ambiente", f"{pv:.2f} °C")
    c2.metric("Abertura VAG", f"{cv:.1f} %")
    c3.metric("Erro (offset)", f"{erro:.2f} °C")

    st.sidebar.divider()
    st.sidebar.subheader("Dados Avançados")

    col1, col2 = st.sidebar.columns(2)

    col1.metric("Kp", f"{componentes[0]:.2f}")
    col2.metric("Ki", f"{componentes[1]:.2f}")

    col1.metric("Kd", f"{componentes[2]:.2f}")
    col2.metric("Tempo", f"{tempo:.1f} s")
