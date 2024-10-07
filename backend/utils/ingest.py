from llama_index.core import (
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
)
from llama_index.core.extractors import QuestionsAnsweredExtractor
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import TokenTextSplitter

from backend.constants import VECTOR_STORE, Settings


def set_transformations() -> list:
    """Configures how a document should be changed for the vector store"""
    text_splitter = TokenTextSplitter(separator=" ", chunk_size=350, chunk_overlap=50)
    extractors = [
        QuestionsAnsweredExtractor(questions=2),
    ]
    transformations = [text_splitter] + extractors
    return transformations


def transform_document_to_nodes(documents, transformations):
    """Applies transformations to document to break it into nodes"""
    pipeline = IngestionPipeline(transformations=transformations)

    nodes = pipeline.run(
        documents=documents, in_place=True, show_progress=True, num_workers=8
    )
    return nodes


def retrieve_index(vector_store, nodes=None):
    """Returns updated index with new content nodes, or
    returns existing index
    """
    if nodes:
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex(
            nodes=nodes, storage_context=storage_context, show_progress=True
        )
    else:
        index = VectorStoreIndex.from_vector_store(vector_store)
    return index


def create_vector_store_from_nodes(vector_store, documents):
    """Creates and adds new content to a vector store
    If vector store table already exists, adds content to it
    """
    transformations = set_transformations()
    nodes = transform_document_to_nodes(documents, transformations)
    index = retrieve_index(vector_store, nodes)
    return index


if __name__ == "__main__":
    documents = SimpleDirectoryReader("data/style").load_data()
    create_vector_store_from_nodes(VECTOR_STORE, documents)
