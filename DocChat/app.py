import gradio as gr
import os, random, time, logging

from css import CSS
from utils import process_files, clearClicked, pre_run_provision

def main(port):
    
    uploadDocs = gr.Interface(
            fn=process_files,
            inputs=[
                gr.File(file_types=[".txt",".xls",".xlsx",".csv",".pdf"], file_count="multiple")
            ],
            outputs=gr.Markdown(),
            allow_flagging="never"
        )
        
    with gr.Blocks(css=CSS) as app:
        with gr.Tab("Chat"):
            chatbot = gr.Chatbot()
            msg = gr.Textbox(show_label=False)
            clear = gr.ClearButton([msg, chatbot])
            clear.click(clearClicked)
    
            def respond(message, chat_history):
                bot_message = random.choice(["Igor is going to do that!"])
                chat_history.append((message, bot_message))
                time.sleep(0.5)
                return "", chat_history
            msg.submit(respond, [msg, chatbot], [msg, chatbot])
            
        with gr.Tab("DB Load"):        
            with gr.Box():
                uploadDocs.render()
            with gr.Box():
                with gr.Column(scale=2, min_width=200):
                    gr.Button("Clear Files",elem_id="btn-pmargin-bottom")
                with gr.Column(scale=2, min_width=200):
                    gr.Button("Clear Files",elem_id="btn-pmargin-bottom")
                with gr.Column(scale=2, min_width=200):
                    gr.Button("Clear Files")
            with gr.Box():
                gr.Dataset(label="Files", components=["text"], samples=[["a.txt"],["b.txt"]])
                
        with gr.Tab("Settings"):        
            with gr.Box():
                msg = gr.Textbox(show_label=True,label="LLM Url",info="URL to text generator working with LLMs")
                gr.Button("Set", scale=2, min_width=200)
    
    app.launch(server_port=port)

if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s", level=logging.INFO
    )
    port = 8080
    pre_run_provision()
    main(port)
