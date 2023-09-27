import requests
import json

class APIDataIngestor:
    def __init__(self, config_file):
        with open(config_file,'r') as file:
            config_data=json.load(file)
        self.base_url = config_data.get("api.url")
        self.api_key = config_data.get("api.key")
    
    def set_header(self):
        self.headers = {
            'accept': 'application/json',
            'X-cb-user-key':self.api_key,
            'Content-Type': 'application/json'
        }

    def set_body(self):
        self.body={
            "field_ids": [
                "identifier",
                "location_identifiers",
                "short_description"
                ],
            "query": [
                {
                    "type": "predicate",
                    "field_id": "short_description",
                    "operator_id": "contains",
                    "values": ["SaaS"]
                }
            ],
         "limit": 50
        }

    def post_request(self):

        self.response=requests.post(self.base_url)
        
        if self.response.status_code == 200:
            data = self.response.json()
            
            with open('../data/crunchbase_data.json', 'w') as json_file:
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
