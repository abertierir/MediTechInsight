import requests
import json

class APIDataIngestor:
    def __init__(self, config_file):
        with open(config_file,'r') as file:
            config_data=json.load(file)
        self.base_url = config_data.get("api.url")
        self.api_key = config_data.get("api.key")
    
    def setHeader(self):
        self.headers = {
            'accept': 'application/json',
            'X-cb-user-key':self.apy_key,
            'Content-Type': 'application/json'
        }
    
    def fetch_organization_data(self, organization_id):
        endpoint = f"organizations/{organization_id}"
        url = f"{self.base_url}{endpoint}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {str(e)}")
            return None
