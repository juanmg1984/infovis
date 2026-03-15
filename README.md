# 🚴 Dos ruedas, muchos datos
### Visualización de datos personales · ECD 2025

Exploración visual de 266 salidas en bicicleta registradas en Strava entre 2016 y 2024. El proyecto toma datos personales exportados de una app de actividad física y los transforma en cuatro visualizaciones que cuentan una historia: hábitos, evolución, clima y el paso del tiempo.

🔗 **[Ver proyecto en vivo](https://TU-USUARIO.github.io/TU-REPO/index_tp.html)**

---

## 📁 Archivos del proyecto

```
/
├── index_tp.html                     # Página principal del proyecto
├── README.md                         # Este archivo
│
├── datos/
│   ├── activities.csv                # Export original de Strava (no incluido por privacidad)
│   ├── datawrapper_vel_multiples.csv # Datos para DataWrapper
│   ├── raw_rawgraphs_beeswarm.csv    # Datos para RAWGraphs
│   ├── flourish_scatter.csv          # Datos para Flourish
│   └── tableau_heatmap.csv           # Datos para Tableau
│
└── beeswarm_final.svg                # Visualización RAWGraphs exportada y editada
```

---

## 🗂 De dónde vienen los datos

Strava permite exportar el historial completo de actividades desde **Configuración → Mi cuenta → Descargar datos**. El archivo descargado es un `.zip` que contiene, entre otras cosas, un archivo llamado `activities.csv` con una fila por cada actividad registrada.

Ese archivo fue el punto de partida de todo el proyecto. Contiene información como la fecha de cada salida, la distancia recorrida, la duración, la velocidad promedio y máxima, el desnivel, las calorías y —en algunos registros más recientes— datos climáticos capturados automáticamente por la app **klimat.app** al momento de la salida: temperatura, velocidad del viento, ráfagas y condición del cielo.

---

## 🔄 Cómo transformamos los datos para cada visualización

### 1 · DataWrapper — *¿En qué meses pedaleo más?*

El archivo original tiene una fila por salida con su fecha exacta. Para este gráfico necesitábamos ver el **tiempo total por mes**, agrupado por año, de forma que cada año fuera una columna independiente.

El proceso fue:
- Convertir la fecha (que venía en formato de texto en español, como "26 ago 2020") a un formato numérico legible
- Sumar todas las horas de cada mes para cada año
- Reorganizar la tabla: en lugar de una fila por salida, una fila por mes (Ene a Dic) y una columna por año (2016, 2017, 2018, 2020, 2021, 2022, 2023, 2024)
- Los meses sin actividad quedaron vacíos — en el gráfico eso se ve como la ausencia de barra, que también cuenta la historia

El resultado es una tabla de 12 filas × 9 columnas que DataWrapper puede leer directamente para armar el gráfico de columnas múltiples.

---

### 2 · RAWGraphs — *¿Qué tan lejos fui según el día de la semana?*

Para el beeswarm necesitábamos una fila por salida con varias dimensiones: cuándo fue, qué día de la semana, cuánto recorrí y a qué ritmo.

El proceso fue:
- Filtrar y eliminar las salidas con menos de 1 km (registros erróneos o pruebas del dispositivo)
- Convertir las fechas al formato `YYYY-MM` que RAWGraphs requiere para el eje temporal
- Traducir los días de la semana al español (lunes, martes, etc.) para que el gráfico se leyera correctamente
- Calcular la velocidad promedio en km/h (el original viene en m/s)
- Crear una columna de **categoría de velocidad** con cuatro niveles: Lenta, Normal, Rápida y Muy rápida, según umbrales definidos a partir de la distribución real de los datos

La visualización se exportó desde RAWGraphs como SVG y luego se editó manualmente en Inkscape para agregar el título, las anotaciones narrativas (el gap de 2018–2019, la pandemia de 2020, el robo de 2024) y adaptar la paleta de colores al estilo visual del proyecto.

---

### 3 · Flourish — *¿El viento me frena?*

Este gráfico explora la relación entre el viento y la velocidad. Los datos climáticos estaban disponibles en las salidas capturadas por klimat.app, identificadas a partir de los títulos de los rides y la presencia de datos en las columnas de clima del CSV.

El proceso fue:
- Filtrar únicamente las salidas que tenían datos de viento registrados
- Aplicar el mismo filtro de calidad que en el beeswarm: solo salidas con más de 1 km y velocidad promedio mayor a 14 km/h (para excluir registros donde el GPS no descontó las pausas)
- Agregar una columna con el **año** de cada salida, para poder colorear los puntos por año en Flourish
- Agregar una columna de **categoría de distancia** (corta, media, larga, muy larga) como dimensión adicional de exploración
- El resultado fue un scatter donde cada punto es una salida, el eje X muestra el viento y el eje Y la velocidad

La correlación entre viento y velocidad resultó ser de **-0.66**: a mayor viento, menor velocidad promedio. 2021 se destaca como el año con mejor desempeño.

---

### 4 · Tableau — *¿Cuándo salgo a rodar?*

Para el heatmap de día × hora necesitábamos saber exactamente a qué hora del día se realizó cada salida.

El proceso fue:
- Extraer la hora de inicio de cada actividad (que venía incluida en el campo de fecha del CSV)
- Traducir los días de la semana al español y asignarles un orden lógico (lunes a domingo)
- Agrupar las salidas por combinación de **día de la semana + hora**, sumando la cantidad de rides y calculando la distancia promedio y total para cada celda
- El resultado es una tabla donde cada fila es una combinación única de día y hora, con la información necesaria para colorear el heatmap

El cuadro más intenso del heatmap es el domingo a las 12 hs: 25 salidas concentradas en ese momento, con las distancias promedio más largas del registro.

---

## 📊 Herramientas utilizadas

| Herramienta | Uso |
|---|---|
| **Python + pandas** | Transformación y limpieza de datos |
| **RAWGraphs** | Beeswarm plot |
| **Inkscape** | Edición y anotaciones del SVG |
| **DataWrapper** | Gráfico de columnas múltiples |
| **Flourish** | Scatter plot con regresión |
| **Tableau Public** | Heatmap interactivo |

---

## 📅 Entregas

| Fecha | Entrega |
|---|---|
| 2026-03-20 | Prototipo navegable en GitHub Pages |
| 2026-03-28 | Versión final + presentación oral (10 min) |

---

*Datos exportados de Strava · Proyecto individual · ECD 2025*
