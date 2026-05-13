import numpy as np

# Limites físicos
TEMP_MIN = 14.0
TEMP_MAX = 32.0

# Simulação de física do ambiente
def update_room_temperature(
    temperatura_atual,
    cv,
    room_tau,
    carga_termica,
    potencia_vag,
    frio_acumulado,
    dt
):
    # Normalização da abertura da VAG
    abertura_vag = np.clip(
        cv / 100.0,
        0.0,
        1.0
    )

    # Geração de frio pela VAG
    frio_desejado = abertura_vag * potencia_vag

    # Inércia (isso serve pra manter a temp baixando mesmo com a VAG fechada, a ideia é simular a carga térmica acumulada na serpentina)
    tau_serpentina = 8.0
    frio_acumulado = frio_acumulado + (
        (frio_desejado - frio_acumulado)
        * (dt / tau_serpentina)
    )
    frio_acumulado = max(
        frio_acumulado,
        0.0
    )

    # Sensibilidade da sala TAU
    fator_resposta_sala = 180.0 / room_tau

    # Balanço térmico
    variacao_temperatura = (
        carga_termica
        - frio_acumulado
    ) * dt * fator_resposta_sala
    nova_temperatura = temperatura_atual + variacao_temperatura

    # Limites físicos
    nova_temperatura = np.clip(
        nova_temperatura,
        TEMP_MIN,
        TEMP_MAX
    )

    return nova_temperatura, frio_acumulado