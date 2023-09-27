from scripts.data_extraction import APIDataIngestor
import json

config_file = "config.json"

if __name__ == "__main__":

    print("Verificando: "+config_file)
    with open(config_file,'r') as file:
            config_data=json.load(file)
    print(config_data.get("api_url"))
    print(config_data.get("api_key"))

    data_extractor = APIDataIngestor(config_file) 
    data_extractor.set_header()
    data_extractor.set_body()
    data_extractor.post_request()