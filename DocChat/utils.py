import os, shutil, logging

from constants import DOCS_DIR

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

def provision_dirs():
    os.makedirs(DOCS_DIR)
