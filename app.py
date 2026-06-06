import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. CONFIGURACIÓN COMPATIBLE DE LA PÁGINA (LOOK CYBERPUNK SEGURO)
st.set_page_config(
    page_title="NICOLL_SYSTEM_v2.1",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyección de estilo simplificada y blindada para Python 3.14
st.html("""
    <style>
    .main { background-color: #08090E !important; color: #00FF66 !important; font-family: 'Courier New', monospace; }
    h1, h2, h3 { color: #FFFFFF !important; }
    </style>
""")

st.title("⚡ NICOLL SYSTEM // CORE v2.1")
st.markdown("`[SISTEMA AUTOMATIZADO DE SEGUIMIENTO DE METAS - COMPATIBLE PYTHON 3.14]`")
st.markdown("---")

# 2. MOTOR DE CONEXIÓN CON TU GOOGLE SHEETS
SHEET_ID = "https://docs.google.com/spreadsheets/d/1Kfni6mGq3bE2F2skY5vUaOszTuQ7iAh9Th4cI-AtcwE/edit?gid=1153926804#gid=1153926804"
URL_ESTUDIO = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=BD_ESTUDIO"
URL_FINANZAS = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=BD_FINANZAS"

@st.cache_data(ttl=15)
def cargar_base_datos():
    try:
        df_estudio = pd.read_csv(URL_ESTUDIO)
        df_finanzas = pd.read_csv(URL_FINANZAS)
        df_estudio.columns = df_estudio.columns.str.strip()
        df_finanzas.columns = df_finanzas.columns.str.strip()
        return df_estudio, df_finanzas
    except:
        # Datos Simulados (Mock) idénticos para que veas la estructura mientras conectas tu Sheets
        mock_e = {'FECHA':['05/06/2026']*3, 'ÁREA':['Ciberseguridad', 'Inglés', 'Alemán'], 'TIEMPO (MINUTOS)':[60, 45, 30], 'ENERGÍA INICIAL':['1-Agotada Ísimo', '3-Media', '4-Alta'], '¿VENCÍ LA PEREZA?':['Sí', 'Sí', 'No aplica']}
        mock_f = {'FECHA':['01/06/2026']*4, 'CONCEPTO':['Quincena', 'Ahorro', 'Ahorro', 'Gasto'], 'DESTINO':['Fondo de Emergencia (ARQ)', 'Celular Mamá', 'Portátil', 'Cuota Celular Actual'], 'INGRESO / AHORRO (+)':[100000, 350000, 400000, 0], 'GASTO / COMPRA (-)':[0, 0, 0, 241660]}
        return pd.DataFrame(mock_e), pd.DataFrame(mock_f)

df_estudio, df_finanzas = cargar_base_datos()

# 3. INTERFAZ DE NAVEGACIÓN
st.sidebar.title("🎮 CORTEX CONTROL")
menu = st.sidebar.radio("SELECCIONAR MÓDULO:", ["🪐 PANEL CENTRAL & TIEMPOS", "💸 MÁQUINA FINANCIERA", "🧠 MATRIZ DE ESTUDIO"])

st.sidebar.markdown("---")
st.sidebar.error("🚨 RETENCIÓN OBLIGATORIA:\n$241,660 COP destinados a la cuota del celular actual.")

# =========================================================================
# MÓDULO 1: PANEL CENTRAL (CON TEMPORIZADORES REALES)
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
    p1 = min(float(total_mama / 700000), 1.0)
    st.progress(p1)
    st.markdown(f"`Progreso Financiero: ${total_mama:,.0f} / $700,000 COP ({p1*100:.1f}%)`")
    
    # FASE 2
    st.markdown("---")
    if fase_1_ok:
        st.markdown(f"### {'🟩' if fase_2_ok else '⚡'} FASE 2: Estación Móvil de Ingeniería (Lenovo LOQ)")
        p2 = min(float(total_portatil / 5900000), 1.0)
        st.progress(p2)
        st.markdown(f"`Progreso Financiero: ${total_portatil:,.0f} / $5,900,000 COP ({p2*100:.1f}%)`")
    else:
        st.markdown("### 🔒 FASE 2: Estación Móvil (Bloqueada hasta completar Fase 1)")
        
    # FASE 3
    st.markdown("---")
    if fase_1_ok and fase_2_ok:
        st.markdown("### 👾 FASE 3: Proyecto Supercomputadora ASUS ROG Hyperion")
        p3 = min(float(total_pc / 13000000), 1.0)
        st.progress(p3)
        st.markdown(f"`Progreso Componentes: ${total_pc:,.0f} / $13,000,000 COP ({p3*100:.1f}%)`")
    else:
        st.markdown("### 🔒 FASE 3: Proyecto Supercomputadora ASUS ROG Hyperion (Bloqueada)")

# =========================================================================
# MÓDULO 2: MÁQUINA FINANCIERA (GRÁFICOS DE HARDWARE)
# =========================================================================
elif menu == "💸 MÁQUINA FINANCIERA":
    st.header("💸 Flujos de Capital y Bóvedas de Resguardo")
    
    total_arq = df_finanzas[df_finanzas['DESTINO'] == 'Fondo de Emergencia (ARQ)']['INGRESO / AHORRO (+)'].sum()
    total_dolares = df_finanzas[df_finanzas['DESTINO'] == 'Ahorro Dólares']['INGRESO / AHORRO (+)'].sum()
    total_pc = df_finanzas[df_finanzas['DESTINO'] == 'Proyecto Torre 13M']['INGRESO / AHORRO (+)'].sum()

    col_b1, col_b2 = st.columns(2)
    with col_b1:
        st.metric(label="🛡️ Bóveda de Emergencia (ARQ)", value=f"${total_arq:,.0f} COP")
    with col_b2:
        st.metric(label="💵 Cojín Anti-Devaluación (Dólares)", value=f"${total_dolares:,.0f} USD/COP")

    st.markdown("---")
    st.subheader("🖥️ INVENTARIO COMPONENTE POR COMPONENTE (ASUS ROG)")
    
    piezas = [
        {"Componente": "Chasis ROG Hyperion GR701", "Costo": 1700000},
        {"Componente": "Fuente ROG Thor 1000W OLED", "Costo": 1400000},
        {"Componente": "Procesador AMD Ryzen 7 7800X3D", "Costo": 1900000},
        {"Componente": "Motherboard ROG Strix X670E-E", "Costo": 2200000},
        {"Componente": "RAM 32GB DDR5 + Almacenamiento 2TB SSD", "Costo": 1500000},
        {"Componente": "Refrigeración Líquida ROG Ryujin III LCD", "Costo": 1600000},
        {"Componente": "Tarjeta Gráfica ROG Strix RTX Serie 40", "Costo": 4500000},
        {"Componente": "Pantalla Gamer ASUS ROG 300Hz", "Costo": 2200000}
    ]
    
    saldo_disponible = total_pc
    nombres_piezas = []
    estados = []
    
    for p in piezas:
        nombres_piezas.append(p["Componente"])
        if saldo_disponible >= p["Costo"]:
            estados.append("ADQUIRIDO")
            saldo_disponible -= p["Costo"]
        else:
            estados.append("EN RUTA DE AHORRO")
            
    df_piezas_visual = pd.DataFrame({"COMPONENTE": nombres_piezas, "ESTADO": estados})
    
    fig_piezas = px.bar(
        df_piezas_visual, 
        y="COMPONENTE", 
        x=[1]*len(df_piezas_visual), 
        color="ESTADO",
        orientation="h",
        color_discrete_map={"ADQUIRIDO": "#00FF66", "EN RUTA DE AHORRO": "#111424"},
        title="Checklist Visual de Armado Mecánico"
    )
    fig_piezas.update_layout(template="plotly_dark", showlegend=True, xaxis_visible=False, plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_piezas, use_container_width=True)

    st.subheader("📋 HISTORIAL TOTAL DE TRANSACCIONES")
    st.dataframe(df_finanzas, use_container_width=True)

# =========================================================================
# MÓDULO 3: MATRIZ DE ESTUDIO (MÉTRICAS INTELIGENTES)
# =========================================================================
elif menu == "🧠 MATRIZ DE ESTUDIO":
    st.header("🧠 Matriz de Crecimiento Intelectual")
    
    horas_totales = df_estudio['TIEMPO (MINUTOS)'].sum() / 60
    
    try:
        total_intentos = df_estudio['¿VENCÍ LA PEREZA?'].count()
        vencidas = df_estudio[df_estudio['¿VENCÍ LA PEREZA?'] == 'Sí'].shape[0]
        factor_disciplina = (vencidas / total_intentos) * 100
    except:
        factor_disciplina = 0.0

    col_e1, col_e2 = st.columns(2)
    with col_e1:
        st.metric(label="🧠 Horas de Vuelo Intelectual", value=f"{horas_totales:.1f} Hrs")
    with col_e2:
        st.metric(label="🔥 Factor de Disciplina Mental", value=f"{factor_disciplina:.1f}%")
        
    st.markdown("---")
    st.subheader("📊 Distribución de Enfoque en la Matriz")
    
    fig_pie = px.pie(
        df_estudio, 
        values='TIEMPO (MINUTOS)', 
        names='ÁREA',
        hole=0.5,
        color_discrete_sequence=['#00FF66', '#0066FF', '#FF007F']
    )
    fig_pie.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_pie, use_container_width=True)
    
    st.subheader("📝 REGISTRO DE LOGS DE APRENDIZAJE")
    st.dataframe(df_estudio, use_container_width=True)
