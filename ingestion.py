import requests
import pandas as pd
import sqlite3
import os

# URL del endpoint de la API
url = "https://coronavirus.m.pipedream.net/"

# Crear directorios si no existen
for folder in ["src/static/xlsx", "src/static/db", "src/static/auditoria"]:
    os.makedirs(folder, exist_ok=True)

# Definir rutas de los archivos
xlsx_file = os.path.join("src", "static", "xlsx", "ingestion.xlsx")
db_file = os.path.join("src", "static", "db", "ingestion.db")
audit_file = os.path.join("src", "static", "auditoria", "ingestion.txt")

# Realizar la solicitud GET a la API
response = requests.get(url)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    data = response.json()  # Convertir la respuesta en JSON
    
    # Extraer la lista "rawData"
    raw_data = data.get("rawData", [])
    
    if raw_data:
        # Convertir los datos en un DataFrame de Pandas
        df_api = pd.DataFrame(raw_data)

        # Seleccionar las columnas necesarias (filtrar si existen en los datos)
        columnas = [
            "FIPS", "Admin2", "Province_State", "Country_Region", "Last_Update",
            "Lat", "Long_", "Confirmed", "Deaths", "Recovered", "Active",
            "Combined_Key", "Incident_Rate", "Case_Fatality_Ratio"
        ]
        
        df_api = df_api[[col for col in columnas if col in df_api.columns]]

        # Guardar en Excel
        try:
            df_api.to_excel(xlsx_file, index=False)
            print(f"[INFO] Datos guardados en Excel: {os.path.abspath(xlsx_file)}")
        except Exception as e:
            print(f"[ERROR] No se pudo guardar en Excel: {e}")

        # Guardar en SQLite
        try:
            conn = sqlite3.connect(db_file)
            df_api.to_sql("covid_data", conn, if_exists="replace", index=False)
            print(f"[INFO] Datos almacenados en SQLite: {os.path.abspath(db_file)}")
        except Exception as e:
            print(f"[ERROR] No se pudo guardar en SQLite: {e}")
        finally:
            conn.close()

        # Leer los datos almacenados en la base de datos
        conn = sqlite3.connect(db_file)
        df_db = pd.read_sql_query("SELECT * FROM covid_data", conn)
        conn.close()

        # Comparar registros (convertir tipos para evitar errores)
        num_registros_api = len(df_api)
        num_registros_db = len(df_db)

        diferencias = "No se puede comparar, estructuras diferentes"
        if num_registros_api == num_registros_db:
            try:
                diferencias = df_api.astype(str).compare(df_db.astype(str), keep_equal=False)
            except Exception as e:
                diferencias = f"Error en comparación: {e}"

        # Generar el reporte de auditoría
        with open(audit_file, "w", encoding="utf-8") as f:
            f.write("Reporte de Auditoría de Datos COVID-19\n")
            f.write("="*50 + "\n")
            f.write(f"Registros obtenidos de la API: {num_registros_api}\n")
            f.write(f"Registros almacenados en SQLite: {num_registros_db}\n")
            f.write("\nIntegridad de los datos: ")
            if num_registros_api == num_registros_db and diferencias.empty:
                f.write("Los datos coinciden perfectamente.\n")
            else:
                f.write("Se encontraron diferencias en los registros.\n")
                f.write("\nDiferencias detectadas:\n")
                f.write(str(diferencias) + "\n")

        print(f"[INFO] Reporte de auditoría generado en: {os.path.abspath(audit_file)}")

    else:
        print("[WARNING] No se encontraron datos en la API.")

else:
    print(f"[ERROR] No se pudo obtener los datos. Código de estado: {response.status_code}")



