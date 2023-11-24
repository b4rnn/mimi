from __future__ import print_function
from flask import Flask, request, abort,jsonify
app = Flask(__name__)
# Routing call messages

#________________________
import sys
import os.path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

#from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex, LLMPredictor, ServiceContext,StorageContext, load_index_from_storage
#from langchain import OpenAI
#from llama_index.chat_engine import SimpleChatEngine
#from langchain.llms import OpenAI
import gradio as gr
import os
#import openai
from openai import OpenAI
#client = OpenAI()

os.environ["OPENAI_API_KEY"] = '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'
#openai.api_key ='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'

#openai.api_key = os.getenv('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')

messages = [
    {"role": "system", "content": "You are a helpful and kind AI Assistant.You specialize in adhd ,aspergers,depression,ocd and ptsd.Your name is Gundua."},
]

client = OpenAI(api_key ='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')
audio_dir ='/var/lib/asterisk/sounds/bot'

def construct_index(directory_path):
    num_outputs = 512

    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.7, model_name="text-davinci-003", max_tokens=num_outputs))

    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

    docs = SimpleDirectoryReader(directory_path).load_data()

    index = GPTVectorStoreIndex.from_documents(docs, service_context=service_context)

    #index.save_to_disk('index.json')
    index.storage_context.persist(persist_dir='index.json')

    return index

def chatbot(input_text):
    #storage_context = StorageContext.from_defaults(persist_dir="index.json")
    #index = load_index_from_storage(storage_context)
    #index = GPTVectorStoreIndex.load_from_disk('index.json')
    #query_engine = index.as_chat_engine(chat_mode='react', verbose=True)
    #response = query_engine.chat(input_text)
    #chat_engine = SimpleChatEngine.from_defaults()
    #chat_engine.chat_repl()
    #return response.response
    messages.append({"role": "user", "content": input_text})
    chat = openai.completions.create(model="gpt-3.5-turbo", messages=messages,max_tokens = 2048,temperature = 0.2,)
    reply = chat.choices[0].message.content
    return reply
'''
iface = gr.Interface(fn=chatbot,
                     inputs=gr.Textbox(lines=7, label="Enter your text"),
                     outputs="text",
                     title="Custom-trained AI Chatbot")

#index = construct_index("docs")
iface.queue().launch(share=True)
'''

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        #Get transcribe audio to text ...from voice input
        dict=request.json
        print(dict)
        input_text =dict.get('data')
        tel = dict.get('tel')
        messages.append({"role": "user", "content": input_text})
        chat = client.chat.completions.create(model="gpt-4", messages=messages,temperature = 0,max_tokens=256)
        reply = chat.choices[0].message.content
        #reply = chat.choices[0]
        print(reply)
        response = client.audio.speech.create(model="tts-1",voice="alloy",input=reply,)
        response.stream_to_file(audio_dir+"/"+tel+".wav")
        #push the query to the a model
        return 'success', 200
    else:
        abort(400)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
