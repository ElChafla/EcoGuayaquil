import streamlit as st
import pandas as pd
import hashlib
import json
from datetime import datetime
import random
import time

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(
    page_title="EcoGuayaquil Reciclaje",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para simular la identidad visual del ITSO y la App
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        width: 100%;
        background-color: #2E7D32;
        color: white;
        border-radius: 10px;
        height: 3em;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        text-align: center;
    }
    h1, h2, h3 {
        color: #1B5E20;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. CLASES DEL SISTEMA (BACKEND LOGIC)
# ==========================================

# --- CLASE BLOCKCHAIN (Objetivo Específico 2: Trazabilidad y Tokens)  ---
class EcoBlock:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = str(timestamp)
        self.data = data # Aquí va la transacción (Usuario, Cantidad Botellas, Tokens)
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class EcoBlockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return EcoBlock(0, datetime.now(), "Bloque Génesis - EcoGuayaquil", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

# --- MOTOR DE GAMIFICACIÓN (Objetivo Específico 1 y Fundamentación 2.3.1)  ---
def calcular_nivel(botellas):
    if botellas < 50:
        return "🌱 Reciclador Novato", 50
    elif botellas < 150:
        return "🌿 Explorador Ambiental", 150
    elif botellas < 300:
        return "🌳 Guardián del Guayas", 300
    else:
        return "👑 Maestro del Reciclaje", 1000

# ==========================================
# 3. GESTIÓN DEL ESTADO (SESSION STATE)
# ==========================================
# Esto permite que la app recuerde los datos mientras interactúas
if 'blockchain' not in st.session_state:
    st.session_state.blockchain = EcoBlockchain()
if 'user_stats' not in st.session_state:
    st.session_state.user_stats = {
        'botellas': 0,
        'tokens': 0.0,
        'co2_ahorrado': 0.0
    }
if 'transactions' not in st.session_state:
    st.session_state.transactions = []

# ==========================================
# 4. INTERFAZ DE USUARIO (FRONTEND)
# ==========================================

# --- BARRA LATERAL (Navegación) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1598/1598196.png", width=100)
    st.title("EcoGuayaquil")
    st.markdown("Plataforma de Transformación Sostenible Urbana ")
    
    menu = st.radio("Navegación", ["🏠 Inicio", "♻️ Reciclar (IoT)", "📍 Mapa Puntos", "💰 Billetera Token", "🛒 Marketplace"])
    
    st.divider()
    st.info(f"**Estado del Sistema:**\nBloques en Cadena: {len(st.session_state.blockchain.chain)}\nValidación: {'✅ Segura' if st.session_state.blockchain.is_chain_valid() else '❌ Error'}")

# --- PÁGINA: INICIO (Dashboard Gamificado) ---
if menu == "🏠 Inicio":
    st.header("Panel del Ciudadano")
    st.markdown("Bienvenido a la gestión circular de residuos en Guayaquil.")
    
    # Datos actuales
    nivel_actual, meta_nivel = calcular_nivel(st.session_state.user_stats['botellas'])
    progreso = (st.session_state.user_stats['botellas'] / meta_nivel)
    
    # Tarjetas de Métricas (KPIs) 
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='metric-card'><h3>{st.session_state.user_stats['tokens']:.2f}</h3><p>EcoTokens (ECOG)</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><h3>{st.session_state.user_stats['botellas']}</h3><p>Botellas PET Recicladas</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-card'><h3>{st.session_state.user_stats['co2_ahorrado']:.2f} kg</h3><p>CO2 Evitado</p></div>", unsafe_allow_html=True)

    st.markdown("---")
    
    # Sección de Gamificación
    st.subheader(f"🏅 Nivel Actual: {nivel_actual}")
    st.progress(progreso)
    st.caption(f"Faltan {meta_nivel - st.session_state.user_stats['botellas']} botellas para el siguiente nivel.")
    
    if st.session_state.user_stats['botellas'] > 0:
        st.success("¡Gracias por contribuir a la sostenibilidad urbana de Guayaquil!")

# --- PÁGINA: RECICLAR (Simulación IoT) ---
elif menu == "♻️ Reciclar (IoT)":
    st.header("Punto de Acopio Inteligente")
    st.markdown("Esta sección simula la interacción con los **sensores IoT** instalados en los contenedores.")

    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 📲 Escanear QR")
        st.markdown("Acerca tu celular al contenedor para iniciar sesión.")
        
        # Simulación del proceso físico
        if st.button("Iniciar Reciclaje"):
            with st.spinner('Conectando con sensor IoT...'):
                time.sleep(1.5) # Simular latencia de red
                
                # Datos simulados del sensor (Peso y Cantidad)
                peso_detectado = round(random.uniform(0.1, 2.0), 2) # kg
                botellas_detectadas = int(peso_detectado * 20) # Aprox 20 botellas por kg
                tokens_ganados = botellas_detectadas * 0.5 # 0.5 tokens por botella
                
                # Crear transacción
                transaccion_data = {
                    "usuario": "Francisco Cevallos",
                    "accion": "Reciclaje PET",
                    "cantidad": botellas_detectadas,
                    "peso_kg": peso_detectado,
                    "tokens": tokens_ganados,
                    "ubicacion": "Sensor_ITSO_01"
                }
                
                # 1. Agregar a Blockchain
                nuevo_bloque = EcoBlock(
                    len(st.session_state.blockchain.chain), 
                    datetime.now(), 
                    transaccion_data, 
                    ""
                )
                bloque_minado = st.session_state.blockchain.add_block(nuevo_bloque)
                
                # 2. Actualizar Estado del Usuario
                st.session_state.user_stats['botellas'] += botellas_detectadas
                st.session_state.user_stats['tokens'] += tokens_ganados
                st.session_state.user_stats['co2_ahorrado'] += (peso_detectado * 1.5) # Factor conversión ficticio
                
                # 3. Guardar historial local para visualización
                st.session_state.transactions.append(transaccion_data)
                
                st.balloons()
                st.success(f"¡Reciclaje Exitoso! El sensor detectó **{botellas_detectadas} botellas** ({peso_detectado}kg).")
                st.info(f"Has ganado **{tokens_ganados} ECOG**.")
                
                with st.expander("Ver Detalles Técnicos (IoT & Blockchain)"):
                    st.json(transaccion_data)
                    st.write(f"**Hash del Bloque:** {bloque_minado.hash}")

    with col2:
        st.image("https://img.freepik.com/vector-gratis/contenedor-reciclaje-plastico-estilo-realista_23-2147828062.jpg", width=300, caption="Contenedor Inteligente con Sensores IoT")

# --- PÁGINA: MAPA (Geolocalización) ---
elif menu == "📍 Mapa Puntos":
    st.header("Red de Puntos Limpios en Guayaquil")
    st.markdown("Ubicación de los contenedores inteligentes aliados[cite: 133].")
    
    # Coordenadas reales aproximadas de Guayaquil
    puntos_acopio = pd.DataFrame({
        'lat': [-2.1894, -2.1450, -2.1980],
        'lon': [-79.8891, -79.9000, -79.8950],
        'nombre': ['Malecón 2000', 'Parque Samanes', 'ITSO (Campus)']
    })
    
    st.map(puntos_acopio, zoom=12)
    
    st.table(puntos_acopio)

# --- PÁGINA: BILLETERA (Ledger Blockchain) ---
elif menu == "💰 Billetera Token":
    st.header("Billetera EcoToken (Blockchain Ledger)")
    st.markdown("Registro inmutable y transparente de todas tus transacciones.")
    
    st.metric(label="Saldo Disponible", value=f"{st.session_state.user_stats['tokens']:.2f} ECOG")
    
    st.subheader("Explorador de Bloques")
    
    if len(st.session_state.blockchain.chain) > 1:
        # Convertir la cadena de bloques a un formato legible para tabla
        chain_data = []
        for block in st.session_state.blockchain.chain:
            chain_data.append({
                "Índice": block.index,
                "Timestamp": block.timestamp,
                "Datos": str(block.data),
                "Hash Actual": block.hash[:15] + "...", # Recortado para visualización
                "Hash Anterior": block.previous_hash[:15] + "..."
            })
        
        df_chain = pd.DataFrame(chain_data)
        st.dataframe(df_chain, use_container_width=True)
    else:
        st.info("Aún no hay transacciones. Ve a la sección 'Reciclar' para generar tu primer bloque.")

# --- PÁGINA: MARKETPLACE (Economía Circular) ---
elif menu == "🛒 Marketplace":
    st.header("Canje de Recompensas")
    st.markdown("Utiliza tus EcoTokens en comercios locales aliados[cite: 133].")
    
    col1, col2, col3 = st.columns(3)
    
    premios = [
        {"nombre": "Pasaje Metrovía", "costo": 3.0, "icon": "🚌"},
        {"nombre": "Cupón Sweet & Coffee", "costo": 10.0, "icon": "☕"},
        {"nombre": "Descuento Mi Comisariato", "costo": 20.0, "icon": "🛒"}
    ]
    
    for i, premio in enumerate(premios):
        with [col1, col2, col3][i]:
            st.markdown(f"<div class='metric-card'><h1>{premio['icon']}</h1><h3>{premio['nombre']}</h3><p style='color:green; font-weight:bold;'>{premio['costo']} ECOG</p></div>", unsafe_allow_html=True)
            
            if st.button(f"Canjear {premio['nombre']}", key=f"btn_{i}"):
                if st.session_state.user_stats['tokens'] >= premio['costo']:
                    # Descontar tokens
                    st.session_state.user_stats['tokens'] -= premio['costo']
                    # Registrar transacción de gasto en blockchain
                    tx_gasto = {"usuario": "Francisco", "accion": f"Canje: {premio['nombre']}", "costo": -premio['costo']}
                    nuevo_bloque = EcoBlock(len(st.session_state.blockchain.chain), datetime.now(), tx_gasto, "")
                    st.session_state.blockchain.add_block(nuevo_bloque)
                    
                    st.success(f"¡Canjeaste {premio['nombre']} exitosamente!")
                    st.balloons()
                else:
                    st.error("Saldo insuficiente para este premio.")

# Pie de página
st.markdown("---")
st.caption("Desarrollado para el Trabajo de Titulación de Maestría en Herramientas Digitales - ITSO [cite: 1]")