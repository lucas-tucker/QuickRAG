# Author: Lucas Tucker

import utils
import os
import openai
openai.api_key = utils.get_openai_api_key()

from llama_index import SimpleDirectoryReader
from llama_index import Document

from llama_index import VectorStoreIndex
from llama_index import ServiceContext
from llama_index.llms import OpenAI

from llama_index import SimpleDirectoryReader, Document
from llama_index import VectorStoreIndex
from llama_index import ServiceContext
from llama_index.llms import OpenAI

from urllib.parse import urlparse, parse_qs
import requests
import pdfkit

from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

# store the highlighted data in QueryEngine object 
class QueryEngine:
    def __init__(self, model="gpt-3.5-turbo", temperature=0.1):
        self.llm = OpenAI(model=model, temperature=temperature)
        self.query_engine = None
        self.document = None
        self.documents = None
    
    def load_documents(self, pdf_url, save_path):
        parsed_url = urlparse(pdf_url)
        # ensure url is (at least somewhat) safe
        if parsed_url.scheme != 'https' or not parsed_url.netloc or not parsed_url.path:
            print(f"Failed to download PDF from: {pdf_url}")
        else:
            response = requests.get(pdf_url)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                    print(f"PDF downloaded successfully to: {save_path}")
            else:
                print(f"Failed to download PDF from: {pdf_url}")
        documents = SimpleDirectoryReader(input_files=["./data.pdf"]).load_data()
        self.documents = documents
        self.document = Document(text="\n\n".join([doc.text for doc in documents]))
        service_context = ServiceContext.from_defaults(llm=self.llm, embed_model="local:BAAI/bge-small-en-v1.5")
        index = VectorStoreIndex.from_documents([self.document], service_context=service_context)
        self.query_engine = index.as_query_engine()
    
    def query(self, input_query):
        print(type(self.query_engine))
        return str(self.query_engine.query(input_query))

engine = QueryEngine()

@app.route('/', methods=['POST'])
def handle_post():
    if request.is_json:
        # recieved linkUrl from background.js
        post_data = request.get_json()
        if post_data['type'] == 'linkUrl':
            linkUrl = post_data['data']
            print(f"The server received the linkUrl {linkUrl}")
            # create the query engine
            engine.load_documents(linkUrl, "data.pdf")
            return jsonify({"message": "PDF loaded successfully"}), 200
        else:
            return jsonify({"error": "Invalid request"}), 400
    else:
        # return query engine result given query
        query = request.form.get('query')
        scaffolding = "Please answer the following query by citing specific portions of the context. "
        result = engine.query(scaffolding + query)
        return result
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

