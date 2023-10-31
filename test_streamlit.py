import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient
import plotly.express as px

st.cache_resource.clear()

# Inicializar la conexión a MongoDB
client = MongoClient('localhost', 27017)  # Cambia 'localhost' y 27017 por la configuración de tu servidor MongoDB
db = client['medical_devices']
collection = db['devices']

# Consulta 1: Obtener la cantidad total de registros
total_records = collection.count_documents({})
st.write(f"Total de registros: {total_records}")


# Análisis Exploratorio de Datos
# Visualizar la estructura de la base de datos
cursor = collection.find({}) 
df = pd.json_normalize(list(cursor))
# df = pd.DataFrame(list(cursor))
st.subheader("Estructura de la base de datos:")
st.write(df.head())

brands = collection.distinct("brandName")
# print("Marcas de dispositivos:")
# for brand in brands:
#     print(brand)
st.subheader("Marcas de dispositivos:")
st.write(brands)

# Estadísticas descriptivas de la base de datos
st.subheader("Estadísticas descriptivas:")
st.write(df.describe())

# Visualizar la distribución de datos
plt.figure(figsize=(12, 6))
#sns.countplot(data=df, x='publicVersionStatus')
plt.title("Distribución de Version Status")
plt.show()

# st.subheader("Top 10 gmdnCodes")
# top_device_types = df["gmdnTerms.gmdn"].apply(lambda x: x[0]['gmdnPTName']).value_counts().nlargest(10)
# st.bar_chart(top_device_types)

# Visualizar los fabricantes (companyName) más comunes
# plt.figure(figsize=(12, 6))
st.subheader("Top 10 Companies")
top_manufacturers = df['companyName'].value_counts().nlargest(10)
st.bar_chart(top_manufacturers)

top_device_types = df["gmdnTerms.gmdn"].apply(lambda x: x[0]['gmdnPTName']).value_counts().nlargest(10)

st.subheader("Top 10 gmdnCodes")
st.write(top_device_types)


fig = px.bar(
    x=top_device_types.index,  # Categories on the X-axis
    y=top_device_types.values,  # Counts on the Y-axis
    labels={'x': 'gmdnCode', 'y': 'Count'},
    title="Top 10 gmdnCodes"
)

st.plotly_chart(fig)

# top_manufacturers.plot(kind='bar')
# plt.title("Top 10 Fabricantes")
# plt.xlabel("Fabricante")
# plt.ylabel("Cantidad de Dispositivos")
# plt.show()

# Visualizar la distribución de tipos de dispositivos (gmdnPTName) gmdnCode
#plt.figure(figsize=(12, 6))

#top_device_types.plot(kind='bar')
# plt.title("Top 10 Tipos de Dispositivos")
# plt.xlabel("Tipo de Dispositivo")
# plt.ylabel("Cantidad de Dispositivos")
# plt.show()

client.close()

