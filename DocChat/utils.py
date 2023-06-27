import os, shutil, logging

from constants import DOCS_DIR, DB_DIR
from repository import ingest

def upload(src_path):
    trg_path = DOCS_DIR + os.path.basename(src_path)
    logging.info(f"Uploading: {trg_path}")
    shutil.copyfile(src_path, trg_path)
    
def process_files(files):
    if not files:
        return "no files selected"
    for fileobj in files:
        upload(fileobj.name)
    return str(len(files)) + " uploaded!"

def clearClicked():
    print("clear button clicked")
    
def pre_run_provision():
    provision_dirs()

def get_current_documents_filenames():
    response = "# Current file sources\n\n"
    for f in os.listdir(DOCS_DIR):
        response+=" - " + f + "\n"
    return response
def clearDB():
    logging.error("clearDB not implemented")

def loadDB():
    ingest()

def clearDocuments():
    # TODO delete files in folder
    folder_path = DOCS_DIR
    logging.info(f"Clearing docs folder: {folder_path}")
    for file_object in os.listdir(folder_path):
        file_object_path = os.path.join(folder_path, file_object)
        if os.path.isfile(file_object_path) or os.path.islink(file_object_path):
            os.unlink(file_object_path)
        else:
            shutil.rmtree(file_object_path)
    return "# Current file sources\n\n"
    
def create_dir(path):
    if not os.path.exists(path):
        logging.info(f"Creating folder: {path}")
        os.makedirs(path)
    
def provision_dirs():
    create_dir(DOCS_DIR)
    create_dir(DB_DIR)
