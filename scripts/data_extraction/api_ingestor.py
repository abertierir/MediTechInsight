import requests
import json


"""
Esta clase tiene:
    - El constructor
    - La función que setea el header (Por ahora fijo)
    - La función que setea el body (Por ahora fijo)
    - La función que hace el post request (Por ahora fijo)

    * FetchOrganizationData por ahora no hace mucho

"""
class APIDataIngestor:
    def __init__(self, config_file):
        with open(config_file,'r') as file:
            config_data=json.load(file)
        self.base_url = config_data.get("api_url")
        self.api_key = config_data.get("api_key")
    
    def set_header(self):
        print("Open header")
        self.headers = {
            'accept': 'application/json',
            'X-cb-user-key':self.api_key,
            'Content-Type': 'application/json'
        }
    

    def set_body(self):
        self.body = {
            "field_ids": [
                "identifier",
                "location_identifiers",
                "short_description"
                ],
            "query": [
                {
                    "type": "predicate",
                    "field_id": "name",
                    "operator_id": "eq",
                    "values": ["HeartLung Corporation"]
                }
            ],
            "limit": 50
        }
    

    def post_request(self):

        self.response=requests.post(self.base_url,headers=self.headers,json=self.body)
        print("Sending Request")
        
        if self.response.status_code == 200:
            data = self.response.json()
            
            with open('./data/crunchbase_data.json', 'w') as json_file:
                json.dump(data, json_file, indent=4)
                print("Data has been saved in: '/data/crunchbase_data.json'")
        else:
            print(f"Error {self.response.status_code}: Couldn't fetch data from Crunchbase.")

    
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
