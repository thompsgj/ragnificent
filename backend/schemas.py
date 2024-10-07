from pydantic import BaseModel


class QueryMessage(BaseModel):
    query: str


class QueryResponseModel(BaseModel):
    answer: str
    query_id: int


class UserQueryFeedback(BaseModel):
    rating: int
