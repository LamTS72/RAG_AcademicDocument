from pyexpat import model
import token
import torch
import sys
from transformers import(
        BitsAndBytesConfig,
        AutoTokenizer,
        AutoModelForCausalLM,
        AutoModel,
        pipeline,
)
# from langchain.llms.huggingface_pipeline import HuggingFacePipeline
from langchain_community.llms.ctransformers import CTransformers
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
# from utils import ConfigKey
# config = ConfigKey()

# Quantization model config
bnb_config = BitsAndBytesConfig(
	load_in_4bit=True,
	bnb_4bit_quant_type="nf4",
	bnb_4bit_use_double_quant=True,
	bnb_4bit_compute_dtype=torch.bfloat16,
)

# Define model 
def get_hf_model(model_name="mistralai/Mistral-7B-Instruct-v0.2", max_new_tokens=1024, **kwargs):
	model = AutoModelForCausalLM.from_pretrained(
		model_name,
		quantization_config=bnb_config,
		low_cpu_less_usage=True, # True if have accelerator lib
		device_map="mps"
	)
	return model

def get_hf_model_gguf(model_name="./models/mistral-7b-instruct-v0.2.Q4_K_S.gguf", max_new_tokens=1024, temperature=0.2):
	'''Create llm if have GPU
	Or use .GGUF for CPU through CTransformers
 	'''
	# Use GPU---------
	# model = AutoModelForCausalLM.from_pretrained(model_name, gguf_file="mistral-7b-instruct-v0.2.Q4_K_S.gguf")
	# print(model)
	# tokenizer = AutoTokenizer.from_pretrained("TheBloke/Mistral-7B-Instruct-v0.2-GGUF")
	# model_pipeline = pipeline(
	#         "text-generation",
	#         model=model,
	#         tokenizer=tokenizer,
	#         max_new_tokens=max_new_tokens,
	#         pad_token_id = tokenizer.eos_token_id,
	#         device_map="auto"
	# )
	# llm = HuggingFacePipeline(
	#         pipeline=model_pipeline,
	#         model_kwargs={
	#                 "temperature":0.2
	#         }
	# )
	# Use GPU---------
	
	# Use CPU---------
	llm = CTransformers(
			model=model_name,
			max_new_tokens=max_new_tokens,
			model_type="llama",
			temperature=temperature,                
	)
	# Use CPU---------
	return llm


