import streamlit as st


def render_sidebar():
    with st.sidebar:
        st.header("Configurações")

        # Controlador PID
        st.subheader("Controlador PID")
        kp = st.number_input(
            "Kp",
            value=10.0,
            min_value=0.0,
            step=0.1,
            key="kp_input"
        )
        ki = st.number_input(
            "Ki",
            value=0.5,
            min_value=0.0,
            step=0.01,
            key="ki_input"
        )
        kd = st.number_input(
            "Kd",
            value=1.0,
            min_value=0.0,
            step=0.1,
            key="kd_input"
        )
        st.divider()

        # Setpoint e modo de operação
        st.subheader("Alvo de Controle")
        setpoint = st.number_input(
            "Setpoint",
            value=20.0,
            min_value=14.0,
            max_value=32.0,
            step=0.5,
            key="setpoint_input"
        )
        mode = st.radio(
            "Modo",
            [
                "Refrigeração (Reverse Acting)",
                "Aquecimento (Direct Acting)"
            ],
            key="mode_input"
        )
        st.divider()

        # Modelo térmico da sala
        st.subheader("Modelo Térmico da Sala")
        room_tau = st.number_input(
            "Constante Térmica da Sala - Tau (s)",
            value=180.0,
            min_value=10.0,
            step=10.0,
            key="room_tau_input_v3",
            help="""
                Representa a inércia térmica do ambiente.

                Quanto MAIOR o valor:

                • Mais lenta será a variação da temperatura  
                • Mais tempo a sala levará para responder à VAG  
                • A VAG permanecerá aberta por mais tempo  
                • O sistema ficará mais próximo de um ambiente com alta massa térmica  
                • O PID precisará sustentar a refrigeração continuamente

                Quanto MENOR o valor:

                • Mais rápida será a resposta da temperatura  
                • A sala ficará mais sensível à abertura da VAG  
                • O overshoot ficará mais fácil de visualizar  
                • O sistema ficará mais agressivo e menos amortecido

                Exemplo prático:

                • 40s  → Sala muito sensível / resposta rápida  
                • 180s → Sala comercial moderada  
                • 400s → Ambiente pesado / alta inércia térmica
            """
        )

        carga_termica = st.number_input(
            "Carga Térmica",
            value=0.15,
            min_value=0.0,
            step=0.01,
            key="carga_termica_input",
            help="""
                Representa a força que faz a temperatura ambiente subir.

                Simula fatores como:

                • Pessoas na sala  
                • Equipamentos ligados  
                • Computadores  
                • Iluminação  
                • Calor externo  
                • Insolação  
                • Porta aberta  
                • Carga térmica do prédio

                Quanto MAIOR o valor:

                • Mais rápido a sala aquece naturalmente  
                • Maior esforço será exigido da VAG  
                • O PID precisará abrir mais a válvula  
                • A CAG será mais exigida

                Exemplo:

                • 0.02 → Sala fria / baixa carga  
                • 0.15 → Escritório comum  
                • 0.40 → Ambiente quente / alta ocupação  
                • 0.80 → Carga muito alta, podendo vencer a VAG
            """
        )

        potencia_vag = st.number_input(
            "Potência de Resfriamento da VAG",
            value=0.50,
            min_value=0.0,
            step=0.01,
            key="potencia_vag_input",
            help="""
                Representa a força de resfriamento da VAG quando ela está 100% aberta.

                Este valor é equivalente à carga térmica, porém no sentido contrário.

                Exemplo:

                • Carga térmica = 0.15  
                • Potência da VAG = 0.50  

                Nesse caso, a VAG tem força suficiente para vencer a carga térmica
                quando estiver bem aberta.

                Quanto MAIOR o valor:

                • Mais rápido a temperatura cai  
                • Mais sensível a sala fica à abertura da VAG  
                • Maior a chance de overshoot de frio  
                • Mais evidente fica o efeito de Ki alto

                Quanto MENOR o valor:

                • A VAG tem menos autoridade  
                • A carga térmica pode vencer o resfriamento  
                • A sala demora mais para chegar no setpoint  
                • O PID pode saturar a válvula sem conseguir controlar bem

                Exemplos didáticos:

                • 0.20 → VAG fraca  
                • 0.50 → VAG normal / boa autoridade  
                • 1.00 → VAG muito forte / resposta agressiva
            """
        )

        st.divider()

        # Perturbação
        st.subheader("Perturbação")
        anomaly_value = st.number_input(
            "Perturbação Térmica",
            value=0.0,
            step=0.1,
            key="anomaly_value_input",
            help="""
                Aplica uma alteração instantânea na temperatura ambiente.

                Use para simular eventos como:

                • Entrada de pessoas na sala  
                • Porta aberta  
                • Mudança brusca de carga térmica  
                • Ar quente entrando no ambiente  
                • Ar frio entrando no ambiente

                Exemplo:

                • +3.0 °C → Simula uma carga quente entrando  
                • -2.0 °C → Simula uma queda brusca de temperatura
            """
        )

        inject_anomaly = st.button(
            "Injetar Perturbação",
            use_container_width=True,
            key="inject_anomaly_button"
        )

        return {
            "kp": kp,
            "ki": ki,
            "kd": kd,
            "setpoint": setpoint,
            "mode": mode,
            "room_tau": room_tau,
            "carga_termica": carga_termica,
            "potencia_vag": potencia_vag,
            "inject_anomaly": inject_anomaly,
            "anomaly_value": anomaly_value
        }