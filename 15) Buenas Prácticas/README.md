# 15) Buenas prácticas con asyncio en el ESP32

Simulador interactivo de las buenas prácticas finales de asyncio en MicroPython, aplicado a sistemas de robótica actuales.

## ▶ Abrir el simulador

### [👉 Haz clic aquí para abrir el simulador](https://dialejobv.github.io/U_Militar/15)%20Buenas%20Pr%C3%A1cticas/)

Se abre en el navegador; no necesitas instalar nada. Funciona en computador y en celular.

## Qué vas a encontrar

| Pestaña | Contenido |
|---|---|
| 01 Simulador de robótica | Brazo robótico, domótica e inmótica, estación meteorológica, robot AGV e invernadero |
| 02 Las cinco prácticas | Error típico, corrección en MicroPython y equivalente en C++ |
| 03 Estructura de un proyecto real | Archivos de un proyecto en MicroPython y en PlatformIO |
| 04 Verificación y preguntas | Lista de verificación y preguntas para argumentar |

## Cómo usarlo

1. Elige un sistema en la parte superior del simulador.
2. Apaga una buena práctica con su interruptor y observa qué falla en la escena, en la línea de tiempo y en el monitor serie.
3. Revisa el código MicroPython o C++ que se genera con tus ajustes.
4. Responde las preguntas de la pestaña 04 y copia tus respuestas con el botón **Copiar todas mis respuestas**.

## Temas

- Uso de `asyncio.gather()` para organizar las tareas
- Evitar `time.sleep()`
- Diseñar tareas cortas y cooperativas
- Manejo de errores con `try/except` dentro de corrutinas
- Estructura recomendada de un proyecto real
