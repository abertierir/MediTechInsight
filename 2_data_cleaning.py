from scripts.data_extraction.api_ingestor import APIDataIngestor
from scripts.data_extraction.nih_robot_ingestor import NIHFormIngestion
import json
import pandas as pd

original_file = "data/primary_di_numbers.csv"

if __name__ == "__main__":

    """
    With the extracted data. Evaluate uniqueness
    """

    csv_file = original_file
    df = pd.read_csv(csv_file)

    df = df.drop_duplicates(subset='id', keep='first')
    
    new_csv_file = 'data/primary_di_cleaned.csv'
    df.to_csv(new_csv_file, index=False)