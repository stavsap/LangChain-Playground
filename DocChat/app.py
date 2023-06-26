import gradio as gr
import os, random, shutil, time

css = """
#btn-pmargin-bottom {margin-bottom: 20px}
"""

def upload(filename, path):
    print(path)
    shutil.copyfile(fileobj.name, path)
    
def process_files(files):
    if not files:
        return "no files selected"
    for fileobj in files:
        upload(fileobj.name, os.path.basename(fileobj.name))
    return str(len(files)) + " uploaded!"

def clearClicked():
    print("clear button clicked")
    
uploadDocs = gr.Interface(
        fn=process_files,
        inputs=[
            gr.File(file_types=[".txt",".xls",".xlsx",".csv",".pdf"], file_count="multiple")
        ],
        outputs=gr.Markdown(),
        allow_flagging="never"
    )
    
with gr.Blocks(css=css) as demo:
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

demo.launch()
