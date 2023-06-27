from langchain.llms import TextGen, HuggingFacePipeline
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceInstructEmbeddings


embeddings = HuggingFaceInstructEmbeddings(model_name=EMBEDDING_MODEL_NAME, model_kwargs={"device": "cuda"})
llm = TextGen(model_url = "http://localhost:5000")
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)


def query(msg):
  return msg
