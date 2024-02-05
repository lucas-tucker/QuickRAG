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

import http.server
import socketserver
import json
import cgi
from urllib.parse import urlparse, parse_qs

import requests

# Load the documents and create the query engine
# documents = SimpleDirectoryReader(input_files=["./Stalin_reading.pdf"]).load_data()
# document = Document(text="\n\n".join([doc.text for doc in documents]))
# llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)
# service_context = ServiceContext.from_defaults(llm=llm, embed_model="local:BAAI/bge-small-en-v1.5")
# index = VectorStoreIndex.from_documents([document], service_context=service_context)
# query_engine = index.as_query_engine()
query_engine = [None]

def download_pdf(pdf_url, save_path):
    parsed_url = urlparse(pdf_url)
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

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        if ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers.get('content-length'))
            postvars = parse_qs(self.rfile.read(length), keep_blank_values=1)
            query = postvars[b'query'][0].decode()
            scaffolding = "Please answer the following query by citing specific portions of the context. "
            # Run your query against the query engine
            result = str(query_engine[0].query(scaffolding + query))
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"result": result}).encode())

        if ctype == 'application/json':
            length = int(self.headers.get('content-length'))
            post_data = json.loads(self.rfile.read(length))
            
            if post_data['type'] == 'linkUrl':
                linkUrl = post_data['data']
                print(f"The server recieved the linkUrl {linkUrl}")
                save_path = "data.pdf"
                download_pdf(linkUrl, save_path)
                documents = SimpleDirectoryReader(input_files=["./data.pdf"]).load_data()
                document = Document(text="\n\n".join([doc.text for doc in documents]))
                llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)
                service_context = ServiceContext.from_defaults(llm=llm, embed_model="local:BAAI/bge-small-en-v1.5")
                index = VectorStoreIndex.from_documents([document], service_context=service_context)
                query_engine[0] = index.as_query_engine()

            elif post_data['type'] == 'window':
                print(f"Made successful window request")

socketserver.TCPServer(("", 8000), Handler).serve_forever()

