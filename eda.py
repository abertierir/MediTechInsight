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
    df=pd.read_csv("./data/3_noncommunicable_diseases.csv")
    nih_extractor=NIHFormIngestion(df)
    nih_extractor.getKeyWords()
    nih_extractor.doASearch()


    """
    Extraer datos del API
    """
    print("Verificando: "+config_file)
    with open(config_file,'r') as file:
            config_data=json.load(file)

    data_extractor = APIDataIngestor(config_file) 
    data_extractor.set_header()
    data_extractor.set_body()
    data_extractor.post_request()