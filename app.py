import streamlit as st
import requests
import json

# Configuración de la página para optimizar en móviles
st.set_page_config(
    page_title="Dudas y dificultades del español",
    page_icon="🗨️",
    layout="centered",  # Centra el contenido en la pantalla
    initial_sidebar_state="collapsed"  # Oculta la barra lateral inicialmente
)

# Título de la aplicación
st.title("🗨️ Dudas y dificultades del español")

# Barra lateral con información (opcional)
st.sidebar.header("Acerca de esta aplicación")
st.sidebar.markdown("""
Bienvenido al **chatbot de Dudas y dificultades del español**. Este asistente utiliza el modelo `klusterai/Meta-Llama-3.3-70B-Instruct-Turbo` para responder tus preguntas sobre gramática, sintaxis, literatura y otros aspectos relacionados con el idioma español.

### ¿Cómo funciona?  
1. Escribe tu consulta en el campo de texto.  
2. Presiona el botón **"Enviar"**.  
3. Recibe una respuesta detallada sobre tus dudas del idioma.

---

### Autor:
**Moris Polanco**  
Miembro de la **Academia Guatemalteca de la Lengua**.
""")

# Instrucciones para el usuario
st.markdown("""
### Instrucciones:
Escribe tu consulta sobre el idioma español en el cuadro de texto a continuación y presiona el botón **"Enviar"** para recibir una respuesta detallada.
""")

# Inicializar el historial de chat en session_state si no existe
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Mostrar el historial de chat
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del usuario
user_query = st.chat_input("📝 Escribe tu consulta sobre el idioma español:")

# Botón para enviar la consulta
if user_query:
    # Agregar la consulta del usuario al historial de chat
    st.session_state.chat_history.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.spinner("🔄 Procesando tu consulta..."):
        try:
            # Recuperar la clave de API desde los secretos
            api_key = st.secrets["klusterai"]["api_key"]  # Asegúrate de tener la clave API en Streamlit secrets

            # Crear el prompt y el payload para la solicitud
            system_prompt = """
            Contexto:
            Eres un renombrado lingüista y académico del español con más de dos décadas de experiencia en la enseñanza, investigación y asesoramiento sobre el idioma español. Tienes un conocimiento profundo de las complejidades lingüísticas del español, sus dialectos y su evolución. Estás bien versado en las pautas y recomendaciones oficiales de la Real Academia Española (RAE) y la Fundación del Español Urgente (Fundéu). Se te busca frecuentemente para aclarar dudas complejas sobre el uso del lenguaje y resolver disputas relacionadas con la gramática, sintaxis, estilo y uso del español.

            Rol:
            Eres un experto líder en lingüística del español, con un sólido historial en enseñanza, investigación y oratoria. Posees un conocimiento intrincado de la gramática, sintaxis, semántica y pragmática del español. Has escrito varios libros y artículos académicos sobre el tema y has contribuido a revistas lingüísticas prestigiosas. Hablas español e inglés de forma fluida y puedes comunicar conceptos lingüísticos complejos tanto a hablantes nativos como no nativos del español.

            Acción:
            1. Responde preguntas relacionadas con gramática, sintaxis, semántica y pragmática del español.
            2. Proporciona ejemplos prácticos y claros.
            3. Ofrece recomendaciones basadas en la RAE y Fundéu.
            """

            # Construir el payload
            payload = {
                "model": "klusterai/Meta-Llama-3.3-70B-Instruct-Turbo",
                "max_completion_tokens": 1000,
                "temperature": 0.8,
                "top_p": 1,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ]
            }

            # Definir los encabezados de la solicitud
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            # Realizar la solicitud a la API de Kluster.ai
            response = requests.post(
                "https://api.kluster.ai/v1/chat/completions",
                headers=headers,
                json=payload
            )

            # Manejar la respuesta de la API
            if response.status_code == 200:
                response_data = response.json()
                message = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
                if message:
                    # Agregar la respuesta del chatbot al historial de chat
                    st.session_state.chat_history.append({"role": "assistant", "content": message})
                    with st.chat_message("assistant"):
                        st.markdown(message)
                else:
                    st.error("⚠️ La respuesta del chatbot no contiene contenido.")
            else:
                st.error(f"⚠️ Error en la solicitud: {response.status_code}")
                st.error(f"Detalles: {response.text}")

        except Exception as e:
            st.error(f"❌ Ocurrió un error: {e}")

# Footer con Copyright y enlace
st.markdown(
    """
    <div style="text-align: center; margin-top: 50px; font-size: 0.9em; color: #666;">
        <p>Copyright © 2025 <a href="https://hablemosbien.org" target="_blank">Hablemos bien</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
