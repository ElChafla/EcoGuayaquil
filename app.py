import streamlit as st
import pandas as pd
import hashlib
import time
import random
from datetime import datetime

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA (CORREGIDO)
# ==========================================
st.set_page_config(
    page_title="EcoGuayaquil App",
    page_icon="♻️",
    layout="centered", # CORREGIDO: "centered" simula mejor la vista móvil
    initial_sidebar_state="collapsed"
)

# Estilos CSS para que parezca App Móvil
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
    }
    .main-header {
        background-color: #2E7D32;
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-box {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        background-color: #2E7D32;
        color: white;
        border-radius: 20px;
        height: 50px;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1B5E20;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. LÓGICA DEL SISTEMA (BACKEND)
# ==========================================

# CLASE BLOCKCHAIN
class EcoBlock:
    def __init__(self, index, transaction, prev_hash):
        self.index = index
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transaction = transaction
        self.prev_hash = prev_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.transaction}{self.prev_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

# GESTIÓN DE ESTADO (Memoria de la App)
if 'chain' not in st.session_state:
    genesis = EcoBlock(0, "Genesis Block", "0")
    st.session_state.chain = [genesis]

if 'user' not in st.session_state:
    st.session_state.user = {
        'name': 'Francisco Cevallos',
        'tokens': 12.50,
        'botellas': 120,
        'nivel': 'Explorador'
    }

# ==========================================
# 3. INTERFAZ DE USUARIO (FRONTEND)
# ==========================================

# ENCABEZADO
st.markdown(f"""
    <div class="main-header">
        <h3 style="margin:0;">EcoGuayaquil</h3>
        <p style="margin:5px 0; opacity:0.9;">Hola, {st.session_state.user['name']}</p>
        <h2 style="margin:0;">💰 {st.session_state.user['tokens']:.2f} ECOG</h2>
    </div>
    """, unsafe_allow_html=True)

# MENÚ
menu = st.selectbox("Navegación", ["🏠 Inicio", "📡 Escanear (IoT)", "📍 Mapa", "🛒 Canjear", "🔗 Blockchain"])

# --- PANTALLA 1: INICIO ---
if menu == "🏠 Inicio":
    st.subheader("Tu Progreso")
    
    # Datos
    nivel = st.session_state.user['nivel']
    botellas = st.session_state.user['botellas']
    prox_nivel = 200
    progreso = min(botellas / prox_nivel, 1.0)
    
    st.info(f"🏅 Nivel Actual: **{nivel}**")
    st.progress(progreso, text=f"{botellas}/{prox_nivel} Botellas")
    
    # Métricas
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"<div class='metric-box'><h2 style='color:#2E7D32'>{botellas}</h2><p>Botellas</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='metric-box'><h2 style='color:#1565C0'>{botellas*0.02:.1f}kg</h2><p>CO2 Ahorrado</p></div>", unsafe_allow_html=True)

# --- PANTALLA 2: ESCANEAR (IoT) ---
elif menu == "📡 Escanear (IoT)":
    st.subheader("Punto de Reciclaje Inteligente")
    st.info("Simulación de conexión con hardware IoT")
    
    if st.button("📲 SIMULAR ESCANEO Y DEPÓSITO"):
        with st.spinner("Conectando con sensores..."):
            time.sleep(1.5) 
            
            nuevas = random.randint(5, 15)
            recompensa = nuevas * 0.50
            
            # Actualizar Estado
            st.session_state.user['botellas'] += nuevas
            st.session_state.user['tokens'] += recompensa
            
            if st.session_state.user['botellas'] > 200:
                st.session_state.user['nivel'] = "Guardián del Guayas"
            
            # Blockchain
            tx = f"Reciclaje: {nuevas} botellas"
            prev = st.session_state.chain[-1]
            new_block = EcoBlock(len(st.session_state.chain), tx, prev.hash)
            st.session_state.chain.append(new_block)
            
            st.success(f"¡Reciclaje Exitoso! +{nuevas} botellas")
            st.balloons()

# --- PANTALLA 3: MAPA ---
elif menu == "📍 Mapa":
    st.subheader("Puntos de Acopio")
    
    data = pd.DataFrame({
        'lat': [-2.1894, -2.1450, -2.1980],
        'lon': [-79.8891, -79.9000, -79.8950],
        'name': ['Malecón', 'Samanes', 'ITSO']
    })
    
    st.map(data, zoom=11)
    st.caption("Puntos activos en Guayaquil")

# --- PANTALLA 4: CANJE ---
elif menu == "🛒 Canjear":
    st.subheader("Marketplace")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='metric-box'><h3>🚌</h3><p><b>Metrovia</b><br>3.00 ECOG</p></div>", unsafe_allow_html=True)
        if st.button("Canjear Metro"):
            if st.session_state.user['tokens'] >= 3:
                st.session_state.user['tokens'] -= 3
                prev = st.session_state.chain[-1]
                st.session_state.chain.append(EcoBlock(len(st.session_state.chain), "Canje: Metrovia", prev.hash))
                st.success("¡Canjeado!")
            else:
                st.error("Saldo insuficiente")

    with col2:
        st.markdown("<div class='metric-box'><h3>☕</h3><p><b>Café</b><br>8.00 ECOG</p></div>", unsafe_allow_html=True)
        if st.button("Canjear Café"):
            if st.session_state.user['tokens'] >= 8:
                st.session_state.user['tokens'] -= 8
                prev = st.session_state.chain[-1]
                st.session_state.chain.append(EcoBlock(len(st.session_state.chain), "Canje: Café", prev.hash))
                st.success("¡Disfruta!")
            else:
                st.error("Saldo insuficiente")

# --- PANTALLA 5: BLOCKCHAIN ---
elif menu == "🔗 Blockchain":
    st.subheader("Ledger Inmutable")
    
    if len(st.session_state.chain) > 0:
        chain_data = []
        for b in st.session_state.chain:
            chain_data.append({
                "Index": b.index,
                "Tx": b.transaction,
                "Hash": b.hash[:10] + "...",
                "Time": b.timestamp
            })
        st.dataframe(pd.DataFrame(chain_data))
