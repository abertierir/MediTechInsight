import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt
import seaborn as sns


if __name__ == "__main__":  

    # Inicializar la conexión a MongoDB
    client = MongoClient('localhost', 27017)  # Cambia 'localhost' y 27017 por la configuración de tu servidor MongoDB
    db = client['medical_devices']
    collection = db['devices']

    # Consulta 1: Obtener la cantidad total de registros
    total_records = collection.count_documents({})
    print(f"Total de registros: {total_records}")

   
    # Análisis Exploratorio de Datos
    # Visualizar la estructura de la base de datos
    cursor = collection.find({}) 
    df = pd.json_normalize(list(cursor))
   # df = pd.DataFrame(list(cursor))
    print("Estructura de la base de datos:")
    print(df.head())

    brands = collection.distinct("brandName")
    print("Marcas de dispositivos:")
    for brand in brands:
        print(brand)

    # Estadísticas descriptivas de la base de datos
    print("Estadísticas descriptivas:")
    print(df.describe())

    # Visualizar la distribución de datos
    plt.figure(figsize=(12, 6))
    sns.countplot(data=df, x='publicVersionStatus')
    plt.title("Distribución de Version Status")
    plt.show()

    # Visualizar los fabricantes (companyName) más comunes
    plt.figure(figsize=(12, 6))
    top_manufacturers = df['companyName'].value_counts().nlargest(10)
    top_manufacturers.plot(kind='bar')
    plt.title("Top 10 Fabricantes")
    plt.xlabel("Fabricante")
    plt.ylabel("Cantidad de Dispositivos")
    plt.show()

    # Visualizar la distribución de tipos de dispositivos (gmdnPTName)
    plt.figure(figsize=(12, 6))
    top_device_types = df["gmdnTerms.gmdn"].apply(lambda x: x[0]['gmdnCode']).value_counts().nlargest(10)
    top_device_types.plot(kind='bar')
    plt.title("Top 10 Tipos de Dispositivos")
    plt.xlabel("Tipo de Dispositivo")
    plt.ylabel("Cantidad de Dispositivos")
    plt.show()

    version_status_json = top_device_types.to_json("datos.json",orient='records')

    client.close()
    