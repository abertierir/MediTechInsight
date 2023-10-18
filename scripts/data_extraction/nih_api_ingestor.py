import requests
import json

class NIHApiDataIngestor:

    def __init__(self, config_file):
        with open(config_file,'r') as file:
            config_data=json.load(file)
        self.base_url = config_data.get("api_url")
    
    def set_header(self):
        print("Open header")
        self.headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
    
    def get_device_by_id(self,id):

        base_url = self.base_url+'devices/'+f'{id}.json'
        self.response=requests.get(base_url,headers=self.headers)

        if self.response.status_code == 200:
            device_info = self.response.json()
            return device_info
        
        return None