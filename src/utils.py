# Author: Lucas Tucker

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv()
# openai_api_key = os.getenv("OPENAI_API_KEY")
# huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")

def get_openai_api_key():
    _ = load_dotenv(find_dotenv())

    return os.getenv("OPENAI_API_KEY")


def get_hf_api_key():
    _ = load_dotenv(find_dotenv())

    return os.getenv("HUGGINGFACE_API_KEY")