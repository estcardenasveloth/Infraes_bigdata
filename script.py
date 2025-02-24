import os
import pandas as pd
import json

def main():
    # Obtener la ruta del directorio actual del script
    script_dir = os.path.dirname(os.path.abspath(__file__))  
    
    # Construir la ruta relativa del archivo JSON
    json_path = os.path.join(script_dir, "data.json")

    # Verificar si el archivo existe
    if not os.path.exists(json_path):
        print(f"Error: No se encontró el archivo '{json_path}'")
        return

    # Leer el archivo JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Si el JSON es un diccionario único, convertirlo a una lista
    if isinstance(data, dict):
        data = [data]
    
    # Crear DataFrame y guardar en Excel
    df = pd.DataFrame(data)
    
    # Guardar el archivo de salida en la misma carpeta del script
    output_path = os.path.join(script_dir, 'output.xlsx')
    df.to_excel(output_path, index=False)

    print(f"Archivo Excel '{output_path}' generado exitosamente.")

if __name__ == '__main__':
    main()