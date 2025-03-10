from openai import AzureOpenAI
from csv import writer
from gTTS import get_speech
import os, faiss, pickle, time
import streamlit as st
import numpy as np
import pandas as pd
from STT import convert_speech_text
from pythonosc import udp_client
from audio2face_streaming_utils import main
from OSC_Sender import send_talkmode, send_dancemode

# Creates a ChatGPT client based on the key, endpoint and version details given below
client = AzureOpenAI(
    api_key=os.getenv('AZURE_KEY'),
    azure_endpoint=os.getenv('AZURE_ENDPOINT'),
    api_version="2023-12-01-preview",
)


###################################
# STEP 1: Load Index and Knowledge Base
###################################

def load_index(pickle_path, faiss_index_path): 
    # Pickle is a Python library used for serializing and deserializing Python objects.
    # Serialization: Converting a Python object (like a list, dictionary, DataFrame, etc.) into a byte stream.
    # Deserialization: Converting the byte stream back into the original Python object.
    with open(pickle_path, "rb") as f:
        context = pickle.load(f)
    index = faiss.read_index(faiss_index_path)
    return index, context

###################################
# STEP 2: Get Similarity Between Prompt and Knowledge Base
###################################

def get_similarity(index, knowledge, prompt, k):
    response = client.embeddings.create(model="text-embedding-ada-002", input=[prompt])
    embedding = response.data[0].embedding

    embedding_array = np.array(embedding).astype("float32")
    embedding_array = embedding_array.reshape(-1, embedding_array.shape[0])

    D, I = index.search(embedding_array, k=k)
    indices = I[0]

    selected = ""
    for i in indices:
        selected += "\n" + knowledge.iloc[i]

    return selected

###################################
# STEP 3: Generate Response from ChatGPT
###################################

def get_response(prompt):
    """Generate a response from ChatGPT based on a given prompt"""
    knowledge_index, knowledge_pkl = load_index(
        "knowledge/knowledge.pkl", "knowledge/knowledge_index.txt"
    )
    context_text = get_similarity(knowledge_index, knowledge_pkl, prompt, 3)
    
    # Constructing the message for the GPT model
    messages = [
        {
            "role": "user",
            "content": f"Imagine you are having a conversation. Answer questions as truthfully as possible getting your response and speaking style from the provided context, and speak conversationally, giving them cues or questions to respond to also. Use a maximum of forty-five words in your response. Answer as if you are the person in the provided context, using their writing style, their language, their structure, their tone and any abbreviations \n Context: {context_text} + \n Question: {prompt}",
        },
    ]
    
    # Send the message to GPT-4 model and get the response
    response = client.chat.completions.create(
        model="GPT-4", messages=messages, temperature=0.001  # , stream=True
    )
    answer = response.choices[0].message.content
    
    # Return the generated response
    return answer

###################################
# STEP 4: Main Program Logic
###################################

if __name__ == "__main__":
    
    # time.sleep(31.0)

    print("Hi! I am a chatbot.")
    prompt = ""
    prompt_index = 0
    
    print("Talk to me")
    
    while True:  # Keep the loop running indefinitely
        prompt = convert_speech_text(prompt_index)  # Get the speech-to-text result
        
        # prompt = 'What is the sound of your favorite drum'
        if prompt:  # If speech is recognized
            prompt_index += 1

            # if prompt_index > 0:
            #     send_dancemode() 
            
            # if prompt_index > 0: #ONLY TO BE USED WITH PRE-TYPED PROMPT
            #     send_dancemode() 

            
            print(f"YOU: {prompt}")
            
            # Generate a response and proceed
            answer = get_response(prompt)
            # print(prompt_index)
            print(f"ANSWER: {get_response(prompt)}\n")

            get_speech(answer)
            send_talkmode()

            main('voices/audio.wav', '/World/audio2face/PlayerStreaming')

        else:
            print("Could not recognize speech. Please try again.")
            send_dancemode()
            continue  # Continue to listen for speech again


    