import pybullet as p
import pybullet_data
import time

# Inicializar simulación
physicsClient = p.connect(p.GUI)  # Usar p.DIRECT para modo sin gráficos
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -10)

# Cargar plano y carro
planeId = p.loadURDF("plane.urdf")
carPos = [0, 0, 0.5]
car = p.loadURDF("cartpole.urdf", carPos, useFixedBase=True)

# Configurar ruedas (simplificado)
wheelIndices = [1, 3]  # Índices de las articulaciones de las ruedas
steeringIndices = [0, 2]  # Articulaciones de dirección

# Simulación
for _ in range(1000):
    # Aplicar fuerzas a las ruedas y dirección
    p.setJointMotorControl2(
        car,
        wheelIndices[0],
        p.VELOCITY_CONTROL,
        targetVelocity=5,
        force=10
    )
    p.setJointMotorControl2(
        car,
        steeringIndices[0],
        p.POSITION_CONTROL,
        targetPosition=0.5
    )
    p.stepSimulation()
    time.sleep(10/240)

p.disconnect()