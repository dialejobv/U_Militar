import streamlit as st
import pybullet as p
import pybullet_data
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

st.set_page_config(layout="wide")  # Para que la visualización sea más grande
st.title("Simulación de PyBullet en Streamlit con Visualización")

# Iniciar la simulación en modo DIRECT (sin GUI)
physicsClient = p.connect(p.DIRECT)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -10)

# Cargar el plano y un objeto (una caja)
planeId = p.loadURDF("plane.urdf")
startPos = [0, 0, 3]  # Empezar a 3 metros de altura
startOrientation = p.getQuaternionFromEuler([0, 0, 0])
boxId = p.loadURDF("cube_small.urdf", startPos, startOrientation)

# Configurar la cámara para ver la escena
cameraDistance = 5.0
cameraYaw = 50
cameraPitch = -35
cameraTargetPosition = [0, 0, 1.5]

# Listas para guardar los datos
tiempos = []
alturas = []
imagenes = []  # Para guardar los fotogramas

st.write("Ejecutando simulación y capturando fotogramas...")

num_pasos = 100  # Puedes ajustar este número
for i in range(num_pasos):
    p.stepSimulation()
    
    # Obtener la posición de la caja
    pos, orn = p.getBasePositionAndOrientation(boxId)
    
    # Guardar el tiempo y la altura (coordenada Z)
    tiempos.append(i * (1./240.))
    alturas.append(pos[2])
    
    # Renderizar la escena en un fotograma (imagen)
    # getCameraImage devuelve: ancho, alto, rgb, depth, seg
    width, height, rgbImg, depthImg, segImg = p.getCameraImage(
        width=640,
        height=480,
        viewMatrix=p.computeViewMatrixFromYawPitchRoll(
            cameraTargetPosition=cameraTargetPosition,
            distance=cameraDistance,
            yaw=cameraYaw,
            pitch=cameraPitch,
            roll=0,
            upAxisIndex=2
        ),
        projectionMatrix=p.computeProjectionMatrixFOV(
            fov=60,
            aspect=640/480,
            nearVal=0.1,
            farVal=100.0
        ),
        renderer=p.ER_TINY_RENDERER  # Usar el renderizador por software
    )
    
    # Convertir el array de píxeles a una imagen de PIL
    img = np.reshape(rgbImg, (height, width, 4))[:, :, :3]  # Descartar el canal alpha
    img = Image.fromarray(img.astype(np.uint8))
    imagenes.append(img)

p.disconnect()
st.write(f"Simulación terminada. Se capturaron {len(imagenes)} fotogramas.")

# --- Mostrar la visualización en Streamlit ---

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Visualización de la Simulación")
    # Mostrar la animación
    # Streamlit no tiene un reproductor de video nativo, pero podemos mostrar los frames uno tras otro
    # Para una animación simple, podemos usar st.image con un slider o mostrarlos en secuencia
    frame_idx = st.slider("Fotograma", 0, len(imagenes)-1, 0)
    st.image(imagenes[frame_idx], caption=f"Frame {frame_idx}", use_container_width=True)

with col2:
    st.subheader("Gráfico de Altura")
    fig, ax = plt.subplots()
    ax.plot(tiempos, alturas, label="Altura de la caja (Z)")
    ax.set_xlabel("Tiempo (s)")
    ax.set_ylabel("Altura (m)")
    ax.set_title("Caída Libre de la Caja")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
    
    st.subheader("Datos de la Simulación")
    st.write(f"Altura final: {alturas[-1]:.2f} m")
    st.write(f"Tiempo total: {tiempos[-1]:.2f} s")