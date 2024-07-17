from langchain_astradb import AstraDBVectorStore
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os
import pandas as pd
from ecommbot.data_converter import dataconveter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
#embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

GOOGLE_API_KEY             = os.getenv("GOOGLE_API_KEY")
ASTRA_DB_API_ENDPOINT      = os.getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_KEYSPACE          = os.getenv("ASTRA_DB_KEYSPACE")

def ingestdata(status):
    vstore = AstraDBVectorStore(
            embedding       = GoogleGenerativeAIEmbeddings(model="models/embedding-001"),
            collection_name ="ecomm",
            api_endpoint    = ASTRA_DB_API_ENDPOINT,
            token           = ASTRA_DB_APPLICATION_TOKEN,
            namespace       = ASTRA_DB_KEYSPACE,
        )
    
    storage=status
    
    if storage==None:
        docs = dataconveter()
        inserted_ids = vstore.add_documents(docs)
    else:
        return vstore
    return vstore, inserted_ids

if __name__=='__main__':
    vstore,inserted_ids = ingestdata(None)
    print(f"\nInserted {len(inserted_ids)} documents.")
    results = vstore.similarity_search("can you tell me the low budget sound basshead.")
    for res in results:
            print(f"* {res.page_content} [{res.metadata}]")