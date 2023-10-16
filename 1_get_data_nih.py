
from scripts.data_extraction.nih_robot_ingestor import NIHFormIngestion
import pandas as pd

key_terms_file = "./data/3_noncommunicable_diseases.csv"

if __name__ == "__main__":
    
    """
    Extract data from NIH
    """
    df=pd.read_csv(key_terms_file)
    nih_extractor=NIHFormIngestion(df)
    nih_extractor.getKeyWords()
    nih_extractor.doASearch()
    