import gradio as gr
import time,logging

from css import CSS
from utils import process_files, clearClicked, pre_run_provision, get_current_documents_filenames, clearDocuments, clearDB, loadDB
from llm import query
from settings import saveSettings, Settings, getSettings,GLOBAL_SETTINGS_MARKDOWN

def main(port):
    CURRENT_SETTINGS = getSettings()
    filesDataset = gr.Markdown(value=lambda: get_current_documents_filenames())
    def saveSettingsFN(textGenWebuiCheckbox, llmURL, textGenWebuiAuthCheckbox,
                                                          username, password, openaiCheckbox, openAIKey):
        saveSettings(Settings(textGenWebuiCheckbox,llmURL,textGenWebuiAuthCheckbox,username,password,openaiCheckbox,openAIKey))
    def upload_files(files):
        response = process_files(files)
        return response, get_current_documents_filenames()
    def toogleAuth(enabled):
        return gr.Textbox.update(visible=enabled),gr.Textbox.update(visible=enabled)
    def toogleBox(enabled):
        return gr.Box.update(visible=enabled)

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
                textGenWebuiCheckbox = gr.Checkbox(value=CURRENT_SETTINGS.enableTextGenWebui, label="Integrate With Text Gen Webui", interactive= True)
                with gr.Box(visible=CURRENT_SETTINGS.enableTextGenWebui) as textGenWebuibox:
                    llmURL = gr.Textbox(show_label=True, label="Text Gen WebUI URL", info="URL to text generator  webui working", value=CURRENT_SETTINGS.textGenWebuiURL, interactive = True)
                    textGenWebuiAuthCheckbox = gr.Checkbox(value=CURRENT_SETTINGS.textGenWebuiEnableAuth, label="Enable Auth",
                                                       interactive=True)
                    username = gr.Textbox(visible=CURRENT_SETTINGS.textGenWebuiEnableAuth,show_label=True, value=CURRENT_SETTINGS.textGenWebuiUsername, interactive = True, label="Username")
                    password = gr.Textbox(visible=CURRENT_SETTINGS.textGenWebuiEnableAuth,show_label=True, value=CURRENT_SETTINGS.textGenWebuiPassword, interactive = True, label="Password", type="password")
            with gr.Box():
                openaiCheckbox = gr.Checkbox(value=CURRENT_SETTINGS.openaiEnabled, label="Integrate With OpenAI",
                                                       interactive=True)
                with gr.Box(visible=CURRENT_SETTINGS.openaiEnabled) as openaiBox:
                    openAIKey = gr.Textbox(show_label=True, label="OpenAI API Key", info="Open AI API key to your account",
                                        value=CURRENT_SETTINGS.opeanAIApiKey, interactive=True)

            saveSettingsBtn = gr.Button("Save Settings", scale=2, min_width=200)

            openaiCheckbox.change(lambda x : gr.Checkbox.update(value=not x), inputs=openaiCheckbox, outputs=textGenWebuiCheckbox)
            openaiCheckbox.change(toogleBox, inputs=openaiCheckbox, outputs=openaiBox)

            textGenWebuiCheckbox.change(toogleBox, inputs=textGenWebuiCheckbox, outputs=textGenWebuibox)
            textGenWebuiCheckbox.change(lambda x : gr.Checkbox.update(value= not x), inputs=textGenWebuiCheckbox, outputs=openaiCheckbox)

            textGenWebuiAuthCheckbox.change(toogleAuth, inputs=textGenWebuiAuthCheckbox, outputs=[username, password])

            saveSettingsBtn.click(saveSettingsFN, inputs=[textGenWebuiCheckbox, llmURL, textGenWebuiAuthCheckbox,
                                                          username, password, openaiCheckbox, openAIKey])
            with gr.Box():
                gr.Markdown(value=GLOBAL_SETTINGS_MARKDOWN)
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
    )
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s", level=logging.DEBUG
    )
    app.launch(server_port=port)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
    )
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s", level=logging.DEBUG
    )
    print(f"\n ---- DocChat ---- \n")

    port = 8080

    pre_run_provision()

    main(port)
