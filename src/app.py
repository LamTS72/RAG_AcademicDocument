import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes

from src.base.llm_model import get_hf_model_gguf
from src.rag.main import build_rag_chain, InputQA, OutputQA

llm = get_hf_model_gguf(temperature=0.2)
path_docs = "./docs/"
print("GET MODEL SUCCESSFUL")
#------------------------CHAINS----------------------------------
genai_chain = build_rag_chain(llm, data_path=path_docs, data_type="pdf")
print("BUILD MODEL SUCCESSFUL")
#------------------------APP - FAST-API------------------------
app = FastAPI(
	title="LangChain Server",
	version="1.0",
	description="A simple API LangChain Server Runnable interface",
)

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
	expose_headers=["*"],
)

#------------------------ROUTES - FAST-API---------------------
@app.get("/check")
async def check():
	return {"status":"ok"}

@app.post("/generative_ai", response_model=OutputQA)
async def genative_ai(inputs: InputQA):
	answer  = genai_chain.invoke(inputs.question)
	return {"answer": answer}


#--------LANGSERVE ROUTES - PLAYGROUND-------------
add_routes(app, genai_chain, playground_type="default", path="/generative_ai")

