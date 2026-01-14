import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import re
import base64

# --- 1. CONFIGURACIÓN DE PÁGINA ---
try:
    logo_icon = Image.open("logofban_sf.png")
except:
    logo_icon = "🏦"

st.set_page_config(
    page_title="Generador de Firmas - Banco Solidario", 
    page_icon=logo_icon, 
    layout="centered"
)

# --- FUNCIÓN AUXILIAR ---
def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
        return f"data:image/png;base64,{encoded}"
    except:
        return None

# --- 2. CSS "PRO NAVBAR" CON FUENTE MATCH ---
st.markdown("""
    <style>
    /* IMPORTANTE: Traemos la fuente Nunito de Google para que coincida con el logo */
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;800&display=swap');

    /* Reset básico */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    html, body, [class*="st-"] {
        font-family: 'Inter', 'Segoe UI', Roboto, sans-serif !important;
    }

    /* BARRA SUPERIOR HORIZONTAL */
    .header-full-width {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 80px;
        background-color: #23b5d6; /* Celeste Corporativo */
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-bottom: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .header-content {
        display: flex;
        align-items: center;
        gap: 25px; /* Más espacio para elegancia */
    }

    .header-logo {
        height: 42px; /* Ajuste fino */
        width: auto;
        filter: drop-shadow(0px 2px 2px rgba(0,0,0,0.1));
    }
    
    .header-divider {
        height: 35px;
        width: 2px; /* Un poco más gruesa */
        background-color: rgba(255,255,255,0.3);
        border-radius: 2px;
    }

    .header-text-block {
        text-align: left;
        color: white;
        line-height: 1.1;
    }

    /* AQUI ESTÁ EL CAMBIO DE FUENTE */
    .header-title {
        font-family: 'Nunito', sans-serif; /* Fuente redondeada */
        font-size: 20px;
        font-weight: 800; /* Extra bold para parecerse al logo */
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .header-subtitle {
        font-family: 'Nunito', sans-serif;
        font-size: 13px;
        font-weight: 400;
        opacity: 0.95;
    }

    /* Ajuste del cuerpo */
    .block-container {
        padding-top: 120px !important; 
    }

    /* Estilos del Formulario */
    .section-header {
        color: #23b5d6;
        font-family: 'Nunito', sans-serif; /* También aplicamos redondez aquí */
        font-size: 15px;
        font-weight: 700;
        margin-top: 15px;
        margin-bottom: 5px;
        border-left: 5px solid #23b5d6;
        padding-left: 10px;
        text-transform: uppercase;
    }

    div.stButton > button:first-child {
        background-color: #23b5d6; color: white; border: none;
        font-weight: bold; height: 3em; width: 100%; border-radius: 8px; margin-top: 10px;
        font-family: 'Nunito', sans-serif; /* Botón con fuente redondeada */
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. RENDERIZADO DEL HEADER ---
logo_header = get_image_base64("header_banco.png")

if logo_header:
    st.markdown(f"""
        <div class="header-full-width">
            <div class="header-content">
                <img src="{logo_header}" class="header-logo">
                <div class="header-divider"></div>
                <div class="header-text-block">
                    <div class="header-title">Generador de Firmas</div>
                    <div class="header-subtitle">Plataforma de Autogestión</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown('<div class="header-full-width"><h3 style="color:white;">Banco Solidario</h3></div>', unsafe_allow_html=True)

# --- 4. FUNCIÓN GENERADORA ---
def generar_imagen_firma(datos):
    canvas_w, canvas_h = 600, 150 
    im = Image.new('RGB', (canvas_w, canvas_h), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    try:
        f_nom = ImageFont.truetype("Gotham-Medium.ttf", 20) 
        f_car = ImageFont.truetype("Gotham-Medium.ttf", 13)
        f_apt = ImageFont.truetype("Aptos.ttf", 11)
        f_boo = ImageFont.truetype("Gotham-Book.ttf", 11)
    except: return None

    x_base, x_sang = 135, 145
    y_curr = 15
    max_x = 0
    def med(txt, x, y, fnt, col="black"):
        nonlocal max_x
        draw.text((x, y), txt, font=fnt, fill=col)
        b = draw.textbbox((x, y), txt, font=fnt)
        if b[2] > max_x: max_x = b[2]

    med(datos["nombre_completo"], x_base, y_curr, f_nom, "#23b5d6")
    y_curr += 22 
    med(datos["cargo"], x_base, y_curr, f_car)
    y_curr += 18
    if datos["fijo"]: med(datos["fijo"], x_sang, y_curr, f_apt); y_curr += 14
    if datos["celular"]: med(datos["celular"], x_sang, y_curr, f_apt); y_curr += 14
    med(datos["email"], x_sang, y_curr, f_apt); y_curr += 14
    med(datos["direccion"], x_base, y_curr, f_boo); y_curr += 14
    med(datos["web"], x_base, y_curr, f_boo)
    
    try:
        logo_f = Image.open("logofban.png")
        h_logo = y_curr - 5 
        logo_res = logo_f.resize((int(h_logo * (logo_f.width/logo_f.height)), h_logo), Image.Resampling.LANCZOS)
        im.paste(logo_res, (15, 15), logo_res if logo_res.mode == 'RGBA' else None)
    except: pass
    
    return im.crop((0, 0, max_x + 20, y_curr + 20))

# --- 5. FORMULARIO ---
with st.container():
    with st.form("main_form"):
        st.markdown('<div class="section-header">INFORMACIÓN PERSONAL</div>', unsafe_allow_html=True)
        nombres = st.text_input("Nombres", placeholder="Ej: Juan Carlos")
        
        c1, c2 = st.columns(2)
        p_ape = st.text_input("Primer Apellido", placeholder="Ej: Pérez")
        s_ape = st.text_input("Segundo Apellido", placeholder="Ej: Armijos")
        
        st.markdown('<div class="section-header">PUESTO Y CONTACTO</div>', unsafe_allow_html=True)
        cargo = st.text_input("Cargo", placeholder="Ej: Analista de Crédito Senior")
        email = st.text_input("Correo Corporativo", placeholder="Ej: jperez@solidario.fin.ec")
        
        c3, c4 = st.columns(2)
        cel = st.text_input("Celular (Opcional)", placeholder="Ej: 0998765432")
        ext = st.text_input("Extensión (Opcional)", placeholder="Ej: 1234")
        
        st.markdown("<br>", unsafe_allow_html=True)
        submit = st.form_submit_button("Generar Firma Institucional")

if submit:
    if not (nombres and p_ape and s_ape and cargo and email):
        st.error("Por favor, complete los campos obligatorios.")
    elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        st.error("El formato del correo electrónico es incorrecto.")
    else:
        nom = nombres.strip().split(" ")[0].capitalize()
        p_ape_f = p_ape.strip().capitalize()
        s_ini = f"{s_ape.strip()[0].upper()}."
        full_nom = f"{nom} {p_ape_f} {s_ini}"

        cel_f = f"+593 {cel.strip().lstrip('0')[:2]} {cel.strip().lstrip('0')[2:5]} {cel.strip().lstrip('0')[5:]}" if cel.strip() else ""
        fij_f = f"(02) 3-950-600 Ext. {ext.strip()}" if ext.strip() else ""

        info = {
            "nombre_completo": full_nom, "cargo": cargo.strip(),
            "fijo": fij_f, "celular": cel_f, "email": email.strip().lower(),
            "direccion": "Amazonas y Corea N36-69. Quito/ Matriz", "web": "www.banco-solidario.com"
        }

        st.success("✅ Firma generada exitosamente")
        img = generar_imagen_firma(info)
        if img:
            st.image(img, caption="Vista Previa Oficial", width="content")
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            st.download_button("📥 Descargar Firma PNG", buf.getvalue(), f"Firma_{p_ape_f}.png", "image/png")
