import requests
import pandas as pd

# Función para obtener los datos de la API
def obtener_datos_api(url, limit=1000, offset=0):
    params = {
        '$limit': limit,
        '$offset': offset
    }
    response = requests.get(url, params=params)
    return response.json()

# Función para procesar los datos y convertirlos al formato adecuado
def procesar_datos(data):
    processed_data = []
    
    for item in data:
        # Extraer los campos y eliminar valores no válidos como "NA" o cadenas vacías
        primer_nombre = item.get('primer_nombre', '').strip()
        segundo_nombre = item.get('segundo_nombre', '').strip()
        primer_apellido = item.get('primer_apellido', '').strip()
        segundo_apellido = item.get('segundo_apellido', '').strip()

        # Filtrar valores vacíos o que sean 'NA' y concatenar los nombres
        def limpiar_nombre(nombre):
            if nombre and nombre != "NA":
                return nombre
            return None

        # Limpiar los nombres
        primer_nombre = limpiar_nombre(primer_nombre)
        segundo_nombre = limpiar_nombre(segundo_nombre)
        primer_apellido = limpiar_nombre(primer_apellido)
        segundo_apellido = limpiar_nombre(segundo_apellido)

        # Concatenar en el orden solicitado sin agregar espacios si algún campo está vacío
        nombre_completo = ' '.join(filter(None, [primer_nombre, segundo_nombre, primer_apellido, segundo_apellido]))

        row = {
            'Descripción/Resumen': item.get('sanciones', ''),
            'Entidad': item.get('entidad_sancionado', ''),
            'Fecha de Vinculación': item.get('fecha_efectos_juridicos', ''),
            'Departamento': item.get('entidad_departamento', ''),
            'Municipio': item.get('entidad_municipio', ''),
            'Nombre Completo (Apellidos-Nombres) /Razón Social': nombre_completo,
            'Tipo de Documento': item.get('nombre_tipo_identificacion', ''),
            'No. De documento': item.get('numero_identificacion', '')
        }
        processed_data.append(row)
    
    return processed_data

# Función principal para consultar la API y exportar los datos a un archivo Excel
def exportar_datos_a_excel(url):
    offset = 0
    limit = 1000
    all_data = []

    while True:
        data = obtener_datos_api(url, limit, offset)
        if not data:  # Si no hay más datos, terminamos
            break
        
        # Procesar los datos obtenidos
        processed_data = procesar_datos(data)
        all_data.extend(processed_data)
        
        # Aumentar el offset para la siguiente consulta
        offset += limit

    # Convertir los datos procesados en un DataFrame de pandas
    df = pd.DataFrame(all_data)

    # Eliminar duplicados basados en el número de identificación
    df = df.drop_duplicates(subset='No. De documento', keep='first')

    # Exportar los datos a un archivo Excel
    df.to_excel('exportado_datos_sin_duplicados.xlsx', index=False)
    print("Los datos han sido exportados a 'exportado_datos_sin_duplicados.xlsx'.")

# URL de la API
url = "https://www.datos.gov.co/resource/iaeu-rcn6.json"

# Llamar a la función para exportar los datos a un archivo Excel
exportar_datos_a_excel(url)
