import os

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from pydantic import BaseModel

from apikey import apikey

os.environ['OPENAI_API_KEY'] = apikey

app = FastAPI(title = "LangChain Demo")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class InputItem(BaseModel):
    prompt: str

# Creating prompt templates
prompt_template1 = PromptTemplate(
    input_variables = ['topic'],
  template = 'Write a story title about {topic}.'
)


prompt_template2 = PromptTemplate(
  input_variables = ['title'],
  template = 'Write a complete short story with the title {title} using 500 words or less.'
)

memory = ConversationBufferMemory(input_key = 'topic', memory_key = 'chat_history')

@app.post("/")
async def root(item:InputItem):
    llm = OpenAI(temperature=0.9)
  
    title_chain = LLMChain(llm = llm, prompt = prompt_template1, verbose = True)
    script_chain = LLMChain(llm = llm, prompt = prompt_template2, verbose = True)
    seq_chain = SimpleSequentialChain(chains=[title_chain, script_chain], verbose = True)
    
    response = seq_chain.run({item.prompt})
    #response = {'response': item.prompt}
    
    return response