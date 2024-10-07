from fastapi import FastAPI
from starlette import status
from starlette.requests import Request

from backend.schemas import QueryMessage, QueryResponseModel, UserQueryFeedback
from backend.utils.message_logging import log_message, log_answer, log_feedback
from backend.utils.query import query_vector_store

app = FastAPI()


@app.post("/queries/{query_id}/feedback", status_code=status.HTTP_201_CREATED)
def send_feedback(query_id: int, request: Request, payload: UserQueryFeedback):
    rating = payload.rating
    log_feedback(query_id, rating)


@app.post("/queries", response_model=QueryResponseModel)
def answer_question(request: Request, payload: QueryMessage):
    query = payload.query
    query_id = log_message(query)
    response = query_vector_store(query)
    log_answer(query_id, str(response))
    return {"answer": str(response), "query_id": query_id}
