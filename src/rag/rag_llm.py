import re
from langchain import hub
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate, ChatPromptTemplate



template = """<|im_start|>system
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.<|im_end|>
<|im_start|>user
Question: {question}\n
Context: {context}<|im_end|>
<|im_start|>assistant"""

class Str_OutputParser(StrOutputParser):
	def __init__(self):
			super().__init__()

	def parser(self, text):
			return self.extract_answer(text)
	
	def extract_answer(self, text_response,  pattern: str=r"(Answer: \s*(.*))|(<\|im_start\|>assistant \s*(.*))"):
		match = re.search(pattern, text_response, re.DOTALL)
		if match:
			answer_text = match.group(1).strip()
			end_pattern = r"<\|im_end\|\n>"
			return answer_text.replace(end_pattern, "")
		else:
			return text_response

class RagLLM():
	def __init__(self, llm) -> None:
		self.llm = llm
		self.prompt = hub.pull("rlm/rag-prompt")
		#self.prompt = self.create_prompt(template)
		self.str_parser = Str_OutputParser()

	def get_chain(self, retriever):
		input_data = {
			"context": retriever | self.format_docs,
			"question": RunnablePassthrough()
		}

		rag_chain = (
			input_data | self.prompt | self.llm | self.str_parser
		)
		return rag_chain
	
	def format_docs(self, docs):
		return "\n\n".join(doc.page_content for doc in docs)
	
	def create_prompt(self, template):
		prompt = PromptTemplate(template = template, input_variables=["question", "context"])
		return prompt

# a = RagLLM(None)
# print(a.prompt1)
# print(type(a.prompt1))
# print(a.prompt2)
# print(type(a.prompt2))