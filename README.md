# 🚴 Cycling Dashboard · Strava Stats

Dashboard estático con estadísticas personales de ciclismo exportadas desde Strava, construido en HTML/CSS/JS puro — sin dependencias de servidor ni frameworks.

🔗 **[Ver dashboard en vivo](https://TU-USUARIO.github.io/TU-REPO/cycling-dashboard.html)**

---

## 📸 Vista general

El dashboard incluye:
- **KPIs globales** — distancia total, salidas, horas y desnivel acumulado
- **Tabla + gráfico anual** — comparativa por año con métricas intercambiables (distancia, salidas, horas)
- **Heatmap mensual** — intensidad de actividad mes a mes a lo largo de los años
- **Velocidad promedio por año** — filtrada a salidas ≥ 14 km/h para excluir pausas
- **Récords personales** — ride más largo, más veloz, mayor desnivel y más horas en ruta
- **Widget de Strava** — últimas salidas en tiempo real

---

## 📁 Estructura del repositorio

```
/
├── index.html                  # página principal (existente)
├── cycling-dashboard.html      # dashboard de ciclismo ← este proyecto
├── cycling_data.json           # datos transformados y limpios
└── README.md
```

---

## 🗂 Datos (`cycling_data.json`)

Los datos originales vienen del **export de Strava** (`activities.csv`) y fueron transformados con Python/pandas. El JSON contiene:

| Campo | Descripción |
|---|---|
| `totals` | Totales globales: distancia, salidas, horas, desnivel, calorías |
| `records` | 4 récords personales con detalle de cada salida |
| `by_year` | Resumen anual agregado (8 años: 2016–2024) |
| `by_month` | Distancia y cantidad de salidas por mes/año (51 registros) |

> **Nota:** `vel_avg_filtered` en `by_year` excluye salidas con velocidad promedio < 14 km/h, que generalmente corresponden a salidas cortas, virtuales o con muchas pausas no descontadas.

---

## 🛠 Cómo actualizar los datos

1. Exportá tus datos desde **Strava → Configuración → Mi cuenta → Descargar datos**
2. Extraé `activities.csv` del `.zip`
3. Corré el script de transformación:

```bash
python3 transform.py activities.csv
```

4. Reemplazá `cycling_data.json` y commiteá

---

## 🔧 Tecnologías

- **HTML / CSS / JavaScript** puro — sin frameworks
- **[Chart.js 4.4](https://www.chartjs.org/)** — gráficos de barras y línea
- **Google Fonts** — Bebas Neue + DM Sans + DM Mono
- **Python + pandas** — transformación de datos offline

---

## 📊 Highlights (2016–2024)

| Métrica | Valor |
|---|---|
| Distancia total | **3.957 km** |
| Salidas totales | **266** |
| Horas en ruta | **353 h** |
| Desnivel acumulado | **12.497 m** |
| Año más activo | **2021** (120 salidas · 1.534 km) |
| Ride más largo | **90.4 km** — 2 mayo 2021 |
| Mayor desnivel | **709 m** — 21 dic 2020 |
| Velocidad pico | **30.6 km/h** prom. — 20 feb 2022 |

---

## 📄 Licencia

Datos personales — uso privado.
