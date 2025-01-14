from typing import Union
from langchain.vectorstores import Chroma, FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from torch import embedding


class VectorDB:
	def __init__(self, documents=None, 
							vector_db: Union[Chroma, FAISS] = Chroma,
							embeddings = HuggingFaceEmbeddings()):
			self.vector_db = vector_db
			self.embeddings = embeddings
			self.db = self.build_db(documents)

	def build_db(self, documents):
			db = self.vector_db.from_documents(
					documents=documents,
					embedding=self.embeddings
			)
			return db

	def get_retriever(self, search_type="similarity", search_kwargs:dict = {"k": 10}):
			retriever = self.db.as_retriever(
					search_type=search_type, 
					search_kwargs=search_kwargs
			)
			return retriever