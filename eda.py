from scripts.data_extraction.api_ingestor import APIDataIngestor
from scripts.data_extraction.nih_robot_ingestor import NIHFormIngestion
import json
import pandas as pd



config_file = "config.json"
excel_file = "/data/"

if __name__ == "__main__":
    
    """
    Extraer datos de NIH
    """
    """
    df=pd.read_csv("./data/3_noncommunicable_diseases.csv")
    nih_extractor=NIHFormIngestion(df)
    nih_extractor.getKeyWords()
    nih_extractor.doASearch()
    """

    """
    Con los datos extraidos. Evaluar unicidad
    """

    csv_file = 'data/primary_di_numbers.csv'
    df = pd.read_csv(csv_file)
    
    # Verificar la unicidad de IDs
    if df['id'].nunique() != df.shape[0]:
        conteo_elementos_repetidos = df['id'].value_counts()
        # Obtén el número de elementos repetidos
        numero_repetidos = (conteo_elementos_repetidos > 1).sum()
        print(f"Hay {numero_repetidos} IDs duplicados en el archivo CSV.")

    # Eliminar registros duplicados basados en la columna 'id'
    df = df.drop_duplicates(subset='id', keep='first')
    

    # Guardar el DataFrame resultante en un nuevo archivo CSV
    new_csv_file = 'data/primary_di_cleaned.csv'
    df.to_csv(new_csv_file, index=False)

    csv_file = 'data/primary_di_cleaned.csv'
    df2 = pd.read_csv(csv_file)

    # Verificar la unicidad de IDs
    if df2['id'].nunique() != df2.shape[0]:
        conteo_elementos_repetidos = df2['id'].value_counts()
        # Obtén el número de elementos repetidos
        numero_repetidos = (conteo_elementos_repetidos > 1).sum()
        print(f"Hay {numero_repetidos} IDs duplicados en el archivo CSV.")

    print("registros eliminados")


""" 
        print("Verificando: "+config_file)
        with open(config_file,'r') as file:
            config_data=json.load(file)

    data_extractor = APIDataIngestor(config_file) 
    data_extractor.set_header()
    data_extractor.set_body()
    data_extractor.post_request()
    """