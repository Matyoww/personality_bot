import os
import random
import dotenv
import streamlit as st
import google.generativeai as genai

dotenv.load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Setup
class Personality:
    def __init__(self):
        self.personalities = ['child', 'teenager', 'adult', 'elderly', 'robot', 'alien', 'vampire', 'zombie', 'ghost', 'pirate', 'ninja', 'wizard', 'superhero', 'supervillain', 'detective', 'spy', 'cowboy', 'nurse', 'doctor', 'teacher', 'professor', 'student', 'athlete', 'chef', 'artist', 'musician', 'writer', 'scientist', 'engineer', 'inventor', 'entrepreneur', 'politician', 'celebrity', 'royalty', 'historical figure', 'mythical creature', 'animal', 'plant', 'object', 'abstract concept', 'random']

    def pick_personality(self):
        return random.choice(self.personalities)

def update_model():
    return genai.GenerativeModel("gemini-1.5-flash", system_instruction=f"You are an intelligent chatbot but answers like a {st.session_state.chosen_personality}. You can only answer about programming and provide code suggestions.")



# Streamlit UI
st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="wide")
st.title("Chat with a bot with different personalities! 🤖")

with st.sidebar:
    st.session_state.is_random = st.toggle("Randomize", True)
    st.session_state.selectbox_personality = st.selectbox("Personality: ", Personality().personalities, disabled=st.session_state.is_random)
    if st.session_state.is_random:
        st.session_state.chosen_personality = Personality().pick_personality()
    else:
        st.session_state.chosen_personality = st.session_state.selectbox_personality
    st.write("Current personality: ", st.session_state.chosen_personality)


if "messages" not in st.session_state:
    st.session_state.messages = []

model = update_model()
chat = model.start_chat(history=st.session_state.messages)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["parts"])


# Chat
prompt = st.chat_input("Type your message here...")

if prompt:
    st.session_state.messages.append({"role": "user", "parts": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        response = chat.send_message(prompt)
        st.write(response.text)

    st.session_state.messages.append({"role": "assistant", "parts": response.text})
    if st.session_state.is_random:
        st.session_state.chosen_personality = Personality().pick_personality()