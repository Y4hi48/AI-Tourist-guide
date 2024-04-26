import os

from PIL import Image
import streamlit as st
from streamlit_option_menu import option_menu

from gemini_utility import (load_gemini_pro_model,
                            gemini_pro_response,
                            gemini_pro_vision_response)

working_dir = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="Tourist Guide AI",
    page_icon="🧠",
    layout="centered",
)

with st.sidebar:
    selected = option_menu('Tourist Guide AI',
                           ['ChatBot',
                            'Monument Detailing',
                            'Historic Info'],
                           menu_icon='globe2', icons=['chat-dots-fill', 'image-fill', 'patch-question-fill'],
                           default_index=0
                           )


# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role


# chatbot page
if selected == 'ChatBot':
    model = load_gemini_pro_model()

    if "chat_session" not in st.session_state:  
        st.session_state.chat_session = model.start_chat(history=[])

    st.title("🤖 Tourist Assistant")

    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    user_prompt = st.chat_input("Ask Tourist Guide")  
    if user_prompt:
        st.chat_message("user").markdown(user_prompt)

        gemini_response = st.session_state.chat_session.send_message(user_prompt)  

        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)


# Image captioning page
if selected == "Monument Detailing":

    st.title("📷 Monument Detailing")

    uploaded_image = st.file_uploader("Upload an image of a monument...", type=["jpg", "jpeg", "png"])

    if st.button("Generate Description"):
        image = Image.open(uploaded_image)

        col1, col2 = st.columns(2)

        with col1:
            resized_img = image.resize((800, 500))
            st.image(resized_img)

        default_prompt = "describe this monument for a tourist"

        caption = gemini_pro_vision_response(default_prompt, image)

        with col2:
            st.info(caption)


# text embedding model
if selected == "Historic Info":

    st.title("🔍 Historic Info")

    user_prompt = st.text_area(label='', placeholder="Ask a historic question...")

    if st.button("Get Response"):
        response = gemini_pro_response(user_prompt)
        st.markdown(response)
