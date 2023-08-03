import gradio as gr
import openai
import json
from factool import Factool
import os


def chat_with_gpt(api_key, model, message):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
      model=model,
      messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message},
        ]
    )
    return response.choices[0].message['content']

def fact_check(openai_api_key, serper_api_key, scraper_api_key, model, message, response, category):
    os.environ['SCRAPER_API_KEY'] = ''
    os.environ['SERPER_API_KEY'] = ''
    os.environ['OPENAI_API_KEY'] = ''
    os.environ['SCRAPER_API_KEY'] = scraper_api_key
    os.environ['SERPER_API_KEY'] = serper_api_key
    os.environ['OPENAI_API_KEY'] = openai_api_key
    factool_instance = Factool(model)
    inputs = [
            {
                "prompt": message,
                "response": response,
                "category": category,
                "search_type": "online",
            },
    ]
    response_list = factool_instance.run(inputs)
    os.environ['SCRAPER_API_KEY'] = ''
    os.environ['SERPER_API_KEY'] = ''
    os.environ['OPENAI_API_KEY'] = ''
    return response_list

with gr.Blocks() as demo:
    openai_api_key = gr.Textbox(label="OpenAI API Key")
    serper_api_key = gr.Textbox(label="Serper API Key")
    scraper_api_key = gr.Textbox(label="Scraper API Key")
    chat_model = gr.inputs.Radio(choices=["gpt-3.5-turbo", "gpt-4"], label="Chat Model")
    prompt = gr.Textbox(label="Prompt")
    response = gr.Textbox(label="Response")
    category = gr.inputs.Radio(choices=["kbqa", "code", "math", "scientific"], label="Category")
    fact_check_model = gr.inputs.Radio(choices=["gpt-3.5-turbo", "gpt-4"], label="Fact Check Model")
    fact_check_result = gr.Textbox(label="Fact Check Result")
    chat_btn = gr.Button("Chat")
    fact_check_btn = gr.Button("Fact Check")
    chat_btn.click(chat_with_gpt, inputs=[openai_api_key,chat_model,prompt], outputs=response)
    fact_check_btn.click(fact_check, inputs=[openai_api_key,serper_api_key,scraper_api_key,fact_check_model,prompt,response,category], outputs=fact_check_result)

demo.launch(share=True)

