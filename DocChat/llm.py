import logging

from langchain.llms import TextGen, HuggingFacePipeline
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceInstructEmbeddings

from repository import getDB
from settings import LLM_URL

qa = None

def setupLLM():
  logging.info("Setting up LLM")
  global qa
  qa = None
  db = getDB()
  if db is None:
    logging.error("DB not present!, LLM not set")
    return
  llm = TextGen(model_url = LLM_URL)
  qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=db.as_retriever(), return_source_documents=True)
  logging.info("LLM set to Text Gen at " + LLM_URL)

def query(msg):
  if qa is None:
    setupLLM()
    if qa is None:
      return "LLM is not set, please set LLM conectivity or construct db."
  return qa(msg)["result"]
