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

bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
)

def get_hf_model(model_name="mistralai/Mistral-7B-Instruct-v0.2", max_new_tokens=1024, **kwargs):
        model = AutoModelForCausalLM.from_pretrained(
                model_name,
                quantization_config=bnb_config,
                low_cpu_less_usage=True,
                device_map="mps"
        )
        return model

def get_hf_model_gguf(model_name="/Users/chessman/Desktop/ML_DL/RAG_Deployment/src/base/mistral-7b-instruct-v0.2.Q4_K_S.gguf", max_new_tokens=1024, temperature=0.2):
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
        print(llm)
        # Use CPU---------
        return llm

def creat_prompt(template):
        prompt = PromptTemplate(template = template, input_variables=["question"])
        return prompt


def create_simple_chain(prompt, llm):
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    return llm_chain

# template = """<|im_start|>system
# You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.<|im_end|>
# <|im_start|>user
# {question}<|im_end|>
# <|im_start|>assistant"""

# # # Tao simple chain

# prompt = creat_prompt(template)
# llm = get_hf_model_gguf()
# llm_chain = create_simple_chain(prompt, llm)
# # get_hf_model_gguf()
# question = "1 plus 1?"
# response = llm_chain.invoke({"question":question})
# print(response)

# template = """<|im_start|>system
# Bạn là một trợ lí AI hữu ích. Hãy trả lời người dùng một cách chính xác.
# <|im_end|>
# <|im_start|>user
# {question}<|im_end|>
# <|im_start|>assistant"""

# prompt = creat_prompt(template)
# llm = get_hf_model_gguf()
# llm_chain = create_simple_chain(prompt, llm)

# question = "Một cộng một bằng mấy?"
# response = llm_chain.invoke({"question":question})
# print(response)