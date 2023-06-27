import os, logging

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed

from langchain.docstore.document import Document
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.text_splitter import Language, RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

from constants import (
    CHROMA_SETTINGS,
    DOCUMENT_MAP,
    INGEST_THREADS,
    DB_DIR,
    DOCS_DIR,
)

from settings import EMBEDDING_MODEL_NAME

db = None

def load_single_document(file_path: str) -> Document:
    file_extension = os.path.splitext(file_path)[1]
    loader_class = DOCUMENT_MAP.get(file_extension)
    if loader_class:
        loader = loader_class(file_path)
    else:
        raise ValueError("Document type is undefined")
    return loader.load()[0]


def load_document_batch(filepaths):
    logging.info("Loading document batch")
    with ThreadPoolExecutor(len(filepaths)) as exe:
        futures = [exe.submit(load_single_document, name) for name in filepaths]
        data_list = [future.result() for future in futures]
        return (data_list, filepaths)


def load_documents(source_dir: str) -> list[Document]:
    all_files = os.listdir(source_dir)
    paths = []
    for file_path in all_files:
        file_extension = os.path.splitext(file_path)[1]
        source_file_path = os.path.join(source_dir, file_path)
        if file_extension in DOCUMENT_MAP.keys():
            paths.append(source_file_path)

    n_workers = min(INGEST_THREADS, max(len(paths), 1))
    chunksize = round(len(paths) / n_workers)
    docs = []
    with ProcessPoolExecutor(n_workers) as executor:
        futures = []
        for i in range(0, len(paths), chunksize):
            filepaths = paths[i : (i + chunksize)]
            future = executor.submit(load_document_batch, filepaths)
            futures.append(future)
        for future in as_completed(futures):
            contents, _ = future.result()
            docs.extend(contents)

    return docs

def split_documents(documents: list[Document]) -> tuple[list[Document], list[Document]]:
    # Splits documents for correct Text Splitter
    text_docs, python_docs = [], []
    for doc in documents:
        file_extension = os.path.splitext(doc.metadata["source"])[1]
        if file_extension == ".py":
            python_docs.append(doc)
        else:
            text_docs.append(doc)

    return text_docs, python_docs

def provisionDB():
    global db
    if db is None:
        embeddings = HuggingFaceInstructEmbeddings(model_name=EMBEDDING_MODEL_NAME, model_kwargs={"device": "cuda"})
        db = Chroma(
                persist_directory=DB_DIR,
                embedding_function=embeddings,
                client_settings=CHROMA_SETTINGS,
            )
        db.persist()

def dropDB():    
    logging.info("Dropping current embeddings")
    db.delete(db.get()["ids"])
    
def getDB():
    global db
    provisionDB()
    return db

def ingest(device_type = "cuda"):

    global db
    
    logging.info(f"Loading documents from {DOCS_DIR}")
    
    documents = load_documents(DOCS_DIR)

    logging.info("Found "+str(len(documents))+" documents")
    
    text_documents, python_documents = split_documents(documents)
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    
    python_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON, chunk_size=1000, chunk_overlap=200
    )
    texts = text_splitter.split_documents(text_documents)
    
    texts.extend(python_splitter.split_documents(python_documents))
    
    logging.info(f"Loaded {len(documents)} documents from {DOCS_DIR}")
    
    logging.info(f"Split into {len(texts)} chunks of text")

    dropDB()

    logging.info("Saving new embeddings")

    db.add_documents(texts)
    
    db.persist()

    logging.info("All complete, all embeddings persisted")
