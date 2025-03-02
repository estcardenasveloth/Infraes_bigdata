# Proyecto de Ingesta y Auditoría de Datos COVID-19

Este proyecto obtiene datos actualizados sobre COVID-19 desde la API `https://coronavirus.m.pipedream.net/`, los almacena en un archivo Excel (`.xlsx`) y en una base de datos SQLite (`.db`), y genera un informe de auditoría en `txt` para validar la integridad de los datos.

---

## Proceso de Ingesta y Auditoría de Datos
1. **Descarga de datos**: Se obtiene información de la API sobre casos, muertes y recuperaciones de COVID-19.
2. **Almacenamiento**:
   - Se guardan los datos en un archivo Excel (`ingestion.xlsx`).
   - Se insertan en una base de datos SQLite (`ingestion.db`).
3. **Auditoría de datos**:
   - Se comparan los datos obtenidos con los almacenados en la base de datos.
   - Se genera un informe detallado en `ingestion.txt` dentro de `src/static/auditoria/`.

---

## Instrucciones para Clonar el Repositorio
Para obtener una copia local del proyecto, ejecuta el siguiente comando en la terminal:

```sh
git clone https://github.com/estcardenasveloth/Infraes_bigdata.git
cd repo
