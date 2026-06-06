import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. CONFIGURACIÓN COMPATIBLE DE LA PÁGINA (LOOK CYBERPUNK)
st.set_page_config(
    page_title="NICOLL_SYSTEM_v4.0",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo visual de alta intensidad
st.html("""
    <style>
    .main { background-color: #08090E !important; color: #00FF66 !important; font-family: 'Courier New', monospace; }
    h1, h2, h3 { color: #FFFFFF !important; }
    div[data-testid="stMetric"] { 
        background-color: #111424 !important; 
        padding: 20px !important; 
        border-radius: 8px !important; 
        border: 1px solid #00FF66 !important;
    }
    </style>
""")

st.title("⚡ NICOLL SYSTEM // CORE v4.0")
st.markdown("`[SISTEMA MULTIMÓDULO: FINANZAS - ESTUDIO - EJERCICIO]`")
st.markdown("---")

# 2. CONEXIÓN CON TU GOOGLE SHEETS REAL
SHEET_ID = "1Kfni6mGq3bE2F2skY5vUaOszTuQ7iAh9Th4cI-AtcwE"
URL_FINANZAS = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=BD_FINANZAS"
URL_ESTUDIO = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=BD_ESTUDIO"
URL_EJERCICIO = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=BD_EJERCICIO"

@st.cache_data(ttl=5)
def cargar_base_datos():
    # Cargar Finanzas
    try:
        df_f = pd.read_csv(URL_FINANZAS)
        df_f.columns = df_f.columns.str.strip()
    except:
        df_f = pd.DataFrame(columns=['FECHA', 'CONCEPTO', 'DESTINO', 'INGRESO / AHORRO (+)', 'GASTO / COMPRA (-)'])
    
    # Cargar Estudio
    try:
        df_e = pd.read_csv(URL_ESTUDIO)
        df_e.columns = df_e.columns.str.strip()
    except:
        df_e = pd.DataFrame(columns=['FECHA', 'ÁREA', 'TIEMPO (MINUTOS)', 'ENERGÍA INICIAL', '¿VENCÍ LA PEREZA?', 'POMODOROS'])
        
    # Cargar Ejercicio
    try:
        df_ex = pd.read_csv(URL_EJERCICIO)
        df_ex.columns = df_ex.columns.str.strip()
    except:
        df_ex = pd.DataFrame(columns=['FECHA', 'TIPO EN TREN', 'DURACIÓN (MINUTOS)', '¿CUMPLÍ LA RUTINA?'])
        
    return df_f, df_e, df_ex

df_finanzas, df_estudio, df_ejercicio = cargar_base_datos()

# Asegurar limpieza de datos numéricos para evitar caídas del sistema
df_finanzas['INGRESO / AHORRO (+)'] = pd.to_numeric(df_finanzas['INGRESO / AHORRO (+)']).fillna(0)
df_finanzas['GASTO / COMPRA (-)'] = pd.to_numeric(df_finanzas['GASTO / COMPRA (-)']).fillna(0)
df_estudio['TIEMPO (MINUTOS)'] = pd.to_numeric(df_estudio['TIEMPO (MINUTOS)']).fillna(0)
df_ejercicio['DURACIÓN (MINUTOS)'] = pd.to_numeric(df_ejercicio['DURACIÓN (MINUTOS)']).fillna(0)

# 3. INTERFAZ DE NAVEGACIÓN
st.sidebar.title("🎮 CORTEX CONTROL")
menu = st.sidebar.radio("SELECCIONAR MÓDULO:", [
    "🪐 PANEL CENTRAL & TIEMPOS", 
    "💸 MÁQUINA FINANCIERA", 
    "🧠 MATRIZ DE ESTUDIO",
    "💪 CONTROL DE ENTRENAMIENTO"
])

st.sidebar.markdown("---")
st.sidebar.subheader("📥 ENLACES DE CONTROL")
st.sidebar.link_button("📝 Abrir Base de Datos Completa", f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit")
st.sidebar.error("🚨 RETENCIÓN OBLIGATORIA:\n$241,660 COP destinados a la cuota del celular actual.")

# =========================================================================
# MÓDULO 1: PANEL CENTRAL
# =========================================================================
if menu == "🪐 PANEL CENTRAL & TIEMPOS":
    st.header("🪐 Estación de Monitoreo de Tiempos y Fases")
    
    hoy = datetime.now()
    meta_julio = datetime(2026, 7, 15)  
    meta_octubre = datetime(2026, 10, 15) 
    
    dias_mama = (meta_julio - hoy).days
    dias_portatil = (meta_octubre - hoy).days

    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.metric(label="⏳ Días restantes para Celular de Mamá", value=f"{max(0, dias_mama)} Días")
    with col_t2:
        st.metric(label="⏳ Cuenta regresiva para Lenovo LOQ", value=f"{max(0, dias_portatil)} Días")

    st.markdown("---")
    
    total_mama = df_finanzas[df_finanzas['DESTINO'] == 'Celular Mamá']['INGRESO / AHORRO (+)'].sum()
    total_portatil = df_finanzas[df_finanzas['DESTINO'] == 'Portátil']['INGRESO / AHORRO (+)'].sum()
    total_pc = df_finanzas[df_finanzas['DESTINO'] == 'Proyecto Torre 13M']['INGRESO / AHORRO (+)'].sum()
    
    fase_1_ok = total_mama >= 700000
    fase_2_ok = total_portatil >= 5900000

    st.subheader("🛠️ ESTADO DE DESPLIEGUE SECUENCIAL")
    
    # FASE 1
    st.markdown(f"### {'🟩' if fase_1_ok else '🔥'} FASE 1: Dispositivo de Honra (Celular Mamá)")
    p1 = min(float(total_mama / 700000), 1.0) if total_mama > 0 else 0.0
    st.progress(p1)
    st.markdown(f"`Progreso Financiero: ${total_mama:,.0f} / $700,000 COP ({p1*100:.1f}%)`")
    
    # FASE 2
    st.markdown("---")
    if fase_1_ok:
        st.markdown(f"### {'🟩' if fase_2_ok else '⚡'} FASE 2: Estación Móvil de Ingeniería (Lenovo LOQ)")
        p2 = min(float(total_portatil / 5900000), 1.0) if total_portatil > 0 else 0.0
        st.progress(p2)
        st.markdown(f"`Progreso Financiero: ${total_portatil:,.0f} / $5,900,000 COP ({p2*100:.1f}%)`")
    else:
        st.markdown("### 🔒 FASE 2: Estación Móvil (Bloqueada hasta completar Fase 1)")
        
    # FASE 3
    st.markdown("---")
    if fase_1_ok and fase_2_ok:
        st.markdown("### 👾 FASE 3: Proyecto Supercomputadora ASUS ROG Hyperion")
        p3 = min(float(total_pc / 13000000), 1.0) if total_pc > 0 else 0.0
        st.progress(p3)
        st.markdown(f"`Progreso Componentes: ${total_pc:,.0f} / $13,000,000 COP ({p3*100:.1f}%)`")
    else:
        st.markdown("### 🔒 FASE 3: Proyecto Supercomputadora ASUS ROG Hyperion (Bloqueada)")

# =========================================================================
# MÓDULO 2: MÁQUINA FINANCIERA
# =========================================================================
elif menu == "💸 MÁQUINA FINANCIERA":
    st.header("💸 Flujos de Capital y Bóvedas de Resguardo")
    
    total_arq = df_finanzas[df_finanzas['DESTINO'] == 'Fondo de Emergencia (ARQ)']['INGRESO / AHORRO (+)'].sum()
    total_dolares = df_finanzas[df_finanzas['DESTINO'] == 'Ahorro Dólares']['INGRESO / AHORRO (+)'].sum()

    col_b1, col_b2 = st.columns(2)
    with col_b1:
        st.metric(label="🛡️ Bóveda de Emergencia (ARQ)", value=f"${total_arq:,.0f} COP")
    with col_b2:
        st.metric(label="💵 Cojín Anti-Devaluación (Dólares)", value=f"${total_dolares:,.0f} USD/COP")

    st.markdown("---")
    st.subheader("📋 HISTORIAL REAL DE TRANSACCIONES")
    if df_finanzas.empty:
        st.info("No hay transacciones registradas todavía en la pestaña BD_FINANZAS.")
    else:
        st.dataframe(df_finanzas, use_container_width=True)

# =========================================================================
# MÓDULO 3: MATRIZ DE ESTUDIO
# =========================================================================
elif menu == "🧠 MATRIZ DE ESTUDIO":
    st.header("🧠 Matriz de Crecimiento Intelectual")
    
    horas_totales = df_estudio['TIEMPO (MINUTOS)'].sum() / 60
    
    try:
        total_intentos = df_estudio['¿VENCÍ LA PEREZA?'].dropna().count()
        vencidas = df_estudio[df_estudio['¿VENCÍ LA PEREZA?'] == 'Sí'].shape[0]
        factor_disciplina = (vencidas / total_intentos) * 100 if total_intentos > 0 else 0.0
    except:
        factor_disciplina = 0.0

    col_e1, col_e2 = st.columns(2)
    with col_e1:
        st.metric(label="🧠 Horas de Vuelo Intelectual", value=f"{horas_totales:.1f} Hrs")
    with col_e2:
        st.metric(label="🔥 Factor de Disciplina Mental", value=f"{factor_disciplina:.1f}%")
        
    st.markdown("---")
    st.subheader("📊 Distribución de Enfoque Intelectual")
    
    if not df_estudio.empty:
        fig_pie = px.pie(
            df_estudio, 
            values='TIEMPO (MINUTOS)', 
            names='ÁREA',
            hole=0.5,
            color_discrete_sequence=['#00FF66', '#0066FF', '#FF007F']
        )
        fig_pie.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("No hay registros de estudio todavía en la pestaña BD_ESTUDIO.")
    
    st.subheader("📝 REGISTRO DE LOGS DE APRENDIZAJE")
    st.dataframe(df_estudio, use_container_width=True)

# =========================================================================
# MÓDULO 4: CONTROL DE ENTRENAMIENTO (EL EJERCICIO)
# =========================================================================
elif menu == "💪 CONTROL DE ENTRENAMIENTO":
    st.header("💪 Terminal de Alta Resistencia Física (Ejercicio)")
    st.markdown("`[EL CUERPO DE UNA INGENIERA SOPORTA LA CARGA DE SU MENTE]`")
    st.markdown("---")
    
    minutos_ejercicio = df_ejercicio['DURACIÓN (MINUTOS)'].sum()
    
    try:
        total_dias_entrenados = df_ejercicio[df_ejercicio['¿CUMPLÍ LA RUTINA?'] == 'Sí'].shape[0]
    except:
        total_dias_entrenados = 0

    col_ex1, col_ex2 = st.columns(2)
    with col_ex1:
        st.metric(label="🏃‍♂️ Minutos Totales Sudados", value=f"{minutos_ejercicio} Mins")
    with col_ex2:
        st.metric(label="🔥 Días de Rutina Completados al 100%", value=f"{total_dias_entrenados} Días")

    st.markdown("---")
    st.subheader("📊 Consistencia de Entrenamiento")
    
    if not df_ejercicio.empty:
        fig_ejercicio = px.bar(
            df_ejercicio,
            x='FECHA',
            y='DURACIÓN (MINUTOS)',
            color='TIPO EN TREN',
            title='Minutos de Ejercicio por Sesión',
            color_discrete_sequence=['#FF007F', '#0066FF', '#00FF66']
        )
        fig_ejercicio.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_ejercicio, use_container_width=True)
    else:
        st.info("Aún no has registrado ejercicios en la pestaña BD_EJERCICIO. ¡Hora de mover el esqueleto!")

    st.subheader("📝 HISTORIAL DE ENTRENAMIENTO EN VIVO")
    st.dataframe(df_ejercicio, use_container_width=True)
