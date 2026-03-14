"""
transform.py — Strava Cycling Dashboard
========================================
Transforma el archivo activities.csv exportado desde Strava
en el JSON limpio que consume cycling-dashboard.html.

Uso:
    python3 transform.py activities.csv
    python3 transform.py activities.csv --output mi_data.json
    python3 transform.py activities.csv --min-speed 12

Requisitos:
    pip install pandas
"""

import sys
import json
import re
import argparse
import pandas as pd
from pathlib import Path


# ── Configuración ─────────────────────────────────────────────────────────────

MESES_ES = {
    'ene':1,'feb':2,'mar':3,'abr':4,'may':5,'jun':6,
    'jul':7,'ago':8,'sep':9,'oct':10,'nov':11,'dic':12
}

BIKE_KEYWORDS = ['ciclista', 'ride', 'bici']

DEFAULT_MIN_SPEED = 14.0  # km/h — umbral para filtrar el promedio de velocidad


# ── Helpers ───────────────────────────────────────────────────────────────────

def parse_date(s: str) -> pd.Timestamp:
    """Parsea fechas en español del estilo '26 ago 2020, 10:38:41 p.m.'"""
    s = str(s).lower()
    m = re.search(r'(\d+)\s+(\w+)\s+(\d{4})', s)
    if m:
        d, mo, y = m.groups()
        month_num = MESES_ES.get(mo[:3])
        if month_num:
            return pd.Timestamp(year=int(y), month=month_num, day=int(d))
    return pd.NaT


def fmt_ride(row: pd.Series) -> dict:
    """Convierte una fila de actividad a dict de récord."""
    return {
        'nombre':      str(row.get('nombre', '')),
        'fecha':       str(row['fecha'].date()) if pd.notna(row['fecha']) else '',
        'dist_km':     round(float(row['dist_km']),  1) if pd.notna(row['dist_km'])  else 0,
        'vel_avg_kmh': round(float(row['vel_avg_kmh']), 1) if pd.notna(row['vel_avg_kmh']) else 0,
        'vel_max_kmh': round(float(row['vel_max_kmh']), 1) if pd.notna(row['vel_max_kmh']) else 0,
        'tiempo_h':    round(float(row['tiempo_h']),  2) if pd.notna(row['tiempo_h'])  else 0,
        'desnivel_m':  round(float(row['desnivel']),  0) if pd.notna(row['desnivel'])  else 0,
    }


# ── Pipeline principal ────────────────────────────────────────────────────────

def transform(input_path: str, output_path: str, min_speed: float) -> None:

    print(f"📂 Leyendo {input_path} ...")
    df = pd.read_csv(input_path)
    print(f"   {len(df)} actividades totales encontradas.")

    # Filtrar solo ciclismo
    pattern = '|'.join(BIKE_KEYWORDS)
    bike = df[df['Tipo de actividad'].str.contains(pattern, case=False, na=False)].copy()
    print(f"   {len(bike)} salidas en bici detectadas.")

    if len(bike) == 0:
        print("❌ No se encontraron actividades de ciclismo. Verificá el archivo.")
        sys.exit(1)

    # Parsear fechas
    bike['fecha']       = bike['Fecha de la actividad'].apply(parse_date)
    bike['año']         = bike['fecha'].dt.year
    bike['mes']         = bike['fecha'].dt.month

    # Convertir unidades
    bike['dist_km']     = pd.to_numeric(bike['Distancia'],           errors='coerce')
    bike['tiempo_h']    = pd.to_numeric(bike['Tiempo transcurrido'], errors='coerce') / 3600
    bike['vel_avg_kmh'] = pd.to_numeric(bike['Velocidad promedio'],  errors='coerce') * 3.6
    bike['vel_max_kmh'] = pd.to_numeric(bike['Velocidad máxima'],    errors='coerce') * 3.6
    bike['desnivel']    = pd.to_numeric(bike['Desnivel positivo'],   errors='coerce')
    bike['calorias']    = pd.to_numeric(bike['Calorías'],            errors='coerce')
    bike['nombre']      = bike['Nombre de la actividad']

    # ── Totales globales
    totals = {
        'total_dist_km':    round(float(bike['dist_km'].sum()), 1),
        'total_rides':      int(len(bike)),
        'total_tiempo_h':   round(float(bike['tiempo_h'].sum()), 1),
        'total_desnivel_m': int(bike['desnivel'].sum()),
        'total_calorias':   int(bike['calorias'].sum()),
        'years_active':     sorted([int(y) for y in bike['año'].dropna().unique()]),
    }

    # ── Récords
    records = {
        'longest_ride':   fmt_ride(bike.loc[bike['dist_km'].idxmax()]),
        'most_elevation': fmt_ride(bike.loc[bike['desnivel'].idxmax()]),
        'longest_time':   fmt_ride(bike.loc[bike['tiempo_h'].idxmax()]),
    }
    fast = bike[bike['vel_avg_kmh'] >= min_speed]
    if len(fast) > 0:
        records['fastest_ride'] = fmt_ride(fast.loc[fast['vel_avg_kmh'].idxmax()])
    else:
        records['fastest_ride'] = {}

    # ── Por año (todas las salidas)
    by_year_all = bike.groupby('año').agg(
        rides        = ('dist_km', 'count'),
        dist_total   = ('dist_km', 'sum'),
        tiempo_total = ('tiempo_h', 'sum'),
        vel_avg      = ('vel_avg_kmh', 'mean'),
        desnivel_total = ('desnivel', 'sum'),
        calorias_total = ('calorias', 'sum'),
    ).reset_index().round(1)

    # Velocidad filtrada (>= min_speed)
    vel_filt = (
        bike[bike['vel_avg_kmh'] >= min_speed]
        .groupby('año')
        .agg(vel_avg_filtered=('vel_avg_kmh','mean'),
             rides_filtered=('vel_avg_kmh','count'))
        .reset_index()
        .round(1)
    )
    by_year = by_year_all.merge(vel_filt, on='año', how='left')
    by_year_list = by_year.to_dict(orient='records')
    # Limpiar NaN → None para JSON válido
    for row in by_year_list:
        for k, v in row.items():
            if pd.isna(v):
                row[k] = None

    # ── Por mes
    by_month = (
        bike.groupby(['año','mes'])
        .agg(dist=('dist_km','sum'), rides=('dist_km','count'))
        .reset_index()
        .round(1)
        .to_dict(orient='records')
    )

    # ── Ensamblar output
    output = {
        'meta': {
            'source':             Path(input_path).name,
            'sport':              'cycling',
            'generated':          pd.Timestamp.now().strftime('%Y-%m-%d'),
            'note_vel_filtered':  f'vel_avg_filtered only includes rides with avg speed >= {min_speed} km/h',
            'min_speed_filter':   min_speed,
        },
        'totals':   totals,
        'records':  records,
        'by_year':  by_year_list,
        'by_month': by_month,
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Listo! Datos guardados en: {output_path}")
    print(f"   📅 Años: {totals['years_active']}")
    print(f"   🚴 Salidas: {totals['total_rides']} · {totals['total_dist_km']} km · {totals['total_tiempo_h']}h")
    print(f"   ⛰  Desnivel total: {totals['total_desnivel_m']} m")


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Transforma activities.csv de Strava → cycling_data.json'
    )
    parser.add_argument('input',
        help='Ruta al archivo activities.csv exportado de Strava')
    parser.add_argument('--output', '-o', default='cycling_data.json',
        help='Nombre del archivo JSON de salida (default: cycling_data.json)')
    parser.add_argument('--min-speed', '-s', type=float, default=DEFAULT_MIN_SPEED,
        help=f'Velocidad mínima en km/h para el promedio filtrado (default: {DEFAULT_MIN_SPEED})')

    args = parser.parse_args()
    transform(args.input, args.output, args.min_speed)
