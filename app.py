from flask import Flask,render_template,jsonify,request
from src.helper import download_hugging_face_embeddings
import os
import ssl

orig_load_default_certs = ssl.SSLContext.load_default_certs
def dummy_load_default_certs(self, purpose=ssl.Purpose.SERVER_AUTH):
    pass
ssl.SSLContext.load_default_certs = dummy_load_default_certs
import certifi
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
from langchain_pinecone import PineconeVectorStore

import pinecone
from pinecone import Pinecone
from langchain_core.prompts import PromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.llms import CTransformers
from langchain.chains.combine_documents import create_stuff_documents_chain
from src.prompt import prompt_template
from dotenv import load_dotenv

app=Flask(__name__)

load_dotenv()

#access the environment variable
KEY=os.getenv("PINECONE_API_KEY")

embeddings=download_hugging_face_embeddings()

#initializing pinecone
pc=Pinecone(api_key=KEY)
index_name="testing-pinecone"

docsearch=PineconeVectorStore.from_existing_index(index_name,embeddings)

PROMPT=PromptTemplate(
    template=prompt_template,
    input_variables=["context","input"]
)

llm=CTransformers(model="model/llama-2-7b-chat.ggmlv3.q4_0.bin",
                  model_type="llama",config={'max_new_tokens':512,'temperature':0.8})

question_answer_chain = create_stuff_documents_chain(llm, PROMPT)
retriever = docsearch.as_retriever(search_kwargs={'k': 2})
qa = create_retrieval_chain(retriever, question_answer_chain)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get",methods=["GET","POST"])
def chat():
    msg=request.form["msg"]
    input=msg
    print(input)
    result = qa.invoke({"input": input})
    print("Response:", result["answer"])
    return str(result["answer"])


if __name__=='__main__':
    app.run(host="0.0.0.0",port="5000",debug=True)