# Ingesta, Limpieza, Transformación y Auditoría de Datos

Este proyecto obtiene datos actualizados sobre COVID-19 desde la API `https://coronavirus.m.pipedream.net/`, los almacena en un archivo Excel (`.xlsx`) y en una base de datos SQLite (`.db`), y genera un informe de auditoría en `txt` para validar la integridad de los datos.

---

## Proceso de Ingesta y Auditoría de Datos

1. **Descarga de datos**: 
   - Se obtiene información de la API sobre casos, muertes y recuperaciones de COVID-19.
   
2. **Almacenamiento**:
   - Se guardan los datos en un archivo Excel (`ingestion.xlsx`).
   - Se insertan en una base de datos SQLite (`ingestion.db`).

3. **Auditoría de datos**:
   - Se comparan los datos obtenidos con los almacenados en la base de datos.
   - Se genera un informe detallado en `ingestion.txt` dentro de `src/static/auditoria/`.

---

## Proceso de Limpieza de Datos

Una vez que los datos han sido almacenados, el **script de limpieza (`cleaning.py`)** se ejecuta para procesar los datos:

1. **Eliminación de Duplicados**:
   - Se eliminan los registros duplicados del conjunto de datos.

2. **Manejo de Valores Nulos**:
   - Se eliminan los registros con valores nulos en columnas clave como `Lat`, `Long_`, `Confirmed`, etc.
   - Los valores faltantes se reemplazan con `-9999` para mantener la integridad de los datos.

3. **Conversión de Tipos de Datos**:
   - Se asegura que los datos estén en el formato adecuado:
     - **Lat**, **Long_** se convierten en `float`.
     - **FIPS**, **Confirmed**, **Deaths**, **Recovered**, **Active** se convierten en `int`.
     - **Last_Update** se convierte en tipo fecha (`datetime`).

4. **Generación de Archivos de Salida**:
   - Después de la limpieza, se genera un archivo CSV (`cleaned_data.csv`) con los datos procesados y un archivo de auditoría (`cleaning_report.txt`) con el resumen de la limpieza.

Puedes ejecutar el script de limpieza ejecutando el siguiente comando:

\```bash
python cleaning.py
\```


---

## Workflow Automatizado con GitHub Actions

Este proyecto utiliza **GitHub Actions** para automatizar el proceso de ingestión, limpieza y generación de informes. El workflow se ejecuta automáticamente cuando se realiza un `push` a la rama `main` del repositorio. A continuación se describe el flujo de trabajo automatizado:

### 1. Ingesta de Datos
- Se ejecuta el script `ingestion.py` para obtener los datos de la API, almacenarlos en un archivo Excel (`ingestion.xlsx`) y en una base de datos SQLite (`ingestion.db`).

### 2. Limpieza de Datos
- Después de la ingestión de los datos, se ejecuta automáticamente el script `cleaning.py` para limpiar los datos. Este script realiza las siguientes operaciones:
  - Elimina registros duplicados.
  - Maneja los valores nulos en las columnas clave.
  - Convierte los tipos de datos a los formatos adecuados (por ejemplo, de texto a números o fechas).

### 3. Generación de Archivos de Salida
- El workflow genera los siguientes archivos de salida:
  - Un archivo CSV (`cleaned_data.csv`) con los datos procesados.
  - Un archivo de auditoría (`cleaning_report.txt`) con detalles sobre las operaciones realizadas durante la limpieza de datos.

### 4. Commit y Push Automático
- Los archivos generados son **commitados** y enviados automáticamente al repositorio utilizando la acción `git-auto-commit-action`. Esto asegura que los cambios se registren y se suban al repositorio sin intervención manual.

### 5. Ubicación del Workflow
- El workflow está definido en el archivo `.github/workflows/bigdata.yml` y se ejecuta cada vez que se realiza un `push` a la rama `main`.