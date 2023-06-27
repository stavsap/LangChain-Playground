import gradio as gr
import random, time, logging

from css import CSS
from utils import process_files, clearClicked, pre_run_provision, get_current_documents_filenames, clearDocuments, clearDB, loadDB
from llm import query
from settings import LLM_URL, EMBEDDING_MODEL_NAME 

def main(port):
    filesDataset = gr.Markdown(value=lambda: get_current_documents_filenames())

    def upload_files(files):
        response = process_files(files)
        return response, get_current_documents_filenames()

    with gr.Blocks(css=CSS) as app:
        with gr.Tab("Chat"):
            chatbot = gr.Chatbot()
            msg = gr.Textbox(show_label=False)
            clear = gr.ClearButton([msg, chatbot])
            clear.click(clearClicked)

            def respond(message, chat_history):
                bot_message = query(message)
                chat_history.append((message, bot_message))
                time.sleep(0.5)
                return "", chat_history

            msg.submit(respond, [msg, chatbot], [msg, chatbot])

        with gr.Tab("DB Load"):
            with gr.Row():
                with gr.Column():
                    with gr.Box():
                        f = gr.File(file_types=[".txt", ".xls", ".xlsx", ".csv", ".pdf"], file_count="multiple")
                        with gr.Column(scale=2, min_width=200):
                            b = gr.Button("Upload Documents", elem_id="btn-pmargin-bottom")
                        status = gr.Markdown()
                        b.click(upload_files, inputs=[f], outputs=[status, filesDataset])
                with gr.Column():
                    with gr.Box():
                        with gr.Column(scale=2, min_width=200):
                            clearDbBtn = gr.Button("Clear DB", elem_id="btn-pmargin-bottom")
                            clearDbBtn.click(clearDB)
                        with gr.Column(scale=2, min_width=200):
                            loadDbBtn = gr.Button("Load DB", elem_id="btn-pmargin-bottom")
                            loadDbBtn.click(loadDB)
                        with gr.Column(scale=2, min_width=200):
                            clearBtn = gr.Button("Clear Files")
                            clearBtn.click(clearDocuments, outputs=[filesDataset])

            with gr.Box():
                filesDataset.render()

        with gr.Tab("Settings"):
            with gr.Box():
                gr.Textbox(show_label=True, label="LLM Url", info="URL to text generator working with LLMs", value=LLM_URL)
                gr.Markdown(value="Embedding model in use: " + EMBEDDING_MODEL_NAME)
                gr.Button("Save Settings", scale=2, min_width=200)
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s", level=logging.INFO
    )
    app.launch(server_port=port)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s", level=logging.INFO
    )
    print(f"\n ---- DocChat ---- \n")

    port = 8080

    pre_run_provision()

    main(port)
