import os

import qdrant_client

from dotenv import load_dotenv
from langfuse.llama_index import LlamaIndexCallbackHandler
from llama_index.core import Settings
from llama_index.core.callbacks import CallbackManager
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.qdrant import QdrantVectorStore
from sqlalchemy import create_engine

load_dotenv()

# Vector Store Settings ################################
QDRANT_HOST = os.environ.get("QDRANT_HOST", "localhost")
QDRANT_PORT = os.environ.get("PORT", 6333)

QDRANT_CLIENT = qdrant_client.QdrantClient(
    # you can use :memory: mode for fast and light-weight experiments,
    # it does not require to have Qdrant deployed anywhere
    # but requires qdrant-client >= 1.1.1
    # location=":memory:"
    # otherwise set Qdrant instance address with:
    # url="http://<host>:<port>"
    # otherwise set Qdrant instance with host and port:
    host=QDRANT_HOST,
    port=QDRANT_PORT,
    # set API KEY for Qdrant Cloud
    # api_key="<qdrant-api-key>",
)

VECTOR_STORE = QdrantVectorStore(
    client=QDRANT_CLIENT, enable_hybrid=True, collection_name="style_python"
)

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "localhost")

# Generation and Embedding Model Seetings ##############
GENERATIVE_MODEL_NAME = os.environ.get("GENERATIVE_MODEL_NAME", "gemma:2b")
LLM = Ollama(
    model=GENERATIVE_MODEL_NAME,
    request_timeout=36000,
    base_url=f"http://{OLLAMA_HOST}:11434",
)

EMBED_MODEL_NAME = os.environ.get("EMBED_MODEL_NAME", "BAAI/bge-base-en-v1.5")


# Monitoring ###########################################
langfuse_callback_handler = LlamaIndexCallbackHandler()


# Configure LlamaIndex and API logic
Settings.embed_model = FastEmbedEmbedding(model_name=EMBED_MODEL_NAME)
Settings.llm = LLM
Settings.callback_manager = CallbackManager([langfuse_callback_handler])

BASE_CONFIG = {"multistep": False, "hyde": True, "rerank": True}
FALLBACK_RESPONSE = "Sorry, I was not able to find an answer for that."

DATABASE_URL = os.environ.get("DATABASE_URL")
DB_ENGINE = create_engine(DATABASE_URL)
