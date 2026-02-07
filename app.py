import streamlit as st
import pandas as pd
import hashlib
import time
import random
from datetime import datetime

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA Y ESTILO
# ==========================================
st.set_page_config(
    page_title="EcoGuayaquil App",
    page_icon="♻️",
    layout="mobile", # Simula vista de celular
    initial_sidebar_state="collapsed"
)

# Estilo visual (Verde Ecológico y Amarillo ITSO)
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
    }
    .main-header {
        background-color: #2E7D32;
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    .metric-box {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        background-color: #2E7D32;
        color: white;
        border-radius: 20px;
        height: 50px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# LÓGICA DEL SISTEMA (BACKEND)
# ==========================================

# 1. CLASE BLOCKCHAIN (Objetivo Específico 2)
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

# 2. GESTIÓN DE ESTADO (Memoria de la App)
if 'chain' not in st.session_state:
    # Bloque Génesis
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
# INTERFAZ DE USUARIO (FRONTEND)
# ==========================================

# --- ENCABEZADO TIPO APP MÓVIL ---
st.markdown(f"""
    <div class="main-header">
        <h3>EcoGuayaquil</h3>
        <p>Hola, {st.session_state.user['name']}</p>
        <h2>💰 {st.session_state.user['tokens']:.2f} ECOG</h2>
    </div>
    """, unsafe_allow_html=True)

# --- MENÚ DE NAVEGACIÓN ---
menu = st.selectbox("Ir a:", ["🏠 Inicio", "📡 Escanear (IoT)", "📍 Mapa", "🛒 Canjear", "🔗 Blockchain"])

# --- PANTALLA 1: INICIO (Gamificación) ---
if menu == "🏠 Inicio":
    st.subheader("Tu Progreso")
    
    # Barra de Nivel
    nivel = st.session_state.user['nivel']
    botellas = st.session_state.user['botellas']
    prox_nivel = 200
    progreso = min(botellas / prox_nivel, 1.0)
    
    st.info(f"🏅 Nivel Actual: **{nivel}**")
    st.progress(progreso)
    st.caption(f"Faltan {prox_nivel - botellas} botellas para el siguiente nivel.")
    
    # Métricas
    c1, c2 = st.columns(2)
    c1.markdown(f"<div class='metric-box'><h1>{botellas}</h1><p>Botellas</p></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='metric-box'><h1>{botellas*0.02:.1f}kg</h1><p>CO2 Ahorrado</p></div>", unsafe_allow_html=True)

# --- PANTALLA 2: ESCANEAR (Simulación IoT) ---
elif menu == "📡 Escanear (IoT)":
    st.subheader("Punto de Reciclaje Inteligente")
    st.image("https://cdn-icons-png.flaticon.com/512/3362/3362708.png", width=100)
    st.write("Acerca tu celular al contenedor para iniciar.")
    
    if st.button("📲 SIMULAR ESCANEO Y DEPÓSITO"):
        with st.spinner("Conectando con sensores IoT..."):
            time.sleep(2) # Simular tiempo de proceso
            
            # Datos aleatorios simulados del sensor
            nuevas_botellas = random.randint(5, 15)
            peso = round(nuevas_botellas * 0.03, 2)
            recompensa = nuevas_botellas * 0.50
            
            # Actualizar Usuario
            st.session_state.user['botellas'] += nuevas_botellas
            st.session_state.user['tokens'] += recompensa
            
            # Actualizar Nivel (Gamificación)
            if st.session_state.user['botellas'] > 200:
                st.session_state.user['nivel'] = "Guardián del Guayas"
            
            # Registrar en Blockchain
            tx = f"Reciclaje: {nuevas_botellas} botellas en ITSO"
            prev_block = st.session_state.chain[-1]
            new_block = EcoBlock(len(st.session_state.chain), tx, prev_block.hash)
            st.session_state.chain.append(new_block)
            
            st.success(f"¡Éxito! Reciclaste {nuevas_botellas} botellas ({peso}kg)")
            st.balloons()

# --- PANTALLA 3: MAPA (Geolocalización) ---
elif menu == "📍 Mapa":
    st.subheader("Puntos de Acopio en Guayaquil")
    
    # Coordenadas reales
    data = pd.DataFrame({
        'lat': [-2.1894, -2.1450, -2.1980],
        'lon': [-79.8891, -79.9000, -79.8950],
        'nombre': ['Malecón 2000', 'Parque Samanes', 'ITSO']
    })
    
    st.map(data, zoom=12)
    st.caption("Los puntos rojos indican contenedores con sensores activos.")

# --- PANTALLA 4: CANJE (Economía Circular) ---
elif menu == "🛒 Canjear":
    st.subheader("Marketplace")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("🚌 **Metrovía**\n\nCosto: 3.00 ECOG")
        if st.button("Canjear Metro"):
            if st.session_state.user['tokens'] >= 3:
                st.session_state.user['tokens'] -= 3
                # Registro en Blockchain
                prev = st.session_state.chain[-1]
                blk = EcoBlock(len(st.session_state.chain), "Canje: Pasaje Metrovía", prev.hash)
                st.session_state.chain.append(blk)
                st.success("¡Canjeado!")
            else:
                st.error("Saldo insuficiente")

    with col2:
        st.warning("☕ **Café**\n\nCosto: 8.00 ECOG")
        if st.button("Canjear Café"):
            if st.session_state.user['tokens'] >= 8:
                st.session_state.user['tokens'] -= 8
                prev = st.session_state.chain[-1]
                blk = EcoBlock(len(st.session_state.chain), "Canje: Café", prev.hash)
                st.session_state.chain.append(blk)
                st.success("¡Disfruta tu café!")
            else:
                st.error("Saldo insuficiente")

# --- PANTALLA 5: BLOCKCHAIN (Trazabilidad) ---
elif menu == "🔗 Blockchain":
    st.subheader("Libro Mayor Inmutable")
    st.write("Cada transacción queda registrada criptográficamente.")
    
    if len(st.session_state.chain) > 0:
        # Convertir a DataFrame para mostrar bonito
        chain_data = []
        for b in st.session_state.chain:
            chain_data.append({
                "Index": b.index,
                "Transacción": b.transaction,
                "Hash": b.hash[:15] + "...", # Mostrar solo inicio del hash
                "Timestamp": b.timestamp
            })
        st.dataframe(pd.DataFrame(chain_data))
    else:
        st.write("Cadena vacía.")