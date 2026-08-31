import pybullet as p
import pybullet_data
import time
import os

# Iniciar la simulación
p.connect(p.GUI)
p.setGravity(0, 0, -9.8)

# Añadir rutas de búsqueda
p.setAdditionalSearchPath(pybullet_data.getDataPath())  # Ruta por defecto de PyBullet
p.setAdditionalSearchPath(".")  # Directorio actual

# Ruta local del URDF
urdf_path = os.path.join("biped", "biped2d.urdf")

# Verifica si el archivo existe
if not os.path.exists(urdf_path):
    raise FileNotFoundError(f"No se encontró el archivo: {urdf_path}. Asegúrate de tener la carpeta 'biped' y el archivo 'biped2d.urdf'.")

# Cargar el robot
robot = p.loadURDF(urdf_path, [0, 0, 2], useFixedBase=False)

# Configurar control PD
joints = [0, 1, 2, 3]  # Articulaciones
kp = 100
kd = 10
target_angles = [0.5, -0.5, 0.3, -0.3]

# Bucle de simulación
for _ in range(1000):
    for i, joint in enumerate(joints):
        p.setJointMotorControl2(
            robot,
            joint,
            p.POSITION_CONTROL,
            targetPosition=target_angles[i],
            positionGain=kp,
            velocityGain=kd
        )
    p.stepSimulation()
    time.sleep(10/240)
