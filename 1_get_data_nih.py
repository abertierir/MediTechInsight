
from scripts.data_extraction.nih_robot_ingestor import NIHSearcher
import pandas as pd

key_terms_file = "./data/3_noncommunicable_diseases.csv"

if __name__ == "__main__":
    
    nihUrl="https://accessgudid.nlm.nih.gov"
    keyTermsFile=pd.read_csv(key_terms_file)
    nih_searcher=NIHSearcher(keyTermsFile, nihUrl)
    nih_searcher.setKeyWordsFromColumn("term")
    # Create a function or class to configure the search engine.
    nih_searcher.doASearch()
    