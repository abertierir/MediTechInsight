from MediTechInsight.scripts.data_extraction.api_ingestor import APIDataIngestor
from MediTechInsight.scripts.data_extraction.nih_robot_ingestor import NIHFormIngestion
import json



config_file = "config.json"

if __name__ == "__main__":
    
    """
    Extraer datos de NIH
    """
    nih_extractor=NIHFormIngestion(config_file)


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