import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# 🌐 Configurar layout wide
st.set_page_config(layout="wide")

# 📥 Carregar modelo treinado e scaler
modelo = joblib.load("Korea_Temperature_Prediction.pkl")
scaler = joblib.load("scaler.pkl")

# 📂 Carregar dados do CSV
df = pd.read_csv("teste.csv")

# 🔽 Remover colunas desnecessárias
df = df.drop(columns=["station", "Date"], errors="ignore")

# 🕒 Últimos 30 dias
dados_30_dias = df.tail(30).copy()

# 🎯 Iniciar valores padrão com último registro
if "valores_atuais" not in st.session_state:
    ultimo_registro = df.tail(1).copy()
    ultimo_registro = ultimo_registro.drop(columns=["Next_Tmax", "Next_Tmin"], errors="ignore")
    st.session_state.valores_atuais = ultimo_registro.to_dict(orient="records")[0]

# --- 🔧 BARRA LATERAL DE AJUSTES ---
st.sidebar.title("🔧 Parâmetros de Entrada")
entrada_usuario = {}
for coluna, valor in st.session_state.valores_atuais.items():
    min_val = float(df[coluna].min())
    max_val = float(df[coluna].max())
    entrada_usuario[coluna] = st.sidebar.slider(
        f"{coluna}", min_value=min_val, max_value=max_val,
        value=float(valor), step=0.01, key=coluna
    )

# --- TÍTULO PRINCIPAL ---
st.title("🌡️ Previsão de Temperatura - Modelo Local")

# --- BOTÃO DE PREVISÃO ---
if st.button("🔮 Prever Temperatura"):
    st.session_state.valores_atuais = entrada_usuario
    dados_input = pd.DataFrame([entrada_usuario])

    try:
        dados_input_escalado = scaler.transform(dados_input)
        predicao = modelo.predict(dados_input_escalado)[0]
        temp_max_pred, temp_min_pred = predicao[0], predicao[1]

        # --- RESULTADOS NO TOPO ---
        with st.container():
            st.markdown("""
                <style>
                .metric-container {
                    display: flex;
                    justify-content: space-around;
                    background-color: #f7f7f7;
                    padding: 20px;
                    border-radius: 15px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                    margin-bottom: 25px;
                }
                .metric {
                    text-align: center;
                    padding: 10px 20px;
                }
                .metric .label {
                    font-size: 18px;
                    color: #666;
                    margin-bottom: 8px;
                }
                .metric .value {
                    font-size: 28px;
                    font-weight: bold;
                    color: #111;
                }
                </style>
                <div class="metric-container">
                    <div class="metric">
                        <div class="label">🌞 Temperatura Máxima Prevista</div>
                        <div class="value">""" + f"{temp_max_pred:.2f}°C" + """</div>
                    </div>
                    <div class="metric">
                        <div class="label">☃️ Temperatura Mínima Prevista</div>
                        <div class="value">""" + f"{temp_min_pred:.2f}°C" + """</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.header("")
        
        # --- HISTÓRICO + PREVISÃO ---
        novo_dia = pd.DataFrame({
            "Dia": ["Previsto"],
            "Temp_Max": [temp_max_pred],
            "Temp_Min": [temp_min_pred]
        })

        historico = dados_30_dias.copy()
        historico["Dia"] = range(1, 31)
        historico = historico.rename(columns={
            "Next_Tmax": "Temp_Max",
            "Next_Tmin": "Temp_Min"
        })

        resultado = pd.concat([historico[["Dia", "Temp_Max", "Temp_Min"]], novo_dia], ignore_index=True)

        # --- EXIBIÇÃO LADO A LADO ---
        col_df, col_graf = st.columns([1, 3])

        with col_df:
            st.subheader("📋 Histórico + Previsão")
            st.dataframe(resultado, use_container_width=True)

        with col_graf:
            fig, ax = plt.subplots(figsize=(12, 4))
            ax.plot(resultado["Dia"][:-1], resultado["Temp_Max"][:-1], label="Temp Max (Real)", marker="o")
            ax.plot(resultado["Dia"][:-1], resultado["Temp_Min"][:-1], label="Temp Min (Real)", marker="o")
            ax.plot(31, temp_max_pred, "r*", label="Temp Max (Previsto)", markersize=12)
            ax.plot(31, temp_min_pred, "b*", label="Temp Min (Previsto)", markersize=12)
            ax.axvline(x=30.5, color="gray", linestyle="--", alpha=0.7)
            ax.set_title("📈 Temperatura - Últimos 30 dias + Previsão")
            ax.set_xlabel("Dias")
            ax.set_ylabel("Temperatura (°C)")
            ax.grid(True)
            ax.legend()
            st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ Erro ao gerar predição: {e}")
