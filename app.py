import streamlit as st
from openai import OpenAI
import ollama
import time
import json
import os
from datetime import datetime

# List of available models
MODELS = [
    "gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo-0125",  # OpenAI models
    "llama3.1:8b", "gemma2:2b", "mistral-nemo:latest", "phi3:latest",  # Ollama models
]

client = OpenAI()

def get_ai_response(messages, model):
    if model.startswith("gpt-"):
        return get_openai_response(messages, model)
    else:
        return get_ollama_response(messages, model)

def get_openai_response(messages, model):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content, response.usage.prompt_tokens, response.usage.completion_tokens
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None, 0, 0

def get_ollama_response(messages, model):
    try:
        response = ollama.chat(
            model=model,
            messages=messages
        )
        return response['message']['content'], response['prompt_eval_count'], response['eval_count']
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None, 0, 0

def stream_response(messages, model):
    if model.startswith("gpt-"):
        return stream_openai_response(messages, model)
    else:
        return stream_ollama_response(messages, model)

def stream_openai_response(messages, model):
    try:
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True
        )
        return stream
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def stream_ollama_response(messages, model):
    try:
        stream = ollama.chat(
            model=model,
            messages=messages,
            stream=True
        )
        return stream
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def save_conversation(messages, filename):
    conversation = {
        "timestamp": datetime.now().isoformat(),
        "messages": messages
    }
    
    os.makedirs('conversations', exist_ok=True)
    file_path = os.path.join('conversations', filename)
    
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                conversations = json.load(f)
        else:
            conversations = []
    except json.JSONDecodeError:
        conversations = []
    
    conversations.append(conversation)
    
    with open(file_path, 'w') as f:
        json.dump(conversations, f, indent=2)

def load_conversations(uploaded_file):
    if uploaded_file is not None:
        try:
            conversations = json.loads(uploaded_file.getvalue().decode("utf-8"))
            return conversations
        except json.JSONDecodeError:
            st.error(f"Error decoding the uploaded file. The file may be corrupted or not in JSON format.")
            return []
    else:
        st.warning("No file was uploaded.")
        return []

def main():
    st.set_page_config(layout="wide")
    st.title("Virtual Podcast App")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "token_count" not in st.session_state:
        st.session_state.token_count = {"prompt": 0, "completion": 0}

    st.sidebar.title("Podcast Settings")
    model = st.sidebar.selectbox("Choose a model", MODELS)

    # Podcast guest setup
    st.sidebar.subheader("Podcast Guests")
    num_guests = st.sidebar.number_input("Number of guests", min_value=2, max_value=5, value=2)
    guests = []
    for i in range(num_guests):
        guest_name = st.sidebar.text_input(f"Guest {i+1} Name", value=f"Guest {i+1}")
        guest_description = st.sidebar.text_area(f"Guest {i+1} Description", value="Enter a brief description of the guest's background and expertise.")
        guests.append({"name": guest_name, "description": guest_description})

    # Podcast topic and rounds
    topic = st.sidebar.text_input("Podcast Topic", "Enter the main topic of discussion for this podcast episode.")
    num_rounds = st.sidebar.number_input("Number of conversation rounds", min_value=1, max_value=10, value=5)

    if st.sidebar.button("Start Podcast"):
        st.session_state.messages = []
        st.session_state.token_count = {"prompt": 0, "completion": 0}

        # Initialize the podcast
        intro_message = f"Welcome to our virtual podcast on the topic of '{topic}'. Today, we have {num_guests} distinguished guests joining us:\n\n"
        for guest in guests:
            intro_message += f"- {guest['name']}: {guest['description']}\n"
        intro_message += f"\nLet's begin our {num_rounds}-round discussion!"

        st.session_state.messages.append({"role": "system", "content": "You are an AI moderator for a virtual podcast. Facilitate an engaging and informative conversation between the guests on the specified topic."})
        st.session_state.messages.append({"role": "assistant", "content": intro_message})

        for round in range(num_rounds):
            for guest in guests:
                ai_messages = [
                    {"role": "system", "content": f"You are now speaking as {guest['name']}. Remember their background: {guest['description']}"},
                ] + st.session_state.messages

                with st.chat_message("assistant"):
                    st.markdown(f"**{guest['name']}:**")
                    message_placeholder = st.empty()
                    full_response = ""
                    for chunk in stream_response(ai_messages, model):
                        if chunk:
                            if model.startswith("gpt-"):
                                full_response += chunk.choices[0].delta.content or ""
                            else:
                                full_response += chunk['message']['content']
                            message_placeholder.markdown(full_response + "▌")
                            time.sleep(0.05)
                    message_placeholder.markdown(full_response)

                st.session_state.messages.append({"role": "assistant", "content": f"{guest['name']}: {full_response}"})

                _, prompt_tokens, completion_tokens = get_ai_response(ai_messages, model)
                st.session_state.token_count["prompt"] += prompt_tokens
                st.session_state.token_count["completion"] += completion_tokens

        # Conclude the podcast
        conclude_message = "Thank you all for joining us for this fascinating discussion. Let's wrap up with some final thoughts from each of our guests."
        st.session_state.messages.append({"role": "assistant", "content": conclude_message})
        st.markdown(conclude_message)

    st.sidebar.subheader("Conversation Management")
    save_name = st.sidebar.text_input("Save podcast as:", "virtual_podcast.json")
    if st.sidebar.button("Save Podcast"):
        save_conversation(st.session_state.messages, save_name)
        st.sidebar.success(f"Podcast saved to conversations/{save_name}")

    st.sidebar.subheader("Load Podcast")
    uploaded_file = st.sidebar.file_uploader("Choose a file to load podcasts", type=["json"])
    
    if uploaded_file is not None:
        conversations = load_conversations(uploaded_file)
        if conversations:
            st.sidebar.success(f"Loaded {len(conversations)} podcasts from the uploaded file")
            selected_podcast = st.sidebar.selectbox(
                "Select a podcast to load",
                range(len(conversations)),
                format_func=lambda i: conversations[i]['timestamp']
            )
            if st.sidebar.button("Load Selected Podcast"):
                st.session_state.messages = conversations[selected_podcast]['messages']
                st.sidebar.success("Podcast loaded successfully!")
                st.experimental_rerun()

    st.sidebar.subheader("Token Usage")
    st.sidebar.write(f"Prompt tokens: {st.session_state.token_count['prompt']}")
    st.sidebar.write(f"Completion tokens: {st.session_state.token_count['completion']}")
    st.sidebar.write(f"Total tokens: {sum(st.session_state.token_count.values())}")

if __name__ == "__main__":
    main()