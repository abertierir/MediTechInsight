from scripts.data_extraction.nih_api_ingestor import NIHApiDataIngestor
import pandas as pd
from pymongo import MongoClient

config_file = "config_nih.json"
csv_file = 'data/primary_di_cleaned.csv'

if __name__ == "__main__":
    
    """
    With the clean data, make the request to retrieve information 
    for each device and save it in the database
    """
    
    df = pd.read_csv(csv_file)

    data_extractor = NIHApiDataIngestor(config_file) 
    data_extractor.set_header()

    # Set connection with MongoDB
    client = MongoClient('localhost', 27017)
    db = client['medical_devices']
    collection = db['devices']

    # Define el valor de inicio
    inicio_id = "00857117006308"

    # Encuentra el índice del valor de inicio en la columna 'id'
    indice_inicio = df[df['id'] == inicio_id].index[0]
    
    # Itera a través del DataFrame desde el índice de inicio hasta el final
    for i in range(indice_inicio, len(df)):
        id = df.loc[i, 'id']
        device_info=data_extractor.get_device_by_id(id)
        collection.insert_one(device_info)
        print(f"ID: {id} - Información guardada en MongoDB")
    """
    for id in df['id']:
        device_info=data_extractor.get_device_by_id(id)
        collection.insert_one(device_info)
        print(f"ID: {id} - Información guardada en MongoDB")
    """
    client.close

    
