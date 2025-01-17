from pydantic import BaseModel, Field
from src.rag.file_loader import Loader
from src.rag.vector_db import VectorDB
from src.rag.rag_llm import RagLLM

class InputQA(BaseModel):
    question: str = Field(..., title="Question to ask model")

class OutputQA(BaseModel):
	answer: str = Field(..., title="Answer from the model")

def build_rag_chain(llm, data_path, data_type):
	docs_loader = Loader(file_type=data_type).load_dir(data_path, workers=2)
	retriever = VectorDB(documents=docs_loader).get_retriever()
	rag_chain = RagLLM(llm).get_chain(retriever)
	return rag_chain
