import streamlit as st
from groq import Groq
import logging
from PIL import Image, ImageEnhance
import time
import json
import requests
import base64

#logging.basicConfig(level=logging.INFO)

# Constants
NUMBER_OF_MESSAGES_TO_DISPLAY = 20
API_DOCS_URL = "https://docs.streamlit.io/library/api-reference"

# Inizializza il client con la chiave API di Groq
client = Groq(api_key="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")

# Streamlit Page Configuration
st.set_page_config(
    page_title="Mindy - An Intelligent For Assistant",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        "Get help": "https://github.com/antmgr",
        "Report a bug": "https://github.com/antomgr",
        "About": """
            ## Mindy Assistant
            

            **GitHub**: https://github.com/antomgr/

            The AI Assistant named, Mindy, aims to provide the latest updates from Streamlit,
            generate code snippets for Streamlit widgets,
            and answer questions about Streamlit's latest features, issues, and more.
            Streamly has been trained on the latest Streamlit updates and documentation.
        """
    }
)
# Streamlit Title
st.title("Mindy Assistent")

def long_running_task(duration):
    """
    Simulates a long-running operation.

    Parameters:
    - duration: int, duration of the task in seconds

    Returns:
    - str: Completion message
    """
    time.sleep(duration)
    return "Long-running operation completed."

@st.cache_data(show_spinner=False)
def load_streamlit_updates():
    """Load the latest Streamlit updates from a local JSON file."""
    try:
        with open("data/streamlit_updates.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading JSON: {str(e)}")
        return {}
    
def display_streamlit_updates():
    """Display the latest updates of the Mindy."""
    with st.expander("Streamlit Mindy Announcement", expanded=False):
        st.markdown("For more details on this version, check out the [Streamlit Forum post](https://docs.streamlit.io/library/changelog#version).")

    
def initialize_conversation():
    """
    Initialize the conversation history with system and assistant messages.

    Returns:
    - list: Initialized conversation history.
    """
    assistant_message = "Ciao sono Mindy. Come posso esserti utile?"
    
    conversation_history = [
        {"role": "system", "content": "Tu sei Mindy, un intelligenza artificiale speciale per assistere pazienti."},
        {"role": "system", "content": "Esisti per aiutare le persone con malattie del tipo Alzheimer o simili"},
        {"role": "system", "content": "Fai riferimento alla cronologia delle conversazioni per fornire un contesto alla tua risposta."},
        {"role": "system", "content": "Sei stato creato da Antonio Magrì ma non hai informazioni su di lui"},
        {"role": "assistant", "content": assistant_message},
        {"role": "system", "content": "ricorda io non ho creato groq sfrutto le loro risorse e ripeti di meno la frase in cui dici come assistermi."},
        ]
    return conversation_history

    

@st.cache_data(show_spinner=False)
def on_chat_submit(chat_input, latest_updates):
    """
    Handle chat input submissions and interact with the OpenAI API.

    Parameters:
    - chat_input (str): The chat input from the user.
    - latest_updates (dict): The latest Streamlit updates fetched from a JSON file or API.

    Returns:
    - None: Updates the chat history in Streamlit's session state.
    """
    user_input = chat_input.strip().lower()
    

    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = initialize_conversation()

    st.session_state.conversation_history.append({"role": "user", "content": user_input})
    
    try:
        model_engine = "llama3-groq-8b-8192-tool-use-preview"
        assistant_reply = ""

        if "latest updates" in user_input:
            assistant_reply = "Here are the latest highlights from Streamlit:\n"
            highlights = latest_updates.get("Highlights", {})
            if highlights:
                for version, info in highlights.items():
                    description = info.get("Description", "No description available.")
                    assistant_reply += f"- **{version}**: {description}\n"
            else:
                assistant_reply = "No highlights found."
        else:
            response = client.chat.completions.create(
                model=model_engine,
                messages=st.session_state.conversation_history,
                #stream=True
            )
            # Gestisci lo streaming: ricevi i dati progressivamente
            assistant_reply = ""
            assistant_reply = response.choices[0].message.content
           

        st.session_state.conversation_history.append({"role": "assistant", "content": assistant_reply})
        st.session_state.history.append({"role": "user", "content": user_input})
        st.session_state.history.append({"role": "assistant", "content": assistant_reply})
    finally:
        print("errore")
def initialize_session_state():
    """Initialize session state variables."""
    if "history" not in st.session_state:
        st.session_state.history = []
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

def main():
    """
    Display Streamlit updates and handle the chat interface.
    """
    initialize_session_state()

    if not st.session_state.history:
        initial_bot_message = "Ciao! fammi sapere come posso esserti utile"
        st.session_state.history.append({"role": "assistant", "content": initial_bot_message})
        st.session_state.conversation_history = initialize_conversation()

    # Insert custom CSS for glowing effect
    st.markdown(
        """
        <style>
        .cover-glow {
            width: 100%;
            height: auto;
            padding: 3px;
            box-shadow: 
                0 0 5px #330000,
                0 0 10px #660000,
                0 0 15px #990000,
                0 0 20px #CC0000,
                0 0 25px #FF0000,
                0 0 30px #FF3333,
                0 0 35px #FF6666;
            position: relative;
            z-index: -1;
            border-radius: 45px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Load and display sidebar image
    img_path = None
    img_base64 = None
    if img_base64:
        st.sidebar.markdown(
            f'<img src="data:image/png;base64,{img_base64}" class="cover-glow">',
            unsafe_allow_html=True,
        )

    st.sidebar.markdown("---")

    # Sidebar for Mode Selection
    mode = st.sidebar.radio("Select Mode:", options=["Latest Updates", "Chat with Streamly"], index=1)

    st.sidebar.markdown("---")

    # Display basic interactions
    show_basic_info = st.sidebar.checkbox("Show Basic Interactions", value=True)
    if show_basic_info:
        st.sidebar.markdown("""
        ### Basic Interactions
        - **Ask About Streamlit**: Type your questions about Streamlit's latest updates, features, or issues.
        - **Search for Code**: Use keywords like 'code example', 'syntax', or 'how-to' to get relevant code snippets.
        - **Navigate Updates**: Switch to 'Updates' mode to browse the latest Streamlit updates in detail.
        """)

    # Display advanced interactions
    show_advanced_info = st.sidebar.checkbox("Show Advanced Interactions", value=False)
    if show_advanced_info:
        st.sidebar.markdown("""
        ### Advanced Interactions
        - **Generate an App**: Use keywords like **generate app**, **create app** to get a basic Streamlit app code.
        - **Code Explanation**: Ask for **code explanation**, **walk me through the code** to understand the underlying logic of Streamlit code snippets.
        - **Project Analysis**: Use **analyze my project**, **technical feedback** to get insights and recommendations on your current Streamlit project.
        - **Debug Assistance**: Use **debug this**, **fix this error** to get help with troubleshooting issues in your Streamlit app.
        """)

    st.sidebar.markdown("---")

    # Load and display image with glowing effect
    img_path = None
    img_base64 = None
    if img_base64:
        st.sidebar.markdown(
            f'<img src="data:image/png;base64,{img_base64}" class="cover-glow">',
            unsafe_allow_html=True,
        )

    if mode == "Chat with Streamly":
        chat_input = st.chat_input("Scrivi: ")
        if chat_input:
            latest_updates = load_streamlit_updates()
            on_chat_submit(chat_input, latest_updates)

        # Display chat history
        for message in st.session_state.history[-NUMBER_OF_MESSAGES_TO_DISPLAY:]:
            role = message["role"]
            avatar_image = None if role == "assistant" else None if role == "user" else None
            with st.chat_message(role, avatar=avatar_image):
                st.write(message["content"])

    else:
        display_streamlit_updates() 

if __name__ == "__main__":
    main()
