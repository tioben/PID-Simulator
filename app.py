# startar projeto = py -m streamlit run app.py

import streamlit as st
import time

from core.simulation import (
    initialize_simulation,
    simulation_step,
    inject_anomaly
)

from ui.sidebar import render_sidebar
from ui.metrics import render_metrics
from ui.charts import render_charts

st.set_page_config(
    page_title="Simulador PID Industrial",
    layout="wide"
)

st.title(
    "Simulador PID: Controle de Temperatura de Sala"
)

config = render_sidebar()

if "sim_state" not in st.session_state:
    st.session_state.sim_state = "parado"
if "sim_data" not in st.session_state:
    st.session_state.sim_data = None

st.subheader("Controles")

col1, col2, col3 = st.columns([1.5, 1, 1.5])

with col1:

    btn_start = st.button(
        "Iniciar Simulação",
        type="primary",
        use_container_width=True,
        disabled=st.session_state.sim_state == "rodando"
    )
with col2:

    btn_pause = st.button(
        "Pausar",
        use_container_width=True,
        disabled=st.session_state.sim_state != "rodando"
    )
with col3:

    btn_reset = st.button(
        "Reiniciar",
        use_container_width=True
    )

# Controle de estado
if btn_start:
    st.session_state.sim_state = "rodando"
    st.rerun()
if btn_pause:
    st.session_state.sim_state = "pausado"
    st.rerun()
if btn_reset:
    st.session_state.sim_state = "parado"
    st.session_state.sim_data = None
    st.rerun()

# Inicialização
if st.session_state.sim_data is None:
    st.session_state.sim_data = initialize_simulation(
        config
    )
sim_data = st.session_state.sim_data

# Perturbação
if config["inject_anomaly"]:
    inject_anomaly(
        sim_data,
        config["anomaly_value"]
    )

# Simulação rodando
if st.session_state.sim_state == "rodando":
    simulation_step(
        sim_data,
        config
    )
    render_metrics(
        sim_data["pv"][-1],
        sim_data["cv"][-1],
        config["setpoint"] - sim_data["pv"][-1],
        sim_data["pid"].components,
        sim_data["tempo"][-1]
    )

    render_charts(
        sim_data["tempo"],
        sim_data["pv"],
        sim_data["cv"],
        sim_data["sp"]
    )
    time.sleep(0.02)
    st.rerun()

# Pausado
elif st.session_state.sim_state == "pausado":
    render_metrics(
        sim_data["pv"][-1],
        sim_data["cv"][-1],
        config["setpoint"] - sim_data["pv"][-1],
        sim_data["pid"].components,
        sim_data["tempo"][-1]
    )

    render_charts(
        sim_data["tempo"],
        sim_data["pv"],
        sim_data["cv"],
        sim_data["sp"]
    )

    st.warning("Simulação pausada.")