import pandas as pd
import sqlite3
import os

# Crear carpetas necesarias
for folder in ["src/static/xlsx", "src/static/db", "src/static/auditoria", "src/static/csv"]:
    os.makedirs(folder, exist_ok=True)

# Rutas de archivos
input_csv_file = os.path.join("src", "static", "csv", "cleaned_data.csv")
csv_iso_file = os.path.join("src", "static", "csv", "codigo_iso_pais.csv")
csv_pob_ipc_file = os.path.join("src", "static", "csv", "pob_ipc.csv")
csv_output_file = os.path.join("src", "static", "csv", "enriched_data.csv")
db_file = os.path.join("src", "static", "db", "ingestion.db")
audit_file = os.path.join("src", "static", "auditoria", "enriched_report.txt")

# Leer archivo cleaned_data.csv
try:
    df_api = pd.read_csv(input_csv_file)
except Exception as e:
    raise FileNotFoundError(f"[ERROR] No se pudo leer el archivo cleaned_data.csv: {e}")

# Cargar códigos ISO
try:
    df_iso = pd.read_csv(csv_iso_file, sep=";")
except Exception as e:
    raise FileNotFoundError(f"[ERROR] No se pudo cargar codigo_iso_pais.csv: {e}")

# Agregar columna code_iso usando Country_Region
df_api["code_iso"] = df_api["Country_Region"].map(dict(zip(df_iso["Country_Region"], df_iso["ISO3_Code"])))

# Agregar columna code_key
def generar_code_key(row):
    parts = [row["code_iso"]]
    if pd.notna(row.get("Province_State")) and row["Province_State"]:
        parts.append(str(row["Province_State"]))
    if pd.notna(row.get("Admin2")) and row["Admin2"]:
        parts.append(str(row["Admin2"]))
    return "-".join(str(p) for p in parts if pd.notna(p) and p != "")

df_api["code_key"] = df_api.apply(generar_code_key, axis=1)

# Auditoría inicial
nuevas_columnas = ["code_iso", "code_key"]
merge_info = ""

# Intentar hacer el merge con pob_ipc.csv
try:
    df_pob = pd.read_csv(csv_pob_ipc_file)
    registros_antes_merge = len(df_api)
    columnas_antes_merge = set(df_api.columns)

    df_merged = df_api.merge(df_pob, how="left", on="code_key")
    registros_despues_merge = len(df_merged)
    columnas_despues_merge = set(df_merged.columns)
    columnas_nuevas_merge = list(columnas_despues_merge - columnas_antes_merge)

    merge_info += "\nDetalles del merge con pob_ipc.csv:\n"
    merge_info += f"- Registros antes del merge: {registros_antes_merge}\n"
    merge_info += f"- Registros después del merge: {registros_despues_merge}\n"
    merge_info += f"- Columnas añadidas por el merge: {', '.join(columnas_nuevas_merge) if columnas_nuevas_merge else 'Ninguna'}\n"

    if registros_despues_merge < registros_antes_merge:
        merge_info += "- [ALERTA] Se perdieron registros en el merge.\n"
    elif registros_despues_merge > registros_antes_merge:
        merge_info += "- [ALERTA] Se añadieron registros inesperadamente en el merge.\n"
    else:
        merge_info += "- No hubo pérdida de registros.\n"

    # Contar nulos en las columnas nuevas del merge
    if columnas_nuevas_merge:
        merge_info += "\nResumen de valores nulos en columnas nuevas del merge:\n"
        for col in columnas_nuevas_merge:
            nulos = df_merged[col].isna().sum()
            merge_info += f"- {col}: {nulos} valores nulos\n"

except Exception as e:
    merge_info += f"\n[ERROR] No se pudo realizar el merge con pob_ipc.csv: {e}\n"
    df_merged = df_api.copy()

# Guardar en CSV
df_merged.to_csv(csv_output_file, index=False)

# Guardar en SQLite en nueva tabla dat_trans
conn = sqlite3.connect(db_file)
df_merged.to_sql("dat_trans", conn, if_exists="replace", index=False)
conn.close()

# Escribir auditoría
with open(audit_file, "w", encoding="utf-8") as f:
    f.write("Auditoría de Transformación de Datos COVID-19\n")
    f.write("=" * 50 + "\n")
    f.write(f"Columnas nuevas añadidas: {len(nuevas_columnas)}\n")
    f.write("Nombres de columnas añadidas:\n")
    for col in nuevas_columnas:
        f.write(f"- {col}\n")
    f.write(merge_info)

print(f"[INFO] Transformación completada y auditoría generada: {audit_file}")
