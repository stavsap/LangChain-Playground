import os
from chromadb.config import Settings
from langchain.document_loaders import CSVLoader, PDFMinerLoader, TextLoader, UnstructuredExcelLoader

ROOT_DIR = os.path.dirname(os.path.realpath(__file__)) + os.sep

DOCS_DIR = f"{ROOT_DIR}docs{os.sep}"

DB_DIR = f"{ROOT_DIR}db{os.sep}"

SETTINGS_FILE_PATH = f"{ROOT_DIR}.settings"

INGEST_THREADS = (os.cpu_count() -1) or 3

CHROMA_SETTINGS = Settings(
    persist_directory=DB_DIR, anonymized_telemetry=False
)

DOCUMENT_MAP = {
    ".txt": TextLoader,
    ".py": TextLoader,
    ".pdf": PDFMinerLoader,
    ".csv": CSVLoader,
    ".xls": UnstructuredExcelLoader,
    ".xlxs": UnstructuredExcelLoader,
}


