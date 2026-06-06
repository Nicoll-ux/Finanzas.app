import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURACIÓN DE LA PÁGINA WEB REAL (LOOK CYBERPUNK)
st.set_page_config(
    page_title="Nicoll System - Inteligencia Personal",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo Dark Mode Avanzado / Cyberpunk mediante CSS inyectado nativo
st.markdown("""
    <style>
    .main { 
        background-color: #0D0E15; 
        color: #FFFFFF; 
    }
    div[data-testid="stMetric"] { 
        background-color: #1A1C28 !important; 
        padding: 20px !important; 
        border-radius: 12px !important; 
        border-left: 5px solid #00FF66 !important;
        box-shadow: 0 4px 10px rgba(0, 255, 102, 0.05);
    }
    div[data-testid="stMetricLabel"] {
        color: #8A8FAD !important;
        font-weight: bold !important;
    }
    div[data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-family: 'Courier New', monospace !important;
    }
    .stProgress > div > div > div > div {
        background-color: #FF007F !important;
    }
    h1, h2, h3 {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    </style>
""", unsafe_allowed_html=True)

st.title("💻 Nicoll - Sistema de Inteligencia Personal & Financiera")
st.markdown("---")

# 2. CONFIGURACIÓN DE TU BASE DE DATOS REAL (GOOGLE SHEETS)
# Remplaza este ID por el ID real de tu Google Sheets una vez lo crees y compartas el enlace como lector público.
SHEET_ID = "https://docs.google.com/spreadsheets/d/1Kfni6mGq3bE2F2skY5vUaOszTuQ7iAh9Th4cI-AtcwE/edit?gid=1153926804#gid=1153926804"
URL_ESTUDIO = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=BD_ESTUDIO"
URL_FINANZAS = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=BD_FINANZAS"

@st.cache_data(ttl=30)  # Actualiza los datos de la web automáticamente cada 30 segundos
def cargar_datos():
    try:
        df_estudio = pd.read_csv(URL_ESTUDIO)
        df_finanzas = pd.read_csv(URL_FINANZAS)
        # Limpieza rápida de columnas para evitar espacios
        df_estudio.columns = df_estudio.columns.str.strip()
        df_finanzas.columns = df_finanzas.columns.str.strip()
        return df_estudio, df_finanzas
    except Exception as e:
        # Datos de simulación en caso de que no esté conectado el Google Sheets aún
        datos_estudio_mock = {
            'FECHA': ['05/06/2026', '05/06/2026'],
            'ÁREA': ['Ciberseguridad', 'Inglés'],
            'TIEMPO (MINUTOS)': [45, 30],
            'ENERGÍA INICIAL': ['1-Agotada Ísimo', '3-Media'],
            '¿VENCÍ LA PEREZA?': ['Sí', 'No aplica'],
            'POMODOROS': [1.8, 1.2]
        }
        datos_finanzas_mock = {
            'FECHA': ['01/06/2026', '05/06/2026'],
            'CONCEPTO': ['Quincena Ísimo', 'Ahorro Celular Mamá'],
            'DESTINO': ['Cuota Celular Actual', 'Celular Mamá'],
            'INGRESO / AHORRO (+)': [0, 150000],
            'GASTO / COMPRA (-)': [241660, 0]
        }
        return pd.DataFrame(datos_estudio_mock), pd.DataFrame(datos_finanzas_mock)

df_estudio, df_finanzas = cargar_datos()

# 3. MENÚ LATERAL (SIDEBAR DE NAVEGACIÓN)
st.sidebar.title("🎛️ Panel de Control")
menu = st.sidebar.radio("Ir a la sección:", ["🎯 Dashboard & Línea Temporal", "💸 Gestión Financiera", "🧠 Bitácora de Estudio"])

# Recordatorio constante en la barra lateral
st.sidebar.markdown("---")
st.sidebar.warning("⚠️ **Gasto Fijo Obligatorio:** Recuerda separar quincenalmente los **$241,660 COP** de la cuota de tu celular actual.")

# =========================================================================
# MENÚ 1: DASHBOARD & LÍNEA TEMPORAL SECUENCIAL
# =========================================================================
if menu == "🎯 Dashboard & Línea Temporal":
    st.header("🚀 Línea Temporal del Éxito Financiado")
    st.write("Progreso de tus metas paso a paso, de forma estrictamente ordenada como la hormiga.")
    
    # Cálculos reales de ahorros acumulados
    total_mama = df_finanzas[df_finanzas['DESTINO'] == 'Celular Mamá']['INGRESO / AHORRO (+)'].sum()
    total_portatil = df_finanzas[df_finanzas['DESTINO'] == 'Portátil']['INGRESO / AHORRO (+)'].sum()
    total_pc = df_finanzas[df_finanzas['DESTINO'] == 'Proyecto Torre 13M']['INGRESO / AHORRO (+)'].sum()
    
    # Banderas automáticas de completado basadas en valores reales de ahorro
    fase_1_completada = total_mama >= 700000
    fase_2_completada = total_portatil >= 5900000
    
    # --- FASE 1 ---
    if not fase_1_completada:
        st.subheader("🔴 FASE 1 EN CURSO: 💓 Celular de Mamá (Meta: Julio)")
        progreso_m = min(float(total_mama / 700000), 1.0)
        st.progress(progreso_m)
        st.caption(f"Fondo Actual: ${total_mama:,.0f} COP / $700,000 COP ({progreso_m * 100:.1f}%)")
    else:
        st.success("🎉 **FASE 1 COMPLETADA:** ¡El celular de tu mamá está 100% financiado! Siguiente paso liberado.")

    st.markdown("---")

    # --- FASE 2 ---
    if fase_1_completada and not fase_2_completada:
        st.subheader("🔵 FASE 2 EN CURSO: 💻 Portátil Lenovo LOQ (Meta: Octubre)")
        progreso_p = min(float(total_portatil / 5900000), 1.0)
        st.progress(progreso_p)
        st.caption(f"Fondo Actual: ${total_portatil:,.0f} COP / $5,900,000 COP ({progreso_p * 100:.1f}%)")
    elif not fase_1_completada:
        st.subheader("🔒 FASE 2: 💻 Portátil Lenovo LOQ ($5.9M)")
        st.info("Esta fase se desbloqueará automáticamente en internet cuando la Fase 1 llegue al 100%.")
    else:
        st.success("🚀 **FASE 2 COMPLETADA:** ¡Tu portátil Lenovo LOQ de ingeniería está comprado! Tu potencial técnico está libre.")

    st.markdown("---")

    # --- FASE 3 ---
    if fase_2_completada:
        st.subheader("⚡ FASE 3 EN CURSO: 🖥️ Proyecto Torre ASUS ROG Hyperion + AMD ($13M)")
        progreso_torre = min(float(total_pc / 13000000), 1.0)
        st.progress(progreso_torre)
        st.caption(f"Ahorro acumulado para componentes: ${total_pc:,.0f} COP / $13,000,000 COP ({progreso_torre * 100:.1f}%)")
    else:
        st.subheader("🔒 FASE 3: 🖥️ Proyecto Torre ASUS ROG Hyperion GR701")
        st.info("Bloqueado estructuralmente. Enfócate primero en el celular de tu mamá y tu portátil de estudio.")

# =========================================================================
# MENÚ 2: GESTIÓN FINANCIERA (Resguardos + Recompensa)
# =========================================================================
elif menu == "💸 Gestión Financiera":
    st.header("💸 Distribución Financiera de Resguardos y Metas")
    
    # Cálculos detallados por categorías financieras
    total_mama = df_finanzas[df_finanzas['DESTINO'] == 'Celular Mamá']['INGRESO / AHORRO (+)'].sum()
    total_portatil = df_finanzas[df_finanzas['DESTINO'] == 'Portátil']['INGRESO / AHORRO (+)'].sum()
    total_arq = df_finanzas[df_finanzas['DESTINO'] == 'Fondo de Emergencia (ARQ)']['INGRESO / AHORRO (+)'].sum()
    total_dolares = df_finanzas[df_finanzas['DESTINO'] == 'Ahorro Dólares']['INGRESO / AHORRO (+)'].sum()
    total_pc = df_finanzas[df_finanzas['DESTINO'] == 'Proyecto Torre 13M']['INGRESO / AHORRO (+)'].sum()

    st.subheader("🛡️ Escudo Protector (Ahorros de Resguardo Constante)")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.metric(label="🛡️ Cuenta ARQ (Fondo de Emergencia)", value=f"${total_arq:,.0f} COP")
        st.caption("Dinero intocable para imprevistos pesados.")
    with col_f2:
        st.metric(label="💵 Bolsillo de Dólares Digitales", value=f"${total_dolares:,.0f} USD/COP")
        st.caption("Tu protección contra la devaluación.")

    st.markdown("---")
    st.subheader("📋 Historial de Transacciones Financieras Reales")
    st.dataframe(df_finanzas, use_container_width=True)

# =========================================================================
# MENÚ 3: BITÁCORA DE ESTUDIO (Ciberseguridad, Inglés, Alemán)
# =========================================================================
elif menu == "🧠 Bitácora de Estudio":
    st.header("🧠 Bitácora de Conocimiento Avanzado")
    
    # Análisis de Datos sobre las horas de estudio
    minutos_totales = df_estudio['TIEMPO (MINUTOS)'].sum()
    horas_totales = minutos_totales / 60
    
    # Métrica de dominio propio personalizada (Victorias sobre el cansancio)
    try:
        victorias_pereza = df_estudio[
            (df_estudio['ENERGÍA INICIAL'] == '1-Agotada Ísimo') & 
            (df_estudio['¿VENCÍ LA PEREZA?'] == 'Sí')
        ].shape[0]
    except:
        victorias_pereza = 0
        
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        st.metric(label="⏳ Horas de Poder Intelectual", value=f"{horas_totales:.1f} Horas")
        st.caption("Tiempo real invertido en tu transformación.")
    with col_e2:
        st.metric(label="🔥 Victorias sobre el Cansancio de Ísimo", value=f"{victorias_pereza} Veces")
        st.caption("Días en que le ganaste al sueño y honraste tu futuro.")

    st.markdown("---")
    
    # Gráfico interactivo circular de distribución usando Plotly Express
    st.subheader("📊 Distribución Tecnológica y de Idiomas")
    if not df_estudio.empty:
        fig_anillo = px.pie(
            df_estudio, 
            values='TIEMPO (MINUTOS)', 
            names='ÁREA', 
            hole=0.4,
            color_discrete_sequence=['#00FF66', '#0066FF', '#FF007F']
        )
        fig_anillo.update_layout(
            template="plotly_dark", 
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_anillo, use_container_width=True)
    else:
        st.info("Aún no hay registros de estudio en la base de datos.")

    # Estado del Proyecto Avanzado de Ensamble de Hardware ASUS ROG / AMD
    st.markdown("---")
    st.subheader("🖥️ Lista de Deseos Técnica: Proyecto ASUS ROG Hyperion")
    st.write("Estado de adquisición por partes (Fase 3):")
    
    # Checklist dinámica basada en el ahorro acumulado para la PC de 13M
    componentes = [
        ("Chasis ASUS ROG Hyperion GR701", 1700000),
        ("Fuente de Poder ROG Thor 1000W OLED", 1400000),
        ("Procesador AMD Ryzen 7 7800X3D", 1900000),
        ("Motherboard ROG Strix X670E-E", 2200000),
        ("Memoria RAM 32GB DDR5 + SSD 2TB", 1500000),
        ("Refrigeración Líquida ROG Ryujin III LCD", 1600000),
        ("Tarjeta Gráfica ROG Strix RTX Serie 40", 4500000),
        ("Pantalla Gamer ASUS ROG 300Hz", 2200000)
    ]
    
    acumulado_temp = total_pc
    for comp, costo in componentes:
        if acumulado_temp >= costo:
            st.success(f"✅ {comp} — **¡ADQUIRIDO DE CONTADO!**")
            acumulado_temp -= costo
        else:
            st.info(f"⏳ {comp} — En ruta de ahorro (Costo estimado: ${costo:,.0f} COP)")

    st.markdown("---")
    st.subheader("📝 Historial Clínico de Sesiones de Estudio")
    st.dataframe(df_estudio, use_container_width=True)
