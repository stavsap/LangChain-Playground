import logging

from langchain.llms import TextGen, HuggingFacePipeline
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceInstructEmbeddings

from repository import getDB

qa = None

def setupLLM():
  logging.info("Setting up LLM")
  global qa
  qa = None
  db = getDB()
  if db is None:
    logging.error("DB not present!, LLM not set")
    return
  logging.info("Connecting to Text Gen at http://localhost:5000")
  llm = TextGen(model_url = "http://localhost:5000")
  qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=db.as_retriever(), return_source_documents=True)
  logging.info("LLM set to Text Gen at http://localhost:5000")

def query(msg):
  if qa is None:
    setupLLM()
    if qa is None:
      return "LLM is not set, please set LLM conectivity or construct db."
  return qa(msg)["result"]
