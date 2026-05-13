import numpy as np
from simple_pid import PID
from collections import deque

from core.thermal_model import update_room_temperature


# Configurações da simulação
TEMP_MIN = 14.0
TEMP_MAX = 32.0
DT = 0.1
MAX_HISTORY = 1000 # aumentar muito trava
TEMPERATURA_INICIAL = 23.0

# Direction
def apply_direction(value, mode):
    if "Refrigeração" in mode:
        return -abs(value)

    return abs(value)

# Criação do PID
def create_pid(config):
    return PID(
        apply_direction(config["kp"], config["mode"]),
        apply_direction(config["ki"], config["mode"]),
        apply_direction(config["kd"], config["mode"]),
        setpoint=config["setpoint"],
        sample_time=DT,
        output_limits=(0, 100)
    )

# Inicia simulation
def initialize_simulation(config):
    pid = create_pid(config)

    return {
        "pid": pid,
        "tempo": deque(
            [0.0],
            maxlen=MAX_HISTORY
        ),
        "pv": deque(
            [TEMPERATURA_INICIAL],
            maxlen=MAX_HISTORY
        ),
        "cv": deque(
            [0.0],
            maxlen=MAX_HISTORY
        ),
        "sp": deque(
            [config["setpoint"]],
            maxlen=MAX_HISTORY
        ),
        "temperatura_real": TEMPERATURA_INICIAL,

        # Frio acumulado para simular overshoot
        "frio_acumulado": 0.0,
        "last_config": (
            config["kp"],
            config["ki"],
            config["kd"],
            config["mode"]
        )
    }

# Pertubação térmica
def inject_anomaly(sim_data, value):
    sim_data["temperatura_real"] += value
    sim_data["temperatura_real"] = np.clip(
        sim_data["temperatura_real"],
        TEMP_MIN,
        TEMP_MAX
    )

# Ciclo da simulação
def simulation_step(sim_data, config):
    # Verificação de ganhas ou modos; Reset de PID; Limpeza de catche
    current_config = (
        config["kp"],
        config["ki"],
        config["kd"],
        config["mode"]
    )
    if sim_data["last_config"] != current_config:
        sim_data["pid"] = create_pid(config)
        sim_data["last_config"] = current_config
    pid = sim_data["pid"]

    # Atualiza sp
    pid.setpoint = config["setpoint"]

    # Leitura atual do process value
    pv_anterior = sim_data["pv"][-1]

    # Cálculo do PID
    cv = pid(
        pv_anterior,
        dt=DT
    )

    # Modelo térmico da sala - Como a Temp_Amb reage a VAG
    temperatura_real, frio_acumulado = update_room_temperature(
        temperatura_atual=sim_data["temperatura_real"],
        cv=cv,
        room_tau=config["room_tau"],
        carga_termica=config["carga_termica"],
        potencia_vag=config["potencia_vag"],
        frio_acumulado=sim_data["frio_acumulado"],
        dt=DT
    )
    sim_data["frio_acumulado"] = frio_acumulado

    # Ruído do sensor - Simula pequenas variações normais de leitura em um sensor real.
    ruido = np.random.normal(
        0,
        0.03
    )
    pv = temperatura_real + ruido

    # Tempo da simulação
    novo_tempo = sim_data["tempo"][-1] + DT

    # Histórico
    sim_data["tempo"].append(novo_tempo)
    sim_data["pv"].append(pv)
    sim_data["cv"].append(cv)
    sim_data["sp"].append(config["setpoint"])
    sim_data["temperatura_real"] = temperatura_real