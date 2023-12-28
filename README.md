# LangChain-Playground

## 🚦 WIP 🚦

[LangChain](https://github.com/hwchase17/langchain) playground to explore different use cases.

[LangChain Doc](https://python.langchain.com/docs/get_started/introduction.html)

## [DocChat](DocChat/README.md)

A small [gradio](https://gradio.app/) chat bot with [chroma](https://www.trychroma.com) and langchain integration, works with [text-generation-webui](https://github.com/oobabooga/text-generation-webui) to get LLM via api.

## Environment Variables

- DEVICE_TYPE - set the device type for the embedding db, default is 'cpu', can e also 'cude'.

## Setup

```shell
pip install -r requirements.txt
```

## windows cuda support

```shell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

## Tutorials 

https://www.mlexpert.io/prompt-engineering/chatbot-with-local-llm-using-langchain