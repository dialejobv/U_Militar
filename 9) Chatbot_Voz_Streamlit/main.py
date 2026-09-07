import os
import base64
import requests
import streamlit as st
from gtts import gTTS
from streamlit_mic_recorder import speech_to_text
import time

# Configuración de DeepSeek
DEEPSEEK_API_KEY = ''
DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions'

def enviar_mensaje_deepseek(mensaje, modelo='deepseek-chat'):
    """
    Función para enviar mensajes a la API de DeepSeek
    """
    headers = {
        'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
        'Content-Type': 'application/json'
    }

    data = {
        'model': modelo,
        'messages': [
            {'role': 'system', 'content': 'Eres un asistente útil y amigable. Responde de manera concisa pero completa.'},
            {'role': 'user', 'content': mensaje}
        ],
        'temperature': 0.7,
        'max_tokens': 1000
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
        
        if response.status_code != 200:
            error_detail = response.json() if response.text else "Sin detalles"
            return f"Error {response.status_code}: {error_detail}"
        
        return response.json()['choices'][0]['message']['content']
    
    except requests.exceptions.RequestException as e:
        return f"Error de conexión: {e}"
    except Exception as e:
        return f"Error Inesperado: {e}"

# Configuración de la interfaz de Streamlit
st.set_page_config(page_title="Tutor IA Voz con DeepSeek", page_icon="🎙️")
st.title("🎙️ Tutor IA con Voz - DeepSeek")
st.write("¡Pregunta lo que quieras usando tu voz o escribiendo!")

# Verificar que la API key funciona al inicio
with st.spinner("Verificando conexión con DeepSeek..."):
    test_response = enviar_mensaje_deepseek("Hola")
    if "Error" in test_response:
        st.error(f"⚠️ {test_response}")
        st.warning("Por favor, verifica tu API Key en https://platform.deepseek.com/")
        st.stop()

# Inicializar variables de sesión
if "messages" not in st.session_state:
    st.session_state.messages = []
if "audio_played" not in st.session_state:
    st.session_state.audio_played = False
if "last_response" not in st.session_state:
    st.session_state.last_response = ""

# Mostrar mensajes anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --- OPCIÓN 1: Entrada por voz ---
st.subheader("🎤 Entrada por Voz")
text = speech_to_text(
    language="es", 
    use_container_width=True, 
    just_once=True, 
    key="STT",
    start_prompt="🎤 Haz clic para hablar",
    stop_prompt="⏹️ Detener grabación"
)

# --- OPCIÓN 2: Entrada por texto ---
st.subheader("⌨️ Entrada por Texto")
user_input = st.chat_input("Escribe tu pregunta aquí...")

# Procesar entrada de voz o texto
input_text = text or user_input

if input_text:
    # Si es entrada por voz, añadir mensaje del usuario
    if text:
        with st.chat_message("user"):
            st.write(text)
        st.session_state.messages.append({"role": "user", "content": text})
        mensaje_usuario = text
    # Si es entrada por texto
    elif user_input:
        with st.chat_message("user"):
            st.write(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        mensaje_usuario = user_input
    
    # Obtener respuesta de DeepSeek
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            response_text = enviar_mensaje_deepseek(mensaje_usuario)
            
            # Mostrar respuesta en texto
            st.write(response_text)
            
            # Guardar en el historial
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            st.session_state.last_response = response_text
            st.session_state.audio_played = False
    
    # --- MEJORADA: Generación y reproducción de audio ---
    try:
        # Crear el archivo de audio
        tts = gTTS(response_text, lang='es', slow=False)
        audio_path = "respuesta.mp3"
        tts.save(audio_path)
        
        # Leer el archivo de audio
        with open(audio_path, "rb") as audio_file:
            audio_bytes = audio_file.read()
        
        # Opción 1: Usar el componente de audio de Streamlit (más confiable)
        st.audio(audio_bytes, format="audio/mp3")
        
        # Opción 2: Auto-reproducción con HTML (funciona en algunos navegadores)
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
        
        # Crear un contenedor para el audio
        audio_container = st.empty()
        
        # HTML con reproducción automática
        audio_html = f"""
        <div style="display: flex; justify-content: center; margin: 10px 0;">
            <audio id="audio-player" controls autoplay style="width: 100%; max-width: 500px;">
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                Tu navegador no soporta audio.
            </audio>
        </div>
        <script>
            // Intentar reproducir automáticamente
            document.addEventListener('DOMContentLoaded', function() {{
                var audio = document.getElementById('audio-player');
                if (audio) {{
                    audio.play().catch(function(error) {{
                        console.log('Reproducción automática bloqueada:', error);
                    }});
                }}
            }});
        </script>
        """
        
        # Mostrar el reproductor de audio mejorado
        audio_container.markdown(audio_html, unsafe_allow_html=True)
        
        # Eliminar el archivo temporal después de un tiempo
        time.sleep(1)
        try:
            os.remove(audio_path)
        except:
            pass
        
    except Exception as e:
        st.error(f"Error al generar el audio: {e}")
        st.info("💡 Puedes leer la respuesta en el texto mostrado arriba.")

# --- MEJORADO: Botón para repetir el audio ---
if st.session_state.last_response and st.button("🔊 Repetir respuesta"):
    try:
        tts = gTTS(st.session_state.last_response, lang='es', slow=False)
        audio_path = "respuesta_repetida.mp3"
        tts.save(audio_path)
        
        with open(audio_path, "rb") as audio_file:
            audio_bytes = audio_file.read()
        
        st.audio(audio_bytes, format="audio/mp3")
        
        # Reproducción automática con HTML
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
        st.markdown(f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
        """, unsafe_allow_html=True)
        
        os.remove(audio_path)
    except Exception as e:
        st.error(f"Error al generar el audio: {e}")

# --- MEJORADO: Botón para limpiar el historial ---
col1, col2 = st.columns(2)
with col1:
    if st.button("🗑️ Limpiar conversación"):
        st.session_state.messages = []
        st.session_state.last_response = ""
        st.rerun()

with col2:
    if st.button("🔄 Reiniciar aplicación"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

# --- MEJORADO: Instrucciones para el usuario ---
with st.expander("ℹ️ Instrucciones de uso", expanded=True):
    st.write("""
    ### 🎯 Cómo usar el chatbot:
    
    1. **Entrada por voz**: 
       - Haz clic en el botón 🎤 y habla claramente
       - La grabación se detiene automáticamente después de hablar
    
    2. **Entrada por texto**:
       - Escribe tu pregunta en el campo de texto
       - Presiona Enter para enviar
    
    3. **Escuchar la respuesta**:
       - El audio se reproduce automáticamente
       - Puedes usar el botón 🔊 para repetir la respuesta
       - También puedes leer la respuesta en el chat
    
    4. **Consejos**:
       - Habla cerca del micrófono
       - Evita ruidos de fondo
       - Las preguntas claras obtienen mejores respuestas
    """)