import os
from src.helper import load_pdf,text_split,download_hugging_face_embeddings
import pinecone

import ssl

orig_load_default_certs = ssl.SSLContext.load_default_certs
def dummy_load_default_certs(self, purpose=ssl.Purpose.SERVER_AUTH):
    pass
ssl.SSLContext.load_default_certs = dummy_load_default_certs
import certifi
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
from langchain_pinecone import PineconeVectorStore

from pinecone import Pinecone
from dotenv import load_dotenv
load_dotenv()

#access the environment variable
KEY=os.getenv("PINECONE_API_KEY")

extracted_data=load_pdf("C:/Users/shrey/OneDrive/Desktop/Medical-Chatbot-using-Llama2/data/")
text_chunks=text_split(extracted_data)
embeddings=download_hugging_face_embeddings()

#initializing pinecone
pc=Pinecone(api_key=KEY)
index_name="testing-pinecone"

#creating embeddings for each text chunks & store
docsearch=PineconeVectorStore.from_texts(
    [t.page_content for t in text_chunks],
    embeddings,
    index_name=index_name,
    pinecone_api_key=KEY
)

