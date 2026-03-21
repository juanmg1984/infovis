import json
import os

notebook_path = r"c:\Users\Administrador\OneDrive\Escritorio\MCD\Visualización de la información\Tp1\V2 page\infovis\data360_exploration.ipynb"

# Check if file exists
if not os.path.exists(notebook_path):
    print(f"Error: {notebook_path} not found.")
    exit(1)

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Update cell 9 (index 8) - Imports
nb['cells'][8]['source'] = [
    "import requests\n",
    "import pandas as pd\n",
    "import duckdb\n",
    "import altair as alt\n",
    "import json\n",
    "\n",
    "# Configuración base\n",
    "BASE_URL = \"https://data360api.worldbank.org/data360\"\n",
    "# alt.renderers.enable('colab') # Descomentar si se usa en Google Colab"
]

# Update cell 14 (index 13) - Population Plot
nb['cells'][13]['source'] = [
    "def get_indicator_data(indicator, countries):\n",
    "    url = f\"{BASE_URL}/data\"\n",
    "    params = {\"DATABASE_ID\": \"WB_WDI\", \"INDICATOR\": indicator, \"REF_AREA\": \",\".join(countries)}\n",
    "    resp = requests.get(url, params=params).json()\n",
    "    df = pd.DataFrame(resp['value'])\n",
    "    df['OBS_VALUE'] = pd.to_numeric(df['OBS_VALUE'])\n",
    "    df['TIME_PERIOD'] = pd.to_numeric(df['TIME_PERIOD'])\n",
    "    return df\n",
    "\n",
    "df_cono_sur = get_indicator_data(\"WB_WDI_SP_POP_TOTL\", [\"ARG\", \"CHL\", \"URY\", \"BRA\"])\n",
    "\n",
    "# Uso de DuckDB para filtrar o procesar si fuera necesario\n",
    "df_filtered = duckdb.query(\"SELECT * FROM df_cono_sur WHERE TIME_PERIOD >= 1960\").df()\n",
    "\n",
    "# Visualización interactiva con Altair\n",
    "line_chart = alt.Chart(df_filtered).mark_line(point=True).encode(\n",
    "    x=alt.X('TIME_PERIOD:O', title='Año'),\n",
    "    y=alt.Y('OBS_VALUE:Q', title='Población', scale=alt.Scale(type='log')),\n",
    "    color=alt.Color('REF_AREA:N', title='País'),\n",
    "    tooltip=['REF_AREA', 'TIME_PERIOD', 'OBS_VALUE']\n",
    ").properties(\n",
    "    title='Población Total en el Cono Sur (1960-2023)',\n",
    "    width=600,\n",
    "    height=300\n",
    ").interactive()\n",
    "\n",
    "line_chart"
]

# Update cell 25 (index 24) - PCA Execution and Interactive Plot
nb['cells'][24]['source'] = [
    "from sklearn.preprocessing import StandardScaler\n",
    "from sklearn.decomposition import PCA\n",
    "\n",
    "# 1. Manejo de Valores Faltantes\n",
    "df_pca_cleaned = df_pca_input.dropna(axis=1, how='all')\n",
    "df_pca_cleaned = df_pca_cleaned.dropna(axis=0)\n",
    "\n",
    "print(f\"DataFrame después de manejar valores faltantes: {df_pca_cleaned.shape[0]} países, {df_pca_cleaned.shape[1]} indicadores.\")\n",
    "\n",
    "if df_pca_cleaned.empty or df_pca_cleaned.shape[1] < 2:\n",
    "    print(\"No hay suficientes datos o indicadores después de la limpieza para realizar PCA.\")\n",
    "else:\n",
    "    # 2. Escalado y PCA\n",
    "    scaler = StandardScaler()\n",
    "    scaled_data = scaler.fit_transform(df_pca_cleaned)\n",
    "    \n",
    "    pca = PCA(n_components=2)\n",
    "    principal_components = pca.fit_transform(scaled_data)\n",
    "    \n",
    "    pca_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'], index=df_pca_cleaned.index).reset_index()\n",
    "    \n",
    "    # Recuperar algunos indicadores para los tooltips usando DuckDB\n",
    "    original_data = df_pca_cleaned.reset_index()\n",
    "    # Unimos con DuckDB para demostrar su uso\n",
    "    pca_final = duckdb.query(\"SELECT p.*, o.* EXCLUDE (REF_AREA) FROM pca_df p JOIN original_data o ON p.REF_AREA = o.REF_AREA\").df()\n",
    "\n",
    "    # 3. Visualización Interactiva con Altair\n",
    "    selection = alt.selection_point(fields=['REF_AREA'], on='click')\n",
    "    \n",
    "    chart = alt.Chart(pca_final).mark_circle(size=100).encode(\n",
    "        x=alt.X('PC1:Q', title=f'PC1 ({pca.explained_variance_ratio_[0]*100:.2f}%)'),\n",
    "        y=alt.Y('PC2:Q', title=f'PC2 ({pca.explained_variance_ratio_[1]*100:.2f}%)'),\n",
    "        color=alt.condition(selection, alt.value('steelblue'), alt.value('lightgray')),\n",
    "        tooltip=['REF_AREA', 'PC1', 'PC2'] + [col for col in df_pca_cleaned.columns]\n",
    "    ).add_params(\n",
    "        selection\n",
    "    ).properties(\n",
    "        title='PCA Interactivo de Países (Indicadores Banco Mundial)',\n",
    "        width=600,\n",
    "        height=400\n",
    "    ).interactive()\n",
    "\n",
    "    # Añadir etiquetas de texto\n",
    "    text = chart.mark_text(\n",
    "        align='left',\n",
    "        baseline='middle',\n",
    "        dx=7\n",
    "    ).encode(\n",
    "        text='REF_AREA:N'\n",
    "    )\n",
    "    \n",
    "    # En Jupyter/Colab a veces chart+text necesita display explicito\n",
    "    display(chart + text)"
]

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Notebook updated successfully.")
