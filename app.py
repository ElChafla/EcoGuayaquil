import streamlit as st
import pandas as pd
import hashlib
import time
import random
from datetime import datetime
from streamlit_option_menu import option_menu 

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(
    page_title="EcoGuayaquil",
    page_icon="♻️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS
st.markdown("""
    <style>
    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Estilo General */
    .stApp {background-color: #f8f9fa;}
    
    /* Tarjetas */
    .metric-card {
        background-color: white;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        text-align: center;
        margin-bottom: 10px;
    }
    
    /* Botones */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 50px;
        font-weight: 600;
        background-color: #2E7D32;
        color: white;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1B5E20;
        transform: scale(1.01);
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. BACKEND (Lógica y Blockchain)
# ==========================================

class EcoBlock:
    def __init__(self, index, transaction, amount, prev_hash):
        self.index = index
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transaction = transaction
        self.amount = amount # Guardamos el monto para graficar
        self.prev_hash = prev_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # Hash único basado en contenido
        block_string = f"{self.index}{self.timestamp}{self.transaction}{self.amount}{self.prev_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

# Inicialización de Estado
if 'chain' not in st.session_state:
    # Bloque Génesis (Saldo inicial)
    genesis = EcoBlock(0, "Saldo Inicial", 12.50, "0")
    st.session_state.chain = [genesis]

if 'user' not in st.session_state:
    st.session_state.user = {
        'name': 'Francisco',
        'tokens': 12.50,
        'botellas': 120,
        'nivel': 'Explorador'
    }

# ==========================================
# 3. BARRA DE NAVEGACIÓN
# ==========================================
selected = option_menu(
    menu_title=None,
    options=["Inicio", "Escanear", "Mapa", "Canjear", "Wallet"],
    icons=["house-fill", "upc-scan", "geo-alt-fill", "bag-fill", "wallet2"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fff"},
        "icon": {"color": "#2E7D32", "font-size": "16px"}, 
        "nav-link": {"font-size": "11px", "text-align": "center", "margin": "0px"},
        "nav-link-selected": {"background-color": "#2E7D32", "color": "white"},
    }
)

# ==========================================
# 4. PANTALLAS
# ==========================================

# --- INICIO ---
if selected == "Inicio":
    st.markdown(f"### Hola, {st.session_state.user['name']} 👋")
    
    # Tarjeta de Saldo Principal
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #2E7D32 0%, #66BB6A 100%); padding: 25px; border-radius: 15px; color: white; margin-bottom: 20px; text-align: center; box-shadow: 0 4px 15px rgba(46, 125, 50, 0.3);">
        <small style="opacity: 0.9">Saldo Disponible</small>
        <h1 style="margin: 5px 0; font-size: 36px;">{st.session_state.user['tokens']:.2f} ECOG</h1>
        <div style="background: rgba(255,255,255,0.2); display: inline-block; padding: 2px 10px; border-radius: 10px;">
            <small>Nivel: {st.session_state.user['nivel']}</small>
        </div>
    </div>
    """, unsafe_allow_html=True)

    botellas = st.session_state.user['botellas']
    st.progress(min(botellas/200, 1.0), text=f"Meta: {botellas}/200 Botellas")
    
    c1, c2 = st.columns(2)
    c1.markdown(f"<div class='metric-card'><h3>♻️ {botellas}</h3><small>Recicladas</small></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='metric-card'><h3>🌳 {botellas*0.03:.1f}kg</h3><small>CO2 Ahorrado</small></div>", unsafe_allow_html=True)

# --- ESCANEAR (IoT) ---
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
            
            # Actualizar Estado
            st.session_state.user['botellas'] += cant
            st.session_state.user['tokens'] += puntos
            
            # Blockchain: Crear bloque
            prev = st.session_state.chain[-1]
            block = EcoBlock(len(st.session_state.chain), f"Reciclaje: {cant} PET", puntos, prev.hash)
            st.session_state.chain.append(block)
            
            st.balloons()
            st.success(f"¡Procesado! +{cant} Botellas (+{puntos} ECOG)")

# --- MAPA ---
elif selected == "Mapa":
    st.subheader("📍 Puntos Cercanos")
    map_data = pd.DataFrame({
        'lat': [-2.1894, -2.1450, -2.1500, -2.1980],
        'lon': [-79.8891, -79.9000, -79.8900, -79.8950],
        'color': ['#2E7D32', '#2E7D32', '#FF0000', '#2E7D32']
    })
    st.map(map_data, zoom=12, color='color')
    st.caption("🟢 Disponibles | 🔴 Llenos")

# --- CANJEAR ---
elif selected == "Canjear":
    st.subheader("🛒 Marketplace")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='metric-card'><h1>🚌</h1><h4>Metrovía</h4><p style='color:green'>3.00 ECOG</p></div>", unsafe_allow_html=True)
        if st.button("Canjear Pasaje"):
            if st.session_state.user['tokens'] >= 3:
                st.session_state.user['tokens'] -= 3
                # Blockchain
                prev = st.session_state.chain[-1]
                st.session_state.chain.append(EcoBlock(len(st.session_state.chain), "Canje: Metro", -3.00, prev.hash))
                st.success("¡Código QR Generado!")
            else:
                st.error("Saldo insuficiente")
                
    with col2:
        st.markdown("<div class='metric-card'><h1>☕</h1><h4>Café</h4><p style='color:green'>8.00 ECOG</p></div>", unsafe_allow_html=True)
        if st.button("Canjear Café"):
            if st.session_state.user['tokens'] >= 8:
                st.session_state.user['tokens'] -= 8
                # Blockchain
                prev = st.session_state.chain[-1]
                st.session_state.chain.append(EcoBlock(len(st.session_state.chain), "Canje: Café", -8.00, prev.hash))
                st.success("¡Disfruta!")
            else:
                st.error("Saldo insuficiente")

# --- WALLET (MEJORADA) ---
elif selected == "Wallet":
    st.subheader("🔗 Billetera Blockchain")
    
    # 1. Gráfico de Balance (Evolución)
    st.markdown("##### 📈 Evolución de Saldo")
    
    # Extraemos datos para el gráfico
    chart_data = []
    saldo_acumulado = 0
    for block in st.session_state.chain:
        saldo_acumulado += block.amount if block.index > 0 else 12.50 # Ajuste para saldo inicial
        chart_data.append({"Bloque": block.index, "Saldo": saldo_acumulado})
    
    st.line_chart(pd.DataFrame(chart_data).set_index("Bloque"))

    # 2. Tabla de Transacciones (Ledger)
    st.markdown("##### 📜 Libro Mayor Inmutable (Ledger)")
    
    if len(st.session_state.chain) > 0:
        # Preparamos DataFrame
        chain_data = []
        for block in reversed(st.session_state.chain): # Orden inverso: más reciente primero
            chain_data.append({
                "ID": block.index,
                "Fecha": block.timestamp,
                "Detalle": block.transaction,
                "Monto": f"{block.amount:+.2f}",
                "Hash": block.hash
            })
        
        df = pd.DataFrame(chain_data)
        
        # Mostramos DataFrame interactivo
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Hash": st.column_config.TextColumn("Hash (Huella Digital)", help="Identificador único del bloque", width="small"),
                "Monto": st.column_config.TextColumn("EcoTokens", width="small"),
            }
        )
        
        # Botón de Descarga
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Descargar Historial (CSV)",
            data=csv,
            file_name="ecoguayaquil_ledger.csv",
            mime="text/csv",
        )
