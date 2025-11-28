import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
from fpdf2 import FPDF
import io
import base64

# ============================================
# CONFIGURACIÓN INICIAL
# ============================================
st.set_page_config(
    page_title="Sistema Escolar Interactivo",
    page_icon="🏫",
    layout="wide"
)

# ============================================
# ESTILOS GLOBALES (COLORES Y CONTRASTES)
# ============================================
st.markdown("""
<style>
/* Fondo general suave */
.stApp {
    background-color: #f4f6fb;
    color: #1f2933;
}

/* Texto normal */
body, p, label, span, div {
    color: #1f2933 !important;
}

/* Títulos */
h1, h2, h3, h4, h5, h6 {
    color: #111827 !important;
}

/* Botones primarios */
.stButton>button[kind="primary"] {
    background: linear-gradient(90deg, #2563eb 0%, #1d4ed8 100%);
    color: white;
    border-radius: 8px;
    border: none;
}

/* Botones normales */
.stButton>button:not([kind="primary"]) {
    background-color: #e5e7eb;
    color: #111827;
    border-radius: 8px;
    border: 1px solid #d1d5db;
}

/* Caja aviso privacidad */
.privacy-box {
    background-color: #e5ecff !important;
    padding: 20px;
    border-radius: 10px;
    border-left: 5px solid #1d4ed8;
    color: #111827 !important;
}

/* Encabezado principal login */
.main-header {
    text-align: center;
    padding: 20px;
    background: linear-gradient(90deg, #1d4ed8 0%, #2563eb 100%);
    color: white !important;
    border-radius: 10px;
    margin-bottom: 30px;
}

/* Tarjetas colegios */
.school-card {
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    transition: transform 0.3s;
}
.school-card:hover {
    transform: scale(1.02);
}

/* Burbujas del chat */
.chat-user {
    background-color: #d1fae5;
    padding: 10px;
    border-radius: 10px;
    margin: 5px 0;
    text-align: right;
}
.chat-bot {
    background-color: #e5e7eb;
    padding: 10px;
    border-radius: 10px;
    margin: 5px 0;
}

/* Tabla previa certificado */
.cert-box {
    background-color: #fff7ed;
    padding: 30px;
    border: 2px solid #c05621;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ============================================
# DATOS DE ESTUDIANTES - COLEGIO CARLOS GIRALDO
# ============================================
data_carlos_giraldo = [
    ["Alejandro Vargas", 13579246, "Matemáticas", 4.5, 8],
    ["Alejandro Vargas", 13579246, "Español", 7.2, 9],
    ["Alejandro Vargas", 13579246, "Inglés", 6.8, 7],
    ["Alejandro Vargas", 13579246, "Ciencias", 5.9, 8],
    ["Beatriz Morales", 24681357, "Matemáticas", 8.1, 10],
    ["Beatriz Morales", 24681357, "Español", 9.0, 10],
    ["Beatriz Morales", 24681357, "Inglés", 7.5, 9],
    ["Beatriz Morales", 24681357, "Ciencias", 8.8, 10],
    ["Carlos Mendoza", 35792468, "Matemáticas", 6.4, 7],
    ["Carlos Mendoza", 35792468, "Español", 5.8, 6],
    ["Carlos Mendoza", 35792468, "Inglés", 8.2, 9],
    ["Carlos Mendoza", 35792468, "Ciencias", 7.0, 8],
    ["Daniela Ortiz", 46813579, "Matemáticas", 3.8, 5],
    ["Daniela Ortiz", 46813579, "Español", 6.5, 8],
    ["Daniela Ortiz", 46813579, "Inglés", 5.0, 6],
    ["Daniela Ortiz", 46813579, "Ciencias", 4.2, 4],
    ["Eduardo Navarro", 57924680, "Matemáticas", 9.2, 10],
    ["Eduardo Navarro", 57924680, "Español", 8.7, 9],
    ["Eduardo Navarro", 57924680, "Inglés", 9.5, 10],
    ["Eduardo Navarro", 57924680, "Ciencias", 8.9, 10],
]

# ============================================
# DATOS DE ESTUDIANTES - INSTITUTO OLGA SANTAMARÍA
# ============================================
data_olga_santamaria = [
    ["Fernanda Pérez", 68035791, "Matemáticas", 7.9, 9],
    ["Fernanda Pérez", 68035791, "Español", 8.8, 10],
    ["Fernanda Pérez", 68035791, "Inglés", 9.0, 10],
    ["Fernanda Pérez", 68035791, "Ciencias", 8.5, 9],
    ["Gabriel Quintana", 79146802, "Matemáticas", 5.3, 7],
    ["Gabriel Quintana", 79146802, "Español", 7.6, 9],
    ["Gabriel Quintana", 79146802, "Inglés", 6.1, 8],
    ["Gabriel Quintana", 79146802, "Ciencias", 6.8, 7],
    ["Helena Ruiz", 80257913, "Matemáticas", 8.5, 10],
    ["Helena Ruiz", 80257913, "Español", 7.3, 8],
    ["Helena Ruiz", 80257913, "Inglés", 8.9, 10],
    ["Helena Ruiz", 80257913, "Ciencias", 7.7, 9],
    ["Ignacio Salazar", 91368024, "Matemáticas", 6.7, 8],
    ["Ignacio Salazar", 91368024, "Español", 5.5, 6],
    ["Ignacio Salazar", 91368024, "Inglés", 7.4, 9],
    ["Ignacio Salazar", 91368024, "Ciencias", 6.9, 8],
    ["Juliana Torres", 2479135, "Matemáticas", 9.0, 10],
    ["Juliana Torres", 2479135, "Español", 8.6, 9],
    ["Juliana Torres", 2479135, "Inglés", 9.3, 10],
    ["Juliana Torres", 2479135, "Ciencias", 8.8, 10],
]

# Crear DataFrames
columns = ["Nombre", "Cedula", "Asignatura", "Nota_Parcial", "Nota_Final"]
df_carlos_giraldo = pd.DataFrame(data_carlos_giraldo, columns=columns)
df_carlos_giraldo["Colegio"] = "Colegio Departamental Carlos Giraldo"

df_olga_santamaria = pd.DataFrame(data_olga_santamaria, columns=columns)
df_olga_santamaria["Colegio"] = "Instituto Técnico Olga Santamaría"

# DataFrame combinado
df_all_students = pd.concat([df_carlos_giraldo, df_olga_santamaria], ignore_index=True)

# ============================================
# DATOS DE ASISTENCIA (INICIALIZACIÓN SIMPLE)
# ============================================
# Creamos una asistencia aleatoria (0-100 %) por estudiante
def inicializar_asistencia(df):
    asistencia = df[['Nombre', 'Cedula']].drop_duplicates().copy()
    asistencia['Asistencia_%'] = [random.randint(80, 100) for _ in range(len(asistencia))]
    return asistencia

if 'asistencia_cg' not in st.session_state:
    st.session_state.asistencia_cg = inicializar_asistencia(df_carlos_giraldo)
if 'asistencia_os' not in st.session_state:
    st.session_state.asistencia_os = inicializar_asistencia(df_olga_santamaria)

# ============================================
# DATOS DE PROFESORES
# ============================================
profesores_data = {
    "Colegio Departamental Carlos Giraldo": [
        {"nombre": "Prof. María García", "cedula": 11111111, "asignatura": "Matemáticas"},
        {"nombre": "Prof. Juan López", "cedula": 22222222, "asignatura": "Español"},
        {"nombre": "Prof. Ana Martínez", "cedula": 33333333, "asignatura": "Inglés"},
        {"nombre": "Prof. Pedro Sánchez", "cedula": 44444444, "asignatura": "Ciencias"},
    ],
    "Instituto Técnico Olga Santamaría": [
        {"nombre": "Prof. Laura Rodríguez", "cedula": 55555555, "asignatura": "Matemáticas"},
        {"nombre": "Prof. Carlos Hernández", "cedula": 66666666, "asignatura": "Español"},
        {"nombre": "Prof. Diana Gómez", "cedula": 77777777, "asignatura": "Inglés"},
        {"nombre": "Prof. Roberto Díaz", "cedula": 88888888, "asignatura": "Ciencias"},
    ]
}

# ============================================
# INFORMACIÓN ESCOLAR
# ============================================
info_escolar = {
    "calendario_academico": """
📅 **CALENDARIO ACADÉMICO 2024-2025**

**Primer Semestre:**
- Inicio de clases: 22 de Enero 2024
- Semana de receso: 25-29 de Marzo (Semana Santa)
- Fin primer período: 12 de Abril
- Entrega de boletines: 19 de Abril
- Fin segundo período: 14 de Junio
- Vacaciones mitad de año: 17 Junio - 7 Julio

**Segundo Semestre:**
- Inicio segundo semestre: 8 de Julio
- Semana de receso: 7-11 de Octubre
- Fin tercer período: 13 de Septiembre
- Fin cuarto período: 22 de Noviembre
- Clausura: 29 de Noviembre
    """,

    "matriculas": """
📋 **INFORMACIÓN DE MATRÍCULAS**

**Fechas de matrícula 2025:**
- Estudiantes antiguos: 1-15 de Noviembre 2024
- Estudiantes nuevos: 18-30 de Noviembre 2024

**Requisitos:**
1. Fotocopia documento de identidad
2. Certificado de estudios anteriores
3. Fotos 3x4 fondo azul (2 unidades)
4. Certificado médico
5. Paz y salvo año anterior

**Costos:**
- Matrícula: $150.000
- Pensión mensual: $180.000
- Seguro estudiantil: $45.000/año
    """,

    "actividades_escolares": """
🎭 **ACTIVIDADES ESCOLARES 2024**

**Próximos eventos:**
- 15 Feb: Día del Amor y la Amistad
- 8 Mar: Día de la Mujer
- 23 Abr: Día del Idioma
- 30 Abr: Día del Niño
- 15 May: Día del Maestro
- 20 Jul: Izadas de bandera - Independencia
- 7 Ago: Batalla de Boyacá
- 12 Oct: Día de la Raza
- 31 Oct: Halloween escolar
- 11 Nov: Festival de talentos
- 29 Nov: Clausura y grados
    """,

    "rutas_escolares": """
🚌 **RUTAS ESCOLARES**

**Rutas disponibles:**

**Ruta 1 - Norte:**
- Salida: 6:00 AM
- Paradas: Centro, La Estación, Barrio Norte
- Costo: $120.000/mes

**Ruta 2 - Sur:**
- Salida: 6:15 AM
- Paradas: Terminal, Barrio Sur, La Esperanza
- Costo: $120.000/mes

**Ruta 3 - Oriente:**
- Salida: 6:00 AM
- Paradas: Comuneros, San José, El Prado
- Costo: $130.000/mes

**Contacto transporte:** 310-555-1234
    """,

    "horarios": """
⏰ **HORARIOS DE CLASE**

**Jornada Mañana:**
- Entrada: 6:30 AM
- Primera hora: 6:45 - 7:35 AM
- Segunda hora: 7:35 - 8:25 AM
- Descanso: 8:25 - 8:50 AM
- Tercera hora: 8:50 - 9:40 AM
- Cuarta hora: 9:40 - 10:30 AM
- Descanso: 10:30 - 10:50 AM
- Quinta hora: 10:50 - 11:40 AM
- Sexta hora: 11:40 AM - 12:30 PM

**Jornada Tarde:**
- Entrada: 12:30 PM
- Salida: 6:30 PM
    """,

    "asignaturas": """
📚 **ASIGNATURAS**

**Áreas Fundamentales:**
- Matemáticas (5 horas/semana)
- Español y Literatura (5 horas/semana)
- Inglés (4 horas/semana)
- Ciencias Naturales (4 horas/semana)
- Ciencias Sociales (3 horas/semana)

**Áreas Complementarias:**
- Educación Física (2 horas/semana)
- Artística (2 horas/semana)
- Tecnología e Informática (2 horas/semana)
- Ética y Valores (1 hora/semana)
- Religión (1 hora/semana)
    """,

    "reuniones": """
👥 **REUNIONES DE PADRES**

**Próximas reuniones:**

📌 **Entrega de boletines 1er período:**
- Fecha: 19 de Abril 2024
- Hora: 7:00 AM - 12:00 PM
- Lugar: Salones de clase

📌 **Asamblea general de padres:**
- Fecha: 10 de Mayo 2024
- Hora: 8:00 AM
- Lugar: Auditorio principal

📌 **Escuela de padres:**
- Fechas: Último viernes de cada mes
- Hora: 6:00 PM
- Tema Mayo: "Acompañamiento escolar"
    """,

    "fechas_entrega": """
📝 **FECHAS DE ENTREGA**

**Período actual - Abril 2024:**

| Asignatura | Trabajo | Fecha |
|------------|---------|-------|
| Matemáticas | Taller álgebra | 15 Abril |
| Español | Ensayo literario | 18 Abril |
| Inglés | Presentación oral | 20 Abril |
| Ciencias | Proyecto ecosistemas | 22 Abril |
| Sociales | Línea de tiempo | 25 Abril |

**Exámenes finales período:**
- 8-12 de Abril 2024
    """,

    "actividades": """
📋 **ACTIVIDADES PENDIENTES**

**Esta semana:**
- Lunes: Quiz de matemáticas
- Martes: Exposición de inglés
- Miércoles: Laboratorio de ciencias
- Jueves: Entrega taller español
- Viernes: Evaluación sociales

**Próxima semana:**
- Preparación día del idioma
- Ensayos grupo de danzas
- Inicio proyecto de feria científica
    """,

    "tutoria": f"""
📖 **TUTORÍAS Y REFUERZOS ACADÉMICOS**

🎥 **Video de refuerzo recomendado:**
https://www.youtube.com/watch?v=0d5VWxcSUIk

**Horarios de tutorías presenciales:**
- Lunes y Miércoles: 2:00 PM - 4:00 PM (Matemáticas)
- Martes y Jueves: 2:00 PM - 4:00 PM (Español e Inglés)
- Viernes: 2:00 PM - 4:00 PM (Ciencias)

**Para agendar tutoría:**
1. Habla con tu director de grupo
2. Inscríbete en coordinación académica
3. Las tutorías son gratuitas

**Contacto:** coordinacion@colegio.edu.co
    """
}

# ============================================
# INICIALIZAR SESSION STATE
# ============================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'user_data' not in st.session_state:
    st.session_state.user_data = None
if 'colegio' not in st.session_state:
    st.session_state.colegio = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'consultas' not in st.session_state:
    st.session_state.consultas = {
        "calendario": 0, "matriculas": 0, "actividades": 0,
        "rutas": 0, "horarios": 0, "asignaturas": 0,
        "reuniones": 0, "fechas_entrega": 0, "tutoria": 0, "notas": 0
    }
if 'privacy_accepted' not in st.session_state:
    st.session_state.privacy_accepted = False

# Para poder editar notas y que se mantengan en sesión
if 'df_cg' not in st.session_state:
    st.session_state.df_cg = df_carlos_giraldo.copy()
if 'df_os' not in st.session_state:
    st.session_state.df_os = df_olga_santamaria.copy()

# ============================================
# FUNCIONES AUXILIARES
# ============================================

def generar_certificado_pdf(nombre, cedula, colegio, promedio):
    """Genera un certificado de estudios en PDF"""
    pdf = FPDF()
    pdf.add_page()

    # Encabezado
    pdf.set_font('Arial', 'B', 20)
    pdf.cell(0, 20, 'CERTIFICADO DE ESTUDIOS', 0, 1, 'C')
    pdf.ln(10)

    # Nombre del colegio
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, colegio.upper(), 0, 1, 'C')
    pdf.ln(10)

    # Línea decorativa
    pdf.set_draw_color(0, 0, 128)
    pdf.line(30, pdf.get_y(), 180, pdf.get_y())
    pdf.ln(15)

    # Cuerpo del certificado
    pdf.set_font('Arial', '', 12)

    texto = f"""
El/La rector(a) del {colegio}, 

CERTIFICA QUE:

El/La estudiante {nombre}, identificado(a) con documento 
de identidad No. {cedula}, se encuentra matriculado(a) 
y cursando estudios en esta institución educativa durante 
el año lectivo 2024.

El estudiante presenta un promedio académico de: {promedio:.2f}

Este certificado se expide a solicitud del interesado(a) 
en la ciudad de Bogotá, a los {datetime.now().day} días 
del mes de {datetime.now().strftime('%B')} de {datetime.now().year}.
    """

    pdf.multi_cell(0, 8, texto)
    pdf.ln(20)

    # Firma
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 10, 'RECTOR(A)', 0, 1, 'C')
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 5, colegio, 0, 1, 'C')

    # Pie de página
    pdf.ln(20)
    pdf.set_font('Arial', 'I', 8)
    pdf.cell(0, 5, f'Documento generado el {datetime.now().strftime("%d/%m/%Y %H:%M")}', 0, 1, 'C')
    pdf.cell(0, 5, 'Este documento es válido sin firma ni sello para trámites internos', 0, 1, 'C')

    return pdf.output(dest='S').encode('latin-1')


def obtener_df_colegio():
    if st.session_state.colegio == "Colegio Departamental Carlos Giraldo":
        return st.session_state.df_cg
    else:
        return st.session_state.df_os


def obtener_asistencia_df():
    if st.session_state.colegio == "Colegio Departamental Carlos Giraldo":
        return st.session_state.asistencia_cg
    else:
        return st.session_state.asistencia_os


def procesar_pregunta(pregunta):
    """Procesa la pregunta del chatbot y retorna la respuesta y opcionalmente datos adjuntos."""
    pregunta_lower = pregunta.lower()
    user = st.session_state.user_data if st.session_state.user_data else None

    # Datos del estudiante actual (si es estudiante)
    df_colegio = obtener_df_colegio()
    asistencia_df = obtener_asistencia_df()
    df_est = None
    df_asist_est = None
    if user and st.session_state.user_type == "estudiante":
        df_est = df_colegio[df_colegio['Cedula'] == user['cedula']]
        df_asist_est = asistencia_df[asistencia_df['Cedula'] == user['cedula']]

    # --- INTENCIONES ---

    # Notas / promedio detallados por chat
    if any(w in pregunta_lower for w in ['nota', 'calificación', 'calificacion', 'promedio', 'boletin', 'boletín']):
        st.session_state.consultas["notas"] += 1
        if df_est is None or df_est.empty:
            return "No encuentro tus notas en el sistema. Verifica que hayas iniciado sesión como estudiante.", None

        promedio_parcial = df_est['Nota_Parcial'].mean()
        promedio_final = df_est['Nota_Final'].mean()
        detalles = df_est[['Asignatura', 'Nota_Parcial', 'Nota_Final']].copy()
        detalles.columns = ['Asignatura', 'Nota Parcial', 'Nota Final']

        tabla_md = "| Asignatura | Nota Parcial | Nota Final |\n|-----------|-------------|-----------|\n"
        for _, r in detalles.iterrows():
            tabla_md += f"| {r['Asignatura']} | {r['Nota Parcial']:.2f} | {r['Nota Final']:.2f} |\n"

        texto = f"""📊 **Tus notas actuales**

{tabla_md}

**Promedio parcial:** {promedio_parcial:.2f}  
**Promedio final:** {promedio_final:.2f}
"""
        # Devolvemos también los datos para dashboards (opcional)
        return texto, {"tipo": "notas", "df": df_est}

    # Asistencia
    if any(w in pregunta_lower for w in ['asistencia', 'faltas', 'inasistencia']):
        if df_asist_est is None or df_asist_est.empty:
            return "No tengo registrada tu asistencia todavía.", None
        asis = df_asist_est['Asistencia_%'].iloc[0]
        texto = f"📅 Tu **asistencia acumulada** al colegio es de **{asis:.1f}%**."
        return texto, {"tipo": "asistencia", "valor": asis}

    # Dashboard general del estudiante
    if any(w in pregunta_lower for w in ['dashboard', 'resumen', 'rendimiento', 'estadísticas', 'estadisticas']):
        if df_est is None or df_est.empty:
            return "No encuentro información suficiente para hacer tu dashboard.", None

        promedio_final = df_est['Nota_Final'].mean()
        asis_val = None
        if df_asist_est is not None and not df_asist_est.empty:
            asis_val = df_asist_est['Asistencia_%'].iloc[0]

        texto = f"""📈 **Resumen de tu rendimiento**

- Promedio final general: **{promedio_final:.2f}**
- Asistencia: **{asis_val:.1f}%**""" if asis_val is not None else f"""📈 **Resumen de tu rendimiento**

- Promedio final general: **{promedio_final:.2f}**
- Asistencia: *(no registrada)*"""

        return texto, {"tipo": "dashboard_est", "df": df_est, "asistencia": asis_val}

    # Certificado solicitado por chat
    if any(w in pregunta_lower for w in ['certificado', 'constancia', 'documento de estudios']):
        if not user or st.session_state.user_type != "estudiante":
            return "Solo los estudiantes pueden generar su certificado de estudios desde el chat.", None

        df_est = df_colegio[df_colegio['Cedula'] == user['cedula']]
        if df_est.empty:
            return "No encontré tus notas para generar el certificado.", None
        promedio = df_est['Nota_Final'].mean()
        pdf_bytes = generar_certificado_pdf(user['nombre'], user['cedula'], user['colegio'], promedio)
        # Guardamos el PDF en session_state para que el chat lo pueda descargar
        st.session_state.chat_certificado = {
            "pdf": pdf_bytes,
            "filename": f"certificado_{user['nombre'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
        }

        texto = """📜 He generado tu **certificado de estudios**.

Debajo de este mensaje verás un botón para descargarlo en formato PDF."""
        return texto, {"tipo": "certificado"}

    # Calendario
    if any(palabra in pregunta_lower for palabra in ['calendario', 'fechas', 'cuando empiezan', 'vacaciones']):
        st.session_state.consultas["calendario"] += 1
        return info_escolar["calendario_academico"], None

    # Matrículas
    if any(palabra in pregunta_lower for palabra in ['matricula', 'inscripción', 'inscribir', 'requisitos matricula', 'matrícula']):
        st.session_state.consultas["matriculas"] += 1
        return info_escolar["matriculas"], None

    # Actividades
    if any(palabra in pregunta_lower for palabra in ['actividad', 'evento', 'celebración', 'festival', 'celebracion']):
        st.session_state.consultas["actividades"] += 1
        return info_escolar["actividades_escolares"], None

    # Rutas
    if any(palabra in pregunta_lower for palabra in ['ruta', 'transporte', 'bus', 'recorrido']):
        st.session_state.consultas["rutas"] += 1
        return info_escolar["rutas_escolares"], None

    # Horarios
    if any(palabra in pregunta_lower for palabra in ['horario', 'hora', 'jornada', 'entrada', 'salida']):
        st.session_state.consultas["horarios"] += 1
        return info_escolar["horarios"], None

    # Asignaturas
    if any(palabra in pregunta_lower for palabra in ['asignatura', 'materia', 'clase', 'área', 'area']):
        st.session_state.consultas["asignaturas"] += 1
        return info_escolar["asignaturas"], None

    # Reuniones
    if any(palabra in pregunta_lower for palabra in ['reunión', 'reunion', 'padres', 'citación', 'citacion', 'asamblea']):
        st.session_state.consultas["reuniones"] += 1
        return info_escolar["reuniones"], None

    # Fechas de entrega / tareas
    if any(palabra in pregunta_lower for palabra in ['entrega', 'tarea', 'trabajo', 'examen', 'quiz']):
        st.session_state.consultas["fechas_entrega"] += 1
        return info_escolar["fechas_entrega"], None

    # Tutorías
    if any(palabra in pregunta_lower for palabra in ['tutoria', 'tutoría', 'refuerzo', 'ayuda', 'apoyo', 'no entiendo']):
        st.session_state.consultas["tutoria"] += 1
        return info_escolar["tutoria"], None

    # Saludos
    if any(palabra in pregunta_lower for palabra in ['hola', 'buenos dias', 'buenas tardes', 'hey']):
        nombre = user['nombre'] if user else "usuario"
        return f"""👋 ¡Hola {nombre}!

Puedo ayudarte con:
- Notas, promedios y dashboard de tu rendimiento
- Asistencia
- Certificado de estudios
- Calendario, matrículas, actividades, rutas
- Horarios, asignaturas, reuniones, fechas de entrega
- Tutorías y refuerzos

Solo escribe tu pregunta. Ejemplo:  
- "muéstrame mi promedio"  
- "quiero mi certificado"  
- "cómo está mi asistencia?"  
- "qué actividades hay este mes?"
""", None

    # Agradecimientos
    if any(palabra in pregunta_lower for palabra in ['gracias', 'thank', 'genial']):
        return "Con gusto. Si tienes más preguntas, aquí estoy.", None

    # Desconocido
    return """No estoy seguro de entender tu pregunta.

Puedo responder sobre:
- Notas, promedios, asistencia, certificado
- Calendario, matrículas
- Actividades, rutas
- Horarios, asignaturas
- Reuniones, fechas de entrega
- Tutorías y refuerzos

Intenta reformular tu pregunta. Ejemplo: "muéstrame mis notas de todas las materias".""", None

# ============================================
# PÁGINA DE PRIVACIDAD
# ============================================
def mostrar_aviso_privacidad():
    st.title("🔒 Aviso de Privacidad y Protección de Datos")

    st.markdown("""
    <div class="privacy-box">

    ### POLÍTICA DE PRIVACIDAD Y PROTECCIÓN DE DATOS PERSONALES

    **Fecha de última actualización:** Enero 2024

    #### 1. RESPONSABLE DEL TRATAMIENTO
    El responsable del tratamiento de sus datos personales es la institución educativa seleccionada.

    #### 2. DATOS QUE RECOPILAMOS
    - Nombre completo  
    - Número de identificación (cédula)  
    - Información académica (notas, asignaturas)  
    - Historial de consultas en el sistema  

    #### 3. FINALIDAD DEL TRATAMIENTO
    Sus datos serán utilizados para:
    - Gestión académica y administrativa
    - Generación de certificados de estudio
    - Seguimiento del rendimiento académico
    - Comunicación de información institucional

    #### 4. DERECHOS DEL TITULAR
    Usted tiene derecho a:
    - Conocer, actualizar y rectificar sus datos
    - Solicitar prueba de la autorización
    - Ser informado sobre el uso de sus datos
    - Revocar la autorización
    - Acceder gratuitamente a sus datos

    #### 5. MEDIDAS DE SEGURIDAD
    Implementamos medidas técnicas y organizativas para proteger sus datos contra:
    - Acceso no autorizado
    - Pérdida o destrucción
    - Uso indebido

    #### 6. TRANSFERENCIA DE DATOS
    Sus datos NO serán compartidos con terceros sin su consentimiento expreso, 
    excepto cuando sea requerido por ley.

    #### 7. CONSERVACIÓN DE DATOS
    Los datos se conservarán mientras mantenga vínculo con la institución 
    y por el tiempo adicional requerido por normativas educativas.

    #### 8. CONTACTO
    Para ejercer sus derechos o consultas sobre esta política:
    - Email: protecciondatos@colegio.edu.co
    - Teléfono: (601) 555-0123

    ---
    **Base legal:** Ley 1581 de 2012 (Colombia) - Protección de Datos Personales
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        acepto = st.checkbox("He leído y acepto la política de privacidad y tratamiento de datos personales")
        if acepto:
            if st.button("Continuar al Sistema", type="primary", use_container_width=True):
                st.session_state.privacy_accepted = True
                st.rerun()

# ============================================
# PÁGINA DE LOGIN
# ============================================
def mostrar_login():
    st.markdown('<div class="main-header"><h1>🏫 Sistema Escolar Interactivo</h1><p>Bienvenido al portal estudiantil</p></div>', unsafe_allow_html=True)

    st.markdown("### 📍 Paso 1: Selecciona tu Colegio")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="school-card" style="background-color: #dbeafe;">
        <h3>🏛️ Colegio Departamental Carlos Giraldo</h3>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Seleccionar Carlos Giraldo", key="cg", use_container_width=True):
            st.session_state.colegio = "Colegio Departamental Carlos Giraldo"

    with col2:
        st.markdown("""
        <div class="school-card" style="background-color: #fee2e2;">
        <h3>🏛️ Instituto Técnico Olga Santamaría</h3>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Seleccionar Olga Santamaría", key="os", use_container_width=True):
            st.session_state.colegio = "Instituto Técnico Olga Santamaría"

    if st.session_state.colegio:
        st.success(f"✅ Colegio seleccionado: **{st.session_state.colegio}**")

        st.markdown("---")
        st.markdown("### 👤 Paso 2: Selecciona tu rol")

        user_type = st.radio(
            "¿Eres estudiante o profesor?",
            ["Estudiante", "Profesor"],
            horizontal=True
        )

        st.markdown("---")
        st.markdown("### 🔐 Paso 3: Ingresa tu número de cédula")

        cedula = st.text_input("Número de cédula:", placeholder="Ej: 12345678")

        if st.button("🚀 Ingresar al Sistema", type="primary", use_container_width=True):
            if cedula:
                try:
                    cedula_num = int(cedula)

                    if user_type == "Estudiante":
                        # Buscar en el DataFrame correcto
                        df_buscar = obtener_df_colegio()
                        estudiante = df_buscar[df_buscar['Cedula'] == cedula_num]

                        if not estudiante.empty:
                            st.session_state.logged_in = True
                            st.session_state.user_type = "estudiante"
                            st.session_state.user_data = {
                                "nombre": estudiante['Nombre'].iloc[0],
                                "cedula": cedula_num,
                                "colegio": st.session_state.colegio
                            }
                            st.rerun()
                        else:
                            st.error("❌ Cédula no encontrada. Verifica que estés en el colegio correcto.")

                    else:  # Profesor
                        profesores = profesores_data.get(st.session_state.colegio, [])
                        profesor = next((p for p in profesores if p['cedula'] == cedula_num), None)

                        if profesor:
                            st.session_state.logged_in = True
                            st.session_state.user_type = "profesor"
                            st.session_state.user_data = {
                                "nombre": profesor['nombre'],
                                "cedula": cedula_num,
                                "asignatura": profesor['asignatura'],
                                "colegio": st.session_state.colegio
                            }
                            st.rerun()
                        else:
                            st.error("❌ Cédula de profesor no encontrada.")

                except ValueError:
                    st.error("❌ Por favor ingresa un número de cédula válido.")
            else:
                st.warning("⚠️ Por favor ingresa tu número de cédula.")

# ============================================
# DASHBOARD ESTUDIANTE
# ============================================
def mostrar_dashboard_estudiante():
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/student-male--v1.png", width=80)
        st.markdown(f"### 👋 ¡Hola, {st.session_state.user_data['nombre']}!")
        st.markdown(f"📍 {st.session_state.colegio}")
        st.markdown(f"🆔 C.C. {st.session_state.user_data['cedula']}")
        st.markdown("---")

        menu = st.radio(
            "📌 Menú",
            ["💬 Chat Bot", "📊 Mis Notas", "📜 Certificado", "📈 Dashboard", "🔒 Privacidad"]
        )

        st.markdown("---")
        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_type = None
            st.session_state.user_data = None
            st.session_state.chat_history = []
            st.rerun()

    if menu == "💬 Chat Bot":
        mostrar_chatbot()
    elif menu == "📊 Mis Notas":
        mostrar_notas()
    elif menu == "📜 Certificado":
        mostrar_certificado()
    elif menu == "📈 Dashboard":
        mostrar_dashboard_stats()
    elif menu == "🔒 Privacidad":
        mostrar_info_privacidad()

def mostrar_chatbot():
    import plotly.graph_objects as go
    import plotly.express as px

    st.title("💬 Asistente Virtual Escolar")
    st.markdown("Pregúntame sobre tus notas, promedios, asistencia, certificado, calendario, actividades, etc.")

    chat_container = st.container()

    with chat_container:
        for mensaje in st.session_state.chat_history:
            if mensaje["role"] == "user":
                st.markdown(f"""
                <div class="chat-user">
                    <strong>Tú:</strong> {mensaje["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-bot">
                    <strong>🤖 Asistente:</strong><br>{mensaje["content"]}
                </div>
                """, unsafe_allow_html=True)

                # Si el mensaje trae datos adjuntos para mostrar dashboard/gráfico
                if "extra" in mensaje and mensaje["extra"] is not None:
                    extra = mensaje["extra"]
                    if extra.get("tipo") == "notas":
                        df_est = extra["df"]
                        fig = go.Figure()
                        fig.add_trace(go.Bar(
                            name='Nota Parcial',
                            x=df_est['Asignatura'],
                            y=df_est['Nota_Parcial'],
                            marker_color='#93c5fd'
                        ))
                        fig.add_trace(go.Bar(
                            name='Nota Final',
                            x=df_est['Asignatura'],
                            y=df_est['Nota_Final'],
                            marker_color='#1d4ed8'
                        ))
                        fig.update_layout(
                            barmode='group',
                            title='Notas por Asignatura',
                            xaxis_title='Asignatura',
                            yaxis_title='Nota',
                            yaxis_range=[0, 10]
                        )
                        st.plotly_chart(fig, use_container_width=True)

                    elif extra.get("tipo") == "asistencia":
                        asis = extra["valor"]
                        fig = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=asis,
                            title={'text': "Asistencia %"},
                            gauge={'axis': {'range': [0, 100]},
                                   'bar': {'color': "#10b981"}}
                        ))
                        st.plotly_chart(fig, use_container_width=True)

                    elif extra.get("tipo") == "dashboard_est":
                        df_est = extra["df"]
                        asis_val = extra.get("asistencia", None)
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**Promedio por asignatura**")
                            prom = df_est.groupby('Asignatura')['Nota_Final'].mean().reset_index()
                            fig2 = px.bar(prom, x='Asignatura', y='Nota_Final', range_y=[0, 10],
                                          color='Asignatura', title='')
                            st.plotly_chart(fig2, use_container_width=True)
                        with col2:
                            if asis_val is not None:
                                st.markdown("**Asistencia**")
                                fig3 = go.Figure(go.Indicator(
                                    mode="gauge+number",
                                    value=asis_val,
                                    title={'text': "Asistencia %"},
                                    gauge={'axis': {'range': [0, 100]},
                                           'bar': {'color': "#10b981"}}
                                ))
                                st.plotly_chart(fig3, use_container_width=True)

                    elif extra.get("tipo") == "certificado":
                        # Botón de descarga del certificado generado por el chat
                        cert = st.session_state.get("chat_certificado", None)
                        if cert:
                            st.download_button(
                                label="📥 Descargar Certificado PDF",
                                data=cert["pdf"],
                                file_name=cert["filename"],
                                mime="application/pdf"
                            )

    st.markdown("---")

    # Accesos rápidos
    st.markdown("**🚀 Accesos rápidos:**")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📅 Calendario"):
            pregunta = "calendario académico"
            respuesta, extra = procesar_pregunta(pregunta)
            st.session_state.chat_history.append({"role": "user", "content": pregunta})
            st.session_state.chat_history.append({"role": "assistant", "content": respuesta, "extra": extra})
            st.rerun()
    with col2:
        if st.button("⏰ Horarios"):
            pregunta = "horarios"
            respuesta, extra = procesar_pregunta(pregunta)
            st.session_state.chat_history.append({"role": "user", "content": pregunta})
            st.session_state.chat_history.append({"role": "assistant", "content": respuesta, "extra": extra})
            st.rerun()
    with col3:
        if st.button("📖 Tutorías"):
            pregunta = "tutoria refuerzo"
            respuesta, extra = procesar_pregunta(pregunta)
            st.session_state.chat_history.append({"role": "user", "content": pregunta})
            st.session_state.chat_history.append({"role": "assistant", "content": respuesta, "extra": extra})
            st.rerun()
    with col4:
        if st.button("🚌 Rutas"):
            pregunta = "rutas escolares"
            respuesta, extra = procesar_pregunta(pregunta)
            st.session_state.chat_history.append({"role": "user", "content": pregunta})
            st.session_state.chat_history.append({"role": "assistant", "content": respuesta, "extra": extra})
            st.rerun()

    pregunta_usuario = st.text_input("✍️ Escribe tu pregunta:", key="chat_input", placeholder="Ej: ¿Cuáles son mis notas?")

    if st.button("Enviar", type="primary"):
        if pregunta_usuario:
            respuesta, extra = procesar_pregunta(pregunta_usuario)
            st.session_state.chat_history.append({"role": "user", "content": pregunta_usuario})
            st.session_state.chat_history.append({"role": "assistant", "content": respuesta, "extra": extra})
            st.rerun()

    if st.button("🗑️ Limpiar conversación"):
        st.session_state.chat_history = []
        st.rerun()

def mostrar_notas():
    st.title("📊 Mis Notas y Calificaciones")

    cedula = st.session_state.user_data['cedula']
    df_colegio = obtener_df_colegio()
    df_estudiante = df_colegio[df_colegio['Cedula'] == cedula]

    if not df_estudiante.empty:
        st.markdown(f"### 👤 Estudiante: {df_estudiante['Nombre'].iloc[0]}")
        st.markdown(f"🏫 {st.session_state.colegio}")

        st.markdown("---")

        notas_display = df_estudiante[['Asignatura', 'Nota_Parcial', 'Nota_Final']].copy()
        notas_display.columns = ['Asignatura', 'Nota Parcial', 'Nota Final']

        st.markdown("#### 📋 Detalle de Calificaciones")
        st.dataframe(notas_display, hide_index=True, use_container_width=True)

        promedio_parcial = df_estudiante['Nota_Parcial'].mean()
        promedio_final = df_estudiante['Nota_Final'].mean()

        st.markdown("---")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Promedio Parcial", f"{promedio_parcial:.2f}")
        with col2:
            st.metric("📈 Promedio Final", f"{promedio_final:.2f}")
        with col3:
            estado = "✅ Aprobado" if promedio_final >= 6 else "⚠️ En riesgo"
            st.metric("📋 Estado", estado)

        st.markdown("---")
        st.markdown("#### 📈 Gráfico de Rendimiento")

        import plotly.graph_objects as go
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Nota Parcial',
            x=df_estudiante['Asignatura'],
            y=df_estudiante['Nota_Parcial'],
            marker_color='#93c5fd'
        ))
        fig.add_trace(go.Bar(
            name='Nota Final',
            x=df_estudiante['Asignatura'],
            y=df_estudiante['Nota_Final'],
            marker_color='#1d4ed8'
        ))
        fig.update_layout(
            barmode='group',
            title='Comparación de Notas por Asignatura',
            xaxis_title='Asignatura',
            yaxis_title='Nota',
            yaxis_range=[0, 10]
        )
        st.plotly_chart(fig, use_container_width=True)

def mostrar_certificado():
    st.title("📜 Certificado de Estudios")

    st.markdown("""
    Genera y descarga tu certificado de estudios oficial. Este documento certifica 
    tu matrícula activa en la institución educativa.
    """)

    user = st.session_state.user_data
    cedula = user['cedula']
    nombre = user['nombre']
    colegio = user['colegio']

    df_colegio = obtener_df_colegio()
    df_estudiante = df_colegio[df_colegio['Cedula'] == cedula]
    promedio = df_estudiante['Nota_Final'].mean()

    st.markdown("---")

    st.markdown(f"""
    <div class="cert-box">
        <h2 style="text-align: center; color: #1a3a5c;">CERTIFICADO DE ESTUDIOS</h2>
        <h3 style="text-align: center; color: #2c5282;">{colegio.upper()}</h3>
        <hr style="border-color: #c05621;">
        <p style="text-align: justify; font-size: 14px;">
            El/La rector(a) del {colegio}, <strong>CERTIFICA QUE:</strong>
        </p>
        <p style="text-align: center; font-size: 16px;">
            El/La estudiante <strong>{nombre}</strong>, identificado(a) con documento 
            de identidad No. <strong>{cedula}</strong>, se encuentra matriculado(a) 
            y cursando estudios en esta institución educativa durante el año lectivo 2024.
        </p>
        <p style="text-align: center; font-size: 14px;">
            Promedio académico actual: <strong>{promedio:.2f}</strong>
        </p>
        <p style="text-align: center; font-size: 12px; color: #4b5563;">
            Expedido el {datetime.now().strftime('%d de %B de %Y')}
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    pdf_bytes = generar_certificado_pdf(nombre, cedula, colegio, promedio)
    st.download_button(
        label="📥 Descargar Certificado PDF",
        data=pdf_bytes,
        file_name=f"certificado_{nombre.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )

def mostrar_dashboard_stats():
    import plotly.express as px

    st.title("📈 Dashboard de Estadísticas")

    st.markdown("### 📊 Temas Más Consultados")

    consultas_df = pd.DataFrame({
        'Tema': list(st.session_state.consultas.keys()),
        'Consultas': list(st.session_state.consultas.values())
    })

    fig = px.bar(consultas_df, x='Tema', y='Consultas',
                 title='Frecuencia de Consultas por Tema',
                 color='Consultas',
                 color_continuous_scale='Blues')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("### 📚 Promedios por Asignatura (Todos los Estudiantes)")

    df_colegio = obtener_df_colegio()
    promedios_asignatura = df_colegio.groupby('Asignatura')['Nota_Final'].mean().reset_index()

    fig2 = px.pie(promedios_asignatura, values='Nota_Final', names='Asignatura',
                  title='Distribución de Promedios por Asignatura')
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.markdown("### 👥 Ranking de Estudiantes")

    ranking = df_colegio.groupby(['Nombre', 'Cedula'])['Nota_Final'].mean().reset_index()
    ranking = ranking.sort_values('Nota_Final', ascending=False)
    ranking.columns = ['Nombre', 'Cédula', 'Promedio']
    ranking['Posición'] = range(1, len(ranking) + 1)

    st.dataframe(ranking[['Posición', 'Nombre', 'Promedio']], hide_index=True, use_container_width=True)

def mostrar_info_privacidad():
    st.title("🔒 Política de Privacidad")

    st.markdown("""
    ### Tus Datos Están Protegidos

    En nuestra institución nos tomamos muy en serio la protección de tus datos personales.

    #### 📋 Datos que manejamos:
    - Nombre completo
    - Número de identificación
    - Calificaciones académicas
    - Historial de consultas

    #### 🛡️ Cómo protegemos tu información:
    - Acceso solo con autenticación
    - Datos encriptados
    - No compartimos con terceros
    - Cumplimiento de Ley 1581 de 2012

    #### ✅ Tus derechos:
    - Acceder a tu información
    - Corregir datos incorrectos
    - Solicitar eliminación
    - Revocar autorización

    #### 📞 Contacto:
    Para ejercer tus derechos: **protecciondatos@colegio.edu.co**
    """)

# ============================================
# DASHBOARD PROFESOR (EDICIÓN DE NOTAS Y ASISTENCIA)
# ============================================
def mostrar_dashboard_profesor():
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/teacher.png", width=80)
        st.markdown(f"### 👋 ¡Hola, {st.session_state.user_data['nombre']}!")
        st.markdown(f"📚 {st.session_state.user_data['asignatura']}")
        st.markdown(f"🏫 {st.session_state.colegio}")
        st.markdown("---")

        menu = st.radio(
            "📌 Menú",
            ["📊 Ver/Editar Estudiantes", "📈 Estadísticas", "🔒 Privacidad"]
        )

        st.markdown("---")
        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_type = None
            st.session_state.user_data = None
            st.rerun()

    df_colegio = obtener_df_colegio()
    asistencia_df = obtener_asistencia_df()
    asignatura = st.session_state.user_data['asignatura']

    if menu == "📊 Ver/Editar Estudiantes":
        st.title("📊 Lista y Edición de Estudiantes")

        df_asignatura = df_colegio[df_colegio['Asignatura'] == asignatura].copy()

        st.markdown(f"### 📚 Estudiantes de {asignatura}")
        st.markdown("Puedes editar las notas directamente en la tabla y luego pulsar **Guardar cambios**.")

        edited_df = st.data_editor(
            df_asignatura[['Nombre', 'Cedula', 'Nota_Parcial', 'Nota_Final']],
            num_rows="fixed",
            hide_index=True,
            use_container_width=True
        )

        if st.button("💾 Guardar cambios en notas", type="primary"):
            # Actualizar en df_colegio dentro de session_state
            for i, row in edited_df.iterrows():
                mask = (df_colegio['Cedula'] == row['Cedula']) & (df_colegio['Asignatura'] == asignatura)
                df_colegio.loc[mask, 'Nota_Parcial'] = row['Nota_Parcial']
                df_colegio.loc[mask, 'Nota_Final'] = row['Nota_Final']

            # Reasignar al estado
            if st.session_state.colegio == "Colegio Departamental Carlos Giraldo":
                st.session_state.df_cg = df_colegio
            else:
                st.session_state.df_os = df_colegio

            st.success("✅ Notas actualizadas correctamente.")

        st.markdown("---")
        st.markdown("### 📅 Asistencia de Estudiantes (por estudiante, no por asignatura)")

        # Mostrar y permitir editar asistencia global de estudiantes de este colegio
        asis_df = asistencia_df.copy()
        edited_asis = st.data_editor(
            asis_df,
            hide_index=True,
            use_container_width=True
        )

        if st.button("💾 Guardar cambios en asistencia"):
            if st.session_state.colegio == "Colegio Departamental Carlos Giraldo":
                st.session_state.asistencia_cg = edited_asis
            else:
                st.session_state.asistencia_os = edited_asis
            st.success("✅ Asistencias actualizadas correctamente.")

    elif menu == "📈 Estadísticas":
        st.title("📈 Estadísticas de la Clase")

        df_asignatura = df_colegio[df_colegio['Asignatura'] == asignatura]

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Promedio Clase", f"{df_asignatura['Nota_Final'].mean():.2f}")
        with col2:
            st.metric("📈 Nota Máxima", f"{df_asignatura['Nota_Final'].max():.2f}")
        with col3:
            st.metric("📉 Nota Mínima", f"{df_asignatura['Nota_Final'].min():.2f}")

        import plotly.express as px
        st.markdown("#### Distribución de notas finales")
        fig = px.histogram(df_asignatura, x="Nota_Final", nbins=10)
        st.plotly_chart(fig, use_container_width=True)

    elif menu == "🔒 Privacidad":
        mostrar_info_privacidad()

# ============================================
# MAIN APP
# ============================================
def main():
    if not st.session_state.privacy_accepted:
        mostrar_aviso_privacidad()
    elif not st.session_state.logged_in:
        mostrar_login()
    elif st.session_state.user_type == "estudiante":
        mostrar_dashboard_estudiante()
    elif st.session_state.user_type == "profesor":
        mostrar_dashboard_profesor()

if __name__ == "__main__":
    main()
