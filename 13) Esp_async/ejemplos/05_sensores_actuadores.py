# =============================================================
# Ejemplo 5 — Varios sensores y actuadores "en paralelo"
# Placa: ESP32 con MicroPython
# Conexiones:
#   Potenciómetro  -> GPIO34 (ADC)      Servo SG90 -> GPIO18 (PWM 50 Hz)
#   DHT22          -> GPIO4             Buzzer     -> GPIO19 (PWM)
#   LED latido     -> GPIO2 (integrado)
# -------------------------------------------------------------
# Cinco tareas, cada una con SU propio ritmo:
#   servo   cada 50 ms   | dht     cada 2 s  | alarma cada 200 ms
#   latido  cada 1 s     | reporte cada 1 s
# Ninguna espera a las demás.
# =============================================================
import asyncio
from machine import Pin, ADC, PWM
import dht

# ---------- Hardware ----------
pot = ADC(Pin(34))
pot.atten(ADC.ATTN_11DB)                 # rango completo 0–3.3 V
servo = PWM(Pin(18), freq=50)
buzzer = PWM(Pin(19), freq=2000)
buzzer.duty_u16(0)
sensor = dht.DHT22(Pin(4))
led = Pin(2, Pin.OUT)

# ---------- Estado compartido ----------
estado = {"temp": None, "hum": None, "angulo": 0, "alarma": False}
TEMP_MAXIMA = 30.0


def angulo_a_duty(angulo):
    """Convierte 0–180° en pulso de 0.5–2.5 ms dentro de 20 ms."""
    pulso_us = 500 + angulo * 2000 // 180
    return pulso_us * 65535 // 20000


# ---------- Tareas ----------
async def tarea_servo():
    while True:
        lectura = pot.read_u16()                     # 0..65535
        estado["angulo"] = lectura * 180 // 65535
        servo.duty_u16(angulo_a_duty(estado["angulo"]))
        await asyncio.sleep_ms(50)


async def tarea_dht():
    while True:
        try:
            sensor.measure()                          # ~25 ms
            estado["temp"] = sensor.temperature()
            estado["hum"] = sensor.humidity()
        except OSError:
            print("Aviso: no se pudo leer el DHT22")
        await asyncio.sleep(2)                        # el DHT22 pide >= 2 s


async def tarea_alarma():
    while True:
        t = estado["temp"]
        estado["alarma"] = t is not None and t > TEMP_MAXIMA
        if estado["alarma"]:
            buzzer.duty_u16(32768)                    # sonido
            await asyncio.sleep_ms(200)
            buzzer.duty_u16(0)                        # silencio
            await asyncio.sleep_ms(200)
        else:
            buzzer.duty_u16(0)
            await asyncio.sleep_ms(500)


async def tarea_latido():
    # "Señal de vida": si el LED deja de parpadear, algo bloqueó el bucle
    while True:
        led.value(1)
        await asyncio.sleep_ms(100)
        led.value(0)
        await asyncio.sleep_ms(900)


async def tarea_reporte():
    while True:
        print("T={temp} °C  H={hum} %  servo={angulo}°  alarma={alarma}".format(**estado))
        await asyncio.sleep(1)


async def main():
    await asyncio.gather(
        tarea_servo(),
        tarea_dht(),
        tarea_alarma(),
        tarea_latido(),
        tarea_reporte(),
    )


try:
    asyncio.run(main())
finally:
    buzzer.duty_u16(0)
    asyncio.new_event_loop()     # deja el planificador limpio al detener
