import os, shutil, logging

def upload(src_path, trg_path):
    logging.info(f"Uploading: {trg_path}")
    shutil.copyfile(src_path, trg_path)
    
def process_files(files):
    if not files:
        return "no files selected"
    for fileobj in files:
        upload(fileobj.name, os.path.basename(fileobj.name))
    return str(len(files)) + " uploaded!"

def clearClicked():
    print("clear button clicked")
