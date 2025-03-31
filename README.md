InsightOrbit - Monitoreo de Participación en WarRooms (Google Meet)

Este repositorio contiene diversas soluciones desarrolladas para el equipo de NOC de MELI, con el objetivo de obtener los nombres de los colaboradores más activos en WarRooms (Google Meet). Esta información es utilizada para completar automáticamente los canales de Slack creados por cada incidente.

🚀 Soluciones Implementadas

🔹 Solución 1: Logeo Automático con Selenium

Esta solución consistía en loguear un usuario extra en la reunión, que interactuaba con la lista de participantes para extraer los nombres.

❌ Inconvenientes:

Requiere ejecución programada mediante el Programador de Tareas de Windows en horario laboral.

No discrimina entre participantes más y menos activos.

Alto consumo de recursos.

La necesidad de loguear un usuario adicional en la reunión se consideró insegura e invasiva.

🔴 Estado: Descartado (aunque el código fue completado).

🔹 Solución 2: Extracción de Texto desde Google Meet (OCR)

Esta solución procesaba el video de la videollamada, eliminaba los FPS irrelevantes y aplicaba OCR para extraer los nombres.

❌ Inconvenientes:

Solo procesaba los videos de forma local.

Distinguía la participación basándose en la frecuencia con la que aparecían los nombres en los FPS (baja precisión).

Almacenamiento de videos en Google Drive: No era legal almacenarlos localmente, por lo que la solución fue descartada rápidamente.

🔴 Estado: Descartado (aunque el código fue completado).

🔹 Solución 3: Dictado por Voz En esta alternativa, el Operador/Administrador de la WarRoom debía dictar manualmente los nombres de los participantes más activos mientras realizaba su trabajo.

❌ Inconvenientes:

Subjetividad: La precisión dependía del criterio del operador.

Posibles errores: Si el operador se distraía, podía omitir nombres importantes o agregar nombres irrelevantes.

Requería ejecución programada mediante el Programador de Tareas de Windows en horario laboral.

Dependía del tono, cadencia y volumen de voz para que la biblioteca spaCy pudiera extraer correctamente los nombres (baja precisión).

🔴 Estado: Descartado (aunque el código fue completado).

✅ Solución Final: InsightOrbit (Extensión de Google Chrome)

Después de evaluar las soluciones anteriores, desarrollé una extensión de Google Chrome que interactúa directamente con el DOM de Google Meet, permitiendo:

🎯 Características Principales:

✔️ Obtención automática de nombres, separando los más activos en función de su tiempo de habla (alta precisión).

✔️ Bajo consumo de recursos: Utiliza observadores compartidos para detectar cambios de estilo en los micrófonos digitales de cada usuario.

✔️ Envío automático a Slack: Extrae datos del incidente desde el JSON de la ticketera y los envía a Slack mediante WebHook.

✔️ Fácil portabilidad: Al ser una extensión de Chrome, puede ejecutarse desde cualquier dispositivo sin instalación compleja.

✔️ Interfaz intuitiva: Permite filtrar nombres y visualizar un cronómetro adjunto a cada participante, indicando su tiempo de habla.

⚠️ Único Inconveniente:

El monitoreo del micrófono digital para detectar el tiempo de habla no funciona en segundo plano. El operador debe mantener la reunión de Google Meet visible en la pantalla.

🔵 Estado: Implementado con éxito. 🎉

📌 Conclusión InsightOrbit es la solución más eficiente y precisa para identificar a los participantes más activos en una WarRoom de Google Meet, optimizando la administración de incidentes en Slack con mínima intervención humana y bajo consumo de recursos.
