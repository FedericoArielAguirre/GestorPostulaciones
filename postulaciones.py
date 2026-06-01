import os
import pandas as pd
import streamlit as st
from datetime import datetime
from pathlib import Path

# ─── CONFIGURACIÓN DE LA PÁGINA ──────────────────────────────────────────────
st.set_page_config(page_title="Gestor de Postulaciones", page_icon="💼", layout="wide")

# ─── INYECCIÓN DE CSS Y ESTILOS (BASADO EN TU FORMATO.TXT) ───────────────────
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:ital,wght@0,400;0,500;1,400&family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,700;0,9..144,900;1,9..144,400&display=swap');

:root {
  --bg: #f5f1eb;
  --ink: #1a1410;
  --ink2: #3d352c;
  --muted: #9a8e82;
  --border: #d9d0c4;
  --surface: #ede8e0;
  --surface2: #e5dfd5;

  --red:    #c0392b;
  --orange: #d4590f;
  --teal:   #1a7a6e;
  --blue:   #1a4f8a;
  --purple: #5c3d8f;
  --green:  #2a6b3c;
}

/* Base de la aplicación */
.stApp {
  background: var(--bg);
  color: var(--ink);
  font-family: 'Fraunces', Georgia, serif;
}

/* Ruido de fondo SVG */
.stApp::before {
  content:'';
  position:fixed; inset:0; z-index:-1; pointer-events:none;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
  background-size: 200px 200px;
}

/* Tipografía general: SE ELIMINÓ 'span' DE ESTA LISTA */
h1, h2, h3, p, li {
    font-family: 'Fraunces', Georgia, serif !important;
    color: var(--ink);
}

/* Ajustes del contenedor principal de Streamlit */
.block-container {
    max-width: 1000px;
    padding-top: 2rem !important;
    padding-bottom: 6rem !important;
}

/* Sidebar: SE ELIMINÓ 'span' DE ESTE SELECTOR */
[data-testid="stSidebar"] {
  background-color: var(--ink);
  color: #a09888;
}
[data-testid="stSidebar"] p {
    font-family: 'DM Mono', monospace !important;
    color: #e5dfd5 !important;
    font-size: 0.85rem !important;
}
[data-testid="stSidebarNav"] { display: none; } 

/* Título de Sidebar */
[data-testid="stSidebar"] h1 {
    font-family: 'Fraunces', Georgia, serif !important;
    color: var(--bg) !important;
    font-size: 1.5rem !important;
    font-style: italic;
    border-bottom: 1px solid #3a342c;
    padding-bottom: 1rem;
    margin-bottom: 1rem;
}

/* ── COMPONENTES PERSONALIZADOS DEL TEMPLATE ── */
.custom-header {
  position: relative;
  padding: 1rem 0 2.5rem;
  border-bottom: 2px solid var(--ink);
  margin-bottom: 3rem;
}
.clase-num {
  font-family: 'DM Mono', monospace !important;
  font-size: 0.7rem;
  letter-spacing: .25em;
  text-transform: uppercase;
  color: var(--blue) !important;
  margin-bottom: .7rem;
  display: flex;
  gap: 1.5rem;
  align-items: center;
}
.clase-num::before {
  content: '';
  display: inline-block;
  width: 32px; height: 2px;
  background: var(--blue);
}
.custom-h1 {
  font-size: clamp(2.4rem, 5vw, 4rem) !important;
  font-weight: 900 !important;
  line-height: .95 !important;
  letter-spacing: -.03em !important;
  font-style: italic !important;
  margin: 0 !important;
}
.header-tag {
  display: inline-block;
  border: 1px solid var(--border);
  padding: .2rem .7rem;
  border-radius: 2px;
  font-family: 'DM Mono', monospace !important;
  font-size: .65rem;
  color: var(--muted) !important;
  margin-top: 1.2rem;
  text-transform: uppercase;
  letter-spacing: .12em;
}
.sec-label {
  font-family: 'DM Mono', monospace !important;
  font-size: .62rem; letter-spacing: .25em;
  text-transform: uppercase; margin-bottom: .6rem;
  display: flex; align-items: center; gap: .8rem;
}
.sec-label.blue { color: var(--blue) !important; }
.sec-label.teal { color: var(--teal) !important; }
.sec-label.orange { color: var(--orange) !important; }
.sec-label.red { color: var(--red) !important; }
.sec-label::after { content:''; flex:1; height:1px; background: currentColor; opacity:.25; }

/* ── MODIFICADORES DE STREAMLIT ── */
/* Etiquetas de Inputs */
.stTextInput label, .stSelectbox label {
    font-family: 'DM Mono', monospace !important;
    font-size: .65rem !important;
    letter-spacing: .15em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
}

/* Inputs y Selectboxes */
[data-baseweb="input"] input, [data-baseweb="select"] div {
    background-color: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--ink) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
}

/* Botones */
.stButton > button, .stFormSubmitButton > button {
    background-color: var(--blue) !important;
    color: var(--bg) !important;
    border: none !important;
    font-family: 'DM Mono', monospace !important;
    font-size: .7rem !important;
    text-transform: uppercase !important;
    letter-spacing: .1em !important;
    padding: .55rem 1.4rem !important;
    border-radius: 2px !important;
    transition: background .2s !important;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    background-color: var(--ink) !important;
}

/* Métricas (Tarjetas de números) */
[data-testid="stMetricValue"] {
    font-family: 'Fraunces', serif !important;
    font-style: italic;
    color: var(--ink) !important;
    font-size: 3rem !important;
    font-weight: 700 !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'DM Mono', monospace !important;
    font-size: .65rem !important;
    letter-spacing: .1em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
}

/* Alertas y Callouts */
[data-testid="stAlert"] {
    background-color: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    color: var(--ink2) !important;
}
[data-testid="stAlert"] * {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
}

/* Dataframes */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 4px;
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ─── FUNCIÓN PARA RENDERIZAR ENCABEZADOS ESTILIZADOS ─────────────────────────
def render_header(clase_txt, titulo, tags):
    st.markdown(f"""
    <div class="custom-header">
        <div class="clase-num">{clase_txt}</div>
        <h1 class="custom-h1">{titulo}</h1>
        <div class="header-tag">{tags}</div>
    </div>
    """, unsafe_allow_html=True)

def render_section(titulo, color="blue"):
    st.markdown(f'<div class="sec-label {color}">{titulo}</div>', unsafe_allow_html=True)


# ─── CONFIGURACIÓN DE DATOS (Misma lógica que antes) ─────────────────────────
LOCAL_DIR = Path(__file__).parent

CSV_FILES = {
    "bumeran": "postulaciones_bumeran.csv",
    "indeed": "postulaciones_indeed.csv",
    "zonajobs": "postulaciones_zonajobs.csv",
    "computrabajo": "postulaciones_computrabajo.csv",
}

SCHEMA = {
    "bumeran": {
        "columns": ["Puesto", "Empresa", "Estado", "Fecha de Postulación", "Publicación"],
        "estado": "Estado", "puesto": "Puesto", "empresa": "Empresa", "fecha": "Fecha de Postulación",
        "estados_validos": ["CV enviado", "CV leído", "Aviso finalizado", "En proceso", "Entrevista", "No seleccionado"],
    },
    "indeed": {
        "columns": ["Estado de Postulación", "Puesto", "Empresa", "Ubicación", "Fecha/Detalle", "Aviso Caducado"],
        "estado": "Estado de Postulación", "puesto": "Puesto", "empresa": "Empresa", "fecha": "Fecha/Detalle",
        "estados_validos": ["Postulación enviada", "Postulación vista", "La empresa no te seleccionó", "En proceso", "Entrevista"],
    },
    "zonajobs": {
        "columns": ["Puesto", "Empresa", "Estado", "Fecha de Postulación", "Publicación"],
        "estado": "Estado", "puesto": "Puesto", "empresa": "Empresa", "fecha": "Fecha de Postulación",
        "estados_validos": ["CV enviado", "CV leído", "Aviso finalizado", "En proceso", "Entrevista", "No seleccionado"],
    },
    "computrabajo": {
        "columns": ["Puesto", "Empresa", "Puntuación empresa", "Ubicación", "Estado postulación", "Fecha", "Candidatos", "URL aviso"],
        "estado": "Estado postulación", "puesto": "Puesto", "empresa": "Empresa", "fecha": "Fecha",
        "estados_validos": ["Postulado", "CV Visto", "En proceso", "Proceso finalizado", "Entrevista", "No seleccionado"],
    },
}

PLATFORM_DISPLAY = {
    "bumeran": "Bumeran",
    "indeed": "Indeed",
    "zonajobs": "ZonaJobs",
    "computrabajo": "Computrabajo",
}

def get_path(platform): return LOCAL_DIR / CSV_FILES[platform]

def load_data(platform):
    path = get_path(platform)
    schema_cols = SCHEMA[platform]["columns"]
    if path.exists():
        try:
            df = pd.read_csv(path)
            for col in schema_cols:
                if col not in df.columns:
                    df[col] = "" 
            return df
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=schema_cols)
    else:
        return pd.DataFrame(columns=schema_cols)

def save_data(platform, df):
    path = get_path(platform)
    df.to_csv(path, index=False, encoding="utf-8")

def today_str(): return datetime.today().strftime("%d-%m-%Y")


# ─── BARRA LATERAL (MENÚ) ────────────────────────────────────────────────────
st.sidebar.title("Gestor Laboral")
menu = st.sidebar.radio("Navegación", [
    "Resumen General", 
    "Agregar Postulación", 
    "Consultar / Filtrar", 
    "Actualizar Estado", 
    "Eliminar Postulación"
])

# ─── 1. RESUMEN GENERAL ──────────────────────────────────────────────────────
if menu == "Resumen General":
    render_header("Sección 01 · Dashboard", "Resumen General<br>de <em>Postulaciones</em>", "Métricas · Gráficos · Totales")
    
    all_data = []
    totales = {}
    
    for plat, display in PLATFORM_DISPLAY.items():
        df = load_data(plat)
        totales[display] = len(df)
        if not df.empty:
            df["Plataforma"] = display
            col_estado = SCHEMA[plat]["estado"]
            df["_Estado_"] = df[col_estado]
            all_data.append(df)
            
    render_section("Volumen global", "blue")
    cols = st.columns(len(PLATFORM_DISPLAY) + 1)
    cols[0].metric("TOTAL GLOBAL", sum(totales.values()))
    for i, (plat, total) in enumerate(totales.items(), 1):
        cols[i].metric(plat.upper(), total)
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    if all_data:
        df_all = pd.concat(all_data, ignore_index=True)
        
        col1, col2 = st.columns(2)
        with col1:
            render_section("Distribución por plataforma", "teal")
            st.bar_chart(df_all["Plataforma"].value_counts(), color="#1a7a6e")
            
        with col2:
            render_section("Estados frecuentes", "orange")
            conteo_estados = df_all["_Estado_"].value_counts().reset_index()
            conteo_estados.columns = ["Estado", "Cantidad"]
            st.dataframe(conteo_estados, use_container_width=True)
    else:
        st.info("Aún no hay postulaciones registradas en el sistema.")

# ─── 2. AGREGAR POSTULACIÓN ──────────────────────────────────────────────────
elif menu == "Agregar Postulación":
    render_header("Sección 02 · Ingreso de datos", "Nueva<br><em>Postulación</em>", "Formulario · Registro de actividad")
    
    render_section("Paso 1: Plataforma", "blue")
    plat_key = st.selectbox("Selecciona la Plataforma origen", list(PLATFORM_DISPLAY.keys()), format_func=lambda x: PLATFORM_DISPLAY[x].upper())
    schema = SCHEMA[plat_key]
    
    st.markdown("<br>", unsafe_allow_html=True)
    render_section("Paso 2: Datos de la vacante", "teal")
    
    with st.form("form_agregar"):
        col1, col2 = st.columns(2)
        puesto = col1.text_input("Puesto / Cargo *")
        empresa = col2.text_input("Empresa", placeholder="Confidencial")
        
        col3, col4 = st.columns(2)
        estado = col3.selectbox("Estado actual", schema["estados_validos"] + ["Otro (Especificar)"])
        estado_custom = ""
        if estado == "Otro (Especificar)":
            estado_custom = col3.text_input("Especificar estado:")
            
        fecha = col4.text_input("Fecha (DD-MM-YYYY)", value=today_str())
        
        ubicacion = url = publicacion = ""
        if plat_key in ["indeed", "computrabajo"]:
            ubicacion = st.text_input("Ubicación")
        if plat_key == "computrabajo":
            url = st.text_input("URL del Aviso")
        if plat_key in ["bumeran", "zonajobs"]:
            publicacion = st.text_input("Publicación (ID/URL)")
            
        submit = st.form_submit_button("Guardar Postulación")
        
        if submit:
            if not puesto:
                st.error("Error: El campo Puesto es obligatorio.")
            else:
                estado_final = estado_custom if estado == "Otro (Especificar)" else estado
                empresa_final = empresa if empresa else "Confidencial"
                
                new_row = {col: "" for col in schema["columns"]}
                new_row[schema["puesto"]] = puesto
                new_row[schema["empresa"]] = empresa_final
                new_row[schema["estado"]] = estado_final
                new_row[schema["fecha"]] = fecha
                
                if plat_key == "indeed": new_row["Ubicación"] = ubicacion
                if plat_key == "computrabajo": 
                    new_row["Ubicación"] = ubicacion
                    new_row["URL aviso"] = url
                if plat_key in ["bumeran", "zonajobs"]: new_row["Publicación"] = publicacion
                
                df = load_data(plat_key)
                df_new = pd.DataFrame([new_row])
                df = pd.concat([df, df_new], ignore_index=True)
                save_data(plat_key, df)
                st.success(f"Guardado exitosamente en {PLATFORM_DISPLAY[plat_key]}.")

# ─── 3. CONSULTAR ────────────────────────────────────────────────────────────
elif menu == "Consultar / Filtrar":
    render_header("Sección 03 · Búsqueda", "Consultar<br><em>Base de datos</em>", "Filtros · Búsqueda textual")
    
    render_section("Filtros activos", "orange")
    col1, col2 = st.columns(2)
    plat_filter = col1.selectbox("Plataforma", ["Todas"] + list(PLATFORM_DISPLAY.keys()), format_func=lambda x: PLATFORM_DISPLAY[x].upper() if x != "Todas" else "TODAS")
    search_text = col2.text_input("Término de búsqueda (Puesto o Empresa)", placeholder="Ej: Analista de Datos...")
    
    st.markdown("<br>", unsafe_allow_html=True)
    render_section("Resultados de la consulta", "blue")
    
    plats_to_show = list(PLATFORM_DISPLAY.keys()) if plat_filter == "Todas" else [plat_filter]
    
    total_results = 0
    for plat in plats_to_show:
        df = load_data(plat)
        if df.empty: continue
        
        schema = SCHEMA[plat]
        if search_text:
            mask = df[schema["puesto"]].fillna("").str.contains(search_text, case=False) | \
                   df[schema["empresa"]].fillna("").str.contains(search_text, case=False)
            df = df[mask]
            
        if not df.empty:
            st.markdown(f"**{PLATFORM_DISPLAY[plat].upper()}** — {len(df)} registros")
            st.dataframe(df, use_container_width=True)
            total_results += len(df)
            st.markdown("<br>", unsafe_allow_html=True)
            
    if total_results == 0:
        st.warning("No se encontraron registros que coincidan con los filtros.")

# ─── 4. ACTUALIZAR ESTADO ────────────────────────────────────────────────────
elif menu == "Actualizar Estado":
    render_header("Sección 04 · Edición", "Actualizar<br><em>Estado</em>", "Seguimiento · Novedades")
    
    render_section("Seleccionar registro", "teal")
    plat_key = st.selectbox("Plataforma", list(PLATFORM_DISPLAY.keys()), format_func=lambda x: PLATFORM_DISPLAY[x].upper())
    df = load_data(plat_key)
    schema = SCHEMA[plat_key]
    
    if df.empty:
        st.info("La base de datos está vacía para esta plataforma.")
    else:
        df["_label_"] = df[schema["puesto"]].astype(str) + " en " + df[schema["empresa"]].astype(str) + " [Estado actual: " + df[schema["estado"]].astype(str) + "]"
        
        selected_idx = st.selectbox("Postulación", df.index, format_func=lambda i: df.loc[i, "_label_"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        render_section("Nuevos valores", "blue")
        
        nuevo_estado = st.selectbox("Nuevo Estado", schema["estados_validos"])
        nota = st.text_input("Nota o Comentario (Opcional)")
        
        if st.button("Aplicar Cambios"):
            df.at[selected_idx, schema["estado"]] = nuevo_estado
            if nota:
                if "Notas" not in df.columns:
                    df["Notas"] = ""
                df.at[selected_idx, "Notas"] = nota
            
            df.drop(columns=["_label_"], inplace=True)
            save_data(plat_key, df)
            st.success("Estado actualizado de forma permanente.")
            st.rerun()

# ─── 5. ELIMINAR POSTULACIÓN ─────────────────────────────────────────────────
elif menu == "Eliminar Postulación":
    render_header("Sección 05 · Mantenimiento", "Eliminar<br><em>Registro</em>", "Acción destructiva · Limpieza")
    
    render_section("Búsqueda y selección", "red")
    plat_key = st.selectbox("Plataforma origen", list(PLATFORM_DISPLAY.keys()), format_func=lambda x: PLATFORM_DISPLAY[x].upper())
    df = load_data(plat_key)
    schema = SCHEMA[plat_key]
    
    if df.empty:
        st.info("La base de datos está vacía para esta plataforma.")
    else:
        df["_label_"] = df[schema["puesto"]].astype(str) + " en " + df[schema["empresa"]].astype(str) + " (" + df[schema["fecha"]].astype(str) + ")"
        selected_idx = st.selectbox("Registro a eliminar", df.index, format_func=lambda i: df.loc[i, "_label_"])
        
        st.warning(f"Está a punto de eliminar definitivamente el registro de **{df.loc[selected_idx, schema['puesto']]}** perteneciente a la empresa **{df.loc[selected_idx, schema['empresa']]}**.")
        
        if st.button("Confirmar Eliminación"):
            df = df.drop(selected_idx)
            df.drop(columns=["_label_"], inplace=True)
            save_data(plat_key, df)
            st.success("Registro eliminado correctamente.")
            st.rerun()