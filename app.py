import streamlit as st
import pandas as pd
import hashlib
import time
import random
from datetime import datetime
from streamlit_option_menu import option_menu # Librería para los íconos

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(
    page_title="EcoGuayaquil",
    page_icon="♻️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS para ocultar elementos de Streamlit y dar look de App
st.markdown("""
    <style>
    /* Ocultar menú hamburguesa y footer de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Estilo del contenedor principal */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Tarjeta de métricas */
    .metric-card {
        background-color: white;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        text-align: center;
        margin-bottom: 10px;
    }
    
    /* Botones grandes */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 50px;
        font-weight: 600;
        background-color: #2E7D32;
        color: white;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #1B5E20;
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. BACKEND (Lógica y Blockchain)
# ==========================================

class EcoBlock:
    def __init__(self, index, transaction, prev_hash):
        self.index = index
        self.timestamp = datetime.now().strftime("%H:%M:%S")
        self.transaction = transaction
        self.prev_hash = prev_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.transaction}{self.prev_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

if 'chain' not in st.session_state:
    st.session_state.chain = [EcoBlock(0, "Genesis", "0")]

if 'user' not in st.session_state:
    st.session_state.user = {
        'name': 'Francisco',
        'tokens': 12.50,
        'botellas': 120,
        'nivel': 'Explorador'
    }

# ==========================================
# 3. BARRA DE NAVEGACIÓN (ICONOS)
# ==========================================

# Menú horizontal con iconos (Simula App Móvil)
selected = option_menu(
    menu_title=None,  # Ocultamos el título del menú
    options=["Inicio", "Escanear", "Mapa", "Canjear", "Wallet"], # Las 5 opciones
    icons=["house-fill", "upc-scan", "geo-alt-fill", "bag-fill", "hdd-network"], # Iconos de Bootstrap
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#ffffff", "border-radius": "0"},
        "icon": {"color": "#2E7D32", "font-size": "18px"}, 
        "nav-link": {"font-size": "12px", "text-align": "center", "margin": "0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#2E7D32", "color": "white"},
    }
)

# ==========================================
# 4. PANTALLAS (VISTAS)
# ==========================================

# --- PANTALLA INICIO ---
if selected == "Inicio":
    st.markdown(f"### Hola, {st.session_state.user['name']} 👋")
    
    # Tarjeta de Saldo Principal
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #2E7D32 0%, #66BB6A 100%); padding: 20px; border-radius: 15px; color: white; margin-bottom: 20px; text-align: center;">
        <small style="opacity: 0.8">Saldo Disponible</small>
        <h1 style="margin: 0;">{st.session_state.user['tokens']:.2f} ECOG</h1>
        <small>Nivel: {st.session_state.user['nivel']}</small>
    </div>
    """, unsafe_allow_html=True)

    # Progreso
    botellas = st.session_state.user['botellas']
    st.progress(min(botellas/200, 1.0), text=f"Meta Nivel: {botellas}/200 Botellas")
    
    c1, c2 = st.columns(2)
    c1.markdown(f"<div class='metric-card'><h3>♻️ {botellas}</h3><small>Recicladas</small></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='metric-card'><h3>🌳 {botellas*0.03:.1f}kg</h3><small>CO2 Ahorrado</small></div>", unsafe_allow_html=True)

# --- PANTALLA ESCANEAR (IoT) ---
elif selected == "Escanear":
    st.subheader("📡 Conexión IoT")
    st.info("Acércate a un contenedor inteligente")
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/3415/3415054.png", width=150)
    
    if st.button("SIMULAR DEPÓSITO"):
        with st.spinner("Leyendo sensores de peso..."):
            time.sleep(1.5)
            cant = random.randint(3, 12)
            puntos = cant * 0.5
            
            # Update Logic
            st.session_state.user['botellas'] += cant
            st.session_state.user['tokens'] += puntos
            
            # Blockchain
            prev = st.session_state.chain[-1]
            block = EcoBlock(len(st.session_state.chain), f"Reciclaje: {cant} PET", prev.hash)
            st.session_state.chain.append(block)
            
            st.balloons()
            st.success(f"¡Procesado! +{cant} Botellas (+{puntos} ECOG)")

# --- PANTALLA MAPA ---
elif selected == "Mapa":
    st.subheader("📍 Puntos Cercanos")
    # Data de Guayaquil
    map_data = pd.DataFrame({
        'lat': [-2.1894, -2.1450, -2.1500, -2.1980],
        'lon': [-79.8891, -79.9000, -79.8900, -79.8950],
        'color': ['#2E7D32', '#2E7D32', '#FF0000', '#2E7D32'] # Verde activos, Rojo lleno
    })
    st.map(map_data, zoom=12, color='color')
    st.caption("🟢 Disponibles | 🔴 Llenos")
    
    with st.expander("Ver lista de ubicaciones"):
        st.write("- Malecón 2000 (Activo)")
        st.write("- Parque Samanes (Activo)")
        st.write("- ITSO Campus (Activo)")
        st.write("- Plaza Lagos (Lleno)")

# --- PANTALLA CANJEAR ---
elif selected == "Canjear":
    st.subheader("🛒 Marketplace")
    st.caption("Usa tus tokens en comercios aliados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='metric-card'><h1>🚌</h1><h4>Metrovía</h4><p style='color:green'>3.00 ECOG</p></div>", unsafe_allow_html=True)
        if st.button("Canjear Pasaje"):
            if st.session_state.user['tokens'] >= 3:
                st.session_state.user['tokens'] -= 3
                st.session_state.chain.append(EcoBlock(len(st.session_state.chain), "Canje: Metro", st.session_state.chain[-1].hash))
                st.success("¡Código QR Generado!")
            else:
                st.error("Saldo insuficiente")
                
    with col2:
        st.markdown("<div class='metric-card'><h1>☕</h1><h4>Café</h4><p style='color:green'>8.00 ECOG</p></div>", unsafe_allow_html=True)
        if st.button("Canjear Café"):
            if st.session_state.user['tokens'] >= 8:
                st.session_state.user['tokens'] -= 8
                st.session_state.chain.append(EcoBlock(len(st.session_state.chain), "Canje: Café", st.session_state.chain[-1].hash))
                st.success("¡Disfruta!")
            else:
                st.error("Saldo insuficiente")

# --- PANTALLA WALLET (BLOCKCHAIN) ---
elif selected == "Wallet":
    st.subheader("🔗 Blockchain Ledger")
    st.caption("Registro inmutable de transacciones")
    
    if len(st.session_state.chain) > 0:
        for block in reversed(st.session_state.chain):
            st.markdown(f"""
            <div style="background: white; padding: 10px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #2E7D32; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                <small style="color: #888">Bloque #{block.index} | {block.timestamp}</small><br>
                <b>{block.transaction}</b><br>
                <small style="font-family: monospace; color: #666; font-size: 8px;">Hash: {block.hash}</small>
            </div>
            """, unsafe_allow_html=True)
