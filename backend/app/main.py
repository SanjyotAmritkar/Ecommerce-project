# app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.rag import retrieve_and_answer

app = FastAPI()

origins = ["http://localhost:5173"]  # Vite default

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query_bot(req: QueryRequest):
    answer = retrieve_and_answer(req.question)
    return {"response": answer}
