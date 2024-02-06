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
from flask import Flask, request, jsonify
import sqlite3

import requests

query_engine = [None]
document = [None]
documents = [None]
llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)

class QueryEngine:
    def __init__(self, model="gpt-3.5-turbo", temperature=0.1):
        self.llm = OpenAI(model=model, temperature=temperature)
        self.query_engine = None
        self.document = None
        self.documents = None
    
    def load_documents(self, pdf_url, save_path):
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
        documents = SimpleDirectoryReader(input_files=["./data.pdf"]).load_data()
        self.documents = documents
        self.document = Document(text="\n\n".join([doc.text for doc in documents]))
        service_context = ServiceContext.from_defaults(llm=llm, embed_model="local:BAAI/bge-small-en-v1.5")
        index = VectorStoreIndex.from_documents([self.document], service_context=service_context)
        self.query_engine = index.as_query_engine()

engine = QueryEngine()

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        if ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers.get('content-length'))
            postvars = parse_qs(self.rfile.read(length), keep_blank_values=1)
            query = postvars[b'query'][0].decode()
            scaffolding = "Please answer the following query by citing specific portions of the context. "
            # Run your query against the query engine
            result = str(engine.query_engine.query(scaffolding + query))
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
                engine.load_documents(linkUrl, "data.pdf")
                # service_context = ServiceContext.from_defaults(llm=llm, embed_model="local:BAAI/bge-small-en-v1.5")
                # index = VectorStoreIndex.from_documents([document[0]], service_context=service_context)
                # query_engine[0] = index.as_query_engine()

            # elif post_data['type'] == 'window':
            #     print(f"Made successful window request")
            #     sentence_index = utils.build_sentence_window_index(document[0], llm, embed_model="local:BAAI/bge-small-en-v1.5", save_dir="sentence_index")
            #     query_engine[0] = utils.get_sentence_window_query_engine(sentence_index)

            # elif post_data['type'] == 'automerging':
            #     print(f"Made successful automerging request")
            #     automerging_index = utils.build_automerging_index(documents[0], llm, embed_model="local:BAAI/bge-small-en-v1.5", save_dir="merging_index")
            #     query_engine[0] = utils.get_automerging_query_engine(automerging_index)

socketserver.TCPServer(("", 8000), Handler).serve_forever()

