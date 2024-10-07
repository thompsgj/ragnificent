from llama_index.core.indices.postprocessor import SentenceTransformerRerank
from llama_index.core.indices.query.query_transform.base import (
    StepDecomposeQueryTransform,
)
from llama_index.core import VectorStoreIndex
from llama_index.core.indices.query.query_transform import HyDEQueryTransform
from llama_index.core.query_engine import MultiStepQueryEngine, TransformQueryEngine
from llama_index.vector_stores.qdrant import QdrantVectorStore

from backend.constants import BASE_CONFIG, FALLBACK_RESPONSE, VECTOR_STORE, Settings
from backend.utils.prompts import CUSTOM_HYDE_PROMPT, SELF_REFLECTION_PROMPT
from backend.utils.ingest import retrieve_index


def set_up_hyde(query_engine) -> TransformQueryEngine:
    hyde = HyDEQueryTransform(include_original=True, hyde_prompt=CUSTOM_HYDE_PROMPT)
    query_engine_hyde = TransformQueryEngine(query_engine, hyde)
    return query_engine_hyde


def set_node_postprocessors(config: dict) -> list:
    node_postprocessors = []

    if config.get("rerank", False) == True:
        rerank = SentenceTransformerRerank(top_n=2, model="BAAI/bge-reranker-base")
        node_postprocessors.append(rerank)
    return node_postprocessors


def set_up_multistep_query_transformation(query_engine) -> MultiStepQueryEngine:
    step_decompose_transform = StepDecomposeQueryTransform(
        llm=Settings.llm, verbose=True
    )
    query_engine_multistep = MultiStepQueryEngine(
        query_engine=query_engine,
        query_transform=step_decompose_transform,
        index_summary="Used to answer questions about Python programming style and best practices",
    )
    return query_engine_multistep


def add_query_transformations_to_query_engine(query_engine, config: dict):
    """Adds selected query transformation techniques"""
    if config.get("multistep", False) == True:
        query_engine = set_up_multistep_query_transformation(query_engine)

    if config.get("hyde", False) == True:
        query_engine = set_up_hyde(query_engine)
    return query_engine


def create_query_engine(
    index: VectorStoreIndex, node_postprocessors: list, config: dict
):
    """Creates a query engine on the document index and adds tools for retrieval"""
    query_engine = index.as_query_engine(
        similarity_top_k=2,
        sparse_top_k=12,
        vector_store_query_mode="hybrid",
        node_postprocessors=node_postprocessors,
    )
    query_engine = add_query_transformations_to_query_engine(query_engine, config)

    return query_engine


def check_response_with_llm(
    query: str, response: str, self_reflection_prompt=SELF_REFLECTION_PROMPT
):
    self_reflection_prompt = self_reflection_prompt.replace("\n{query}\n", query)
    self_reflection_prompt = self_reflection_prompt.replace("\n{response}\n", response)
    response = Settings.llm.complete(prompt=self_reflection_prompt)
    if "yes" in str(response).lower():
        return True
    return False


def query_vector_store(
    query: str,
    vector_store: QdrantVectorStore = VECTOR_STORE,
    config: dict = BASE_CONFIG,
):
    """Attempts to find an answer in the saved documents
    using the query_engine configurations
    """
    index = retrieve_index(vector_store)

    node_postprocessors = set_node_postprocessors(config)
    query_engine = create_query_engine(index, node_postprocessors, config)

    response = query_engine.query(query)

    is_relevant_response = check_response_with_llm(query, str(response))
    if is_relevant_response:
        return response
    return FALLBACK_RESPONSE
