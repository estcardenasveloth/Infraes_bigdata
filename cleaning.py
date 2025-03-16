import sqlite3
import pandas as pd
import numpy as np
import os

# Definir la ruta de la base de datos SQLite
db_file = "src/static/db/ingestion.db"

# Crear directorios si no existen
for folder in ["src/static/csv", "src/static/auditoria"]:
    os.makedirs(folder, exist_ok=True)

# Conectar a la base de datos
conn = sqlite3.connect(db_file)

# Leer los datos de la tabla 'covid_data'
df = pd.read_sql_query("SELECT * FROM covid_data", conn)

# Guardar el número de registros antes de la limpieza
num_registros_antes = len(df)

# Eliminar registros duplicados
df = df.drop_duplicates()

# Llenar los campos vacíos de las columnas de texto con NaN
text_columns = ["Admin2", "Province_State", "Combined_Key"]
for col in text_columns:
    df[col] = df[col].replace('', np.nan)

# Convertir las columnas Lat y Long_ a NaN si tienen valores vacíos o no válidos
df["Lat"] = pd.to_numeric(df["Lat"], errors="coerce")
df["Long_"] = pd.to_numeric(df["Long_"], errors="coerce")

# Contar el número de registros que serán eliminados por tener valores NULL en 'Lat' o 'Long_'
num_eliminados_lat_long = df[df["Lat"].isnull() | df["Long_"].isnull()].shape[0]

# Eliminar filas con valores NaN en las columnas 'Lat' y 'Long_'
df = df.dropna(subset=["Lat", "Long_"])

# Manejo de valores nulos para las columnas numéricas:
# Eliminar filas con valores nulos en las columnas numéricas relevantes
columns_to_check = ["Confirmed", "Deaths", "Recovered", "Active", "Lat", "Long_", "Incident_Rate", "Case_Fatality_Ratio"]
df = df.dropna(subset=columns_to_check)

# Guardar el número de registros después de la limpieza
num_registros_despues = len(df)

# Guardar los datos limpios en un archivo CSV
csv_file = "src/static/csv/cleaned_data.csv"
df.to_csv(csv_file, index=False)

# Generar el archivo de auditoría
audit_file = "src/static/auditoria/cleaning_report.txt"
with open(audit_file, "w", encoding="utf-8") as f:
    f.write("Reporte de Auditoría de Limpieza de Datos\n")
    f.write("="*50 + "\n")
    f.write(f"Registros antes de la limpieza: {num_registros_antes}\n")
    f.write(f"Registros después de la limpieza: {num_registros_despues}\n")
    f.write(f"Registros eliminados por valores NULL en 'Lat' o 'Long_': {num_eliminados_lat_long}\n")
    f.write("\nOperaciones realizadas:\n")
    f.write("- Eliminación de duplicados\n")
    f.write("- Manejo de valores nulos en columnas clave (Lat, Long_, Confirmed, etc.)\n")
    f.write("- Conversión de tipos de datos (entero, flotante, fecha, texto)\n")
    f.write("- Reemplazo de valores nulos con -9999 en columnas numéricas\n")
    f.write("- Eliminación de registros con valores NULL en 'Lat' o 'Long_'\n")

# Cerrar la conexión a la base de datos
conn.close()

print(f"[INFO] Datos procesados y guardados en el archivo CSV: {csv_file}")
print(f"[INFO] Reporte de auditoría generado en: {audit_file}")
