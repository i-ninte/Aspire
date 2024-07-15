import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.llms import HuggingFaceHub
from langchain.chains import LLMChain

# Define the prompt template
template = """Question: {question}
Answer: Hello I am AspireBot. Here to help you with all the questions."""
prompt = PromptTemplate(template=template, input_variables=["question"])

# Initialize the LLM from Hugging Face
def initialize_llm(api_key):
    return HuggingFaceHub(huggingfacehub_api_token=api_key, repo_id="mistralai/Mistral-7B-Instruct-v0.3")

# Initialize the LLMChain
def initialize_chain(api_key):
    llm = initialize_llm(api_key)
    return LLMChain(llm=llm, prompt=prompt)

# Function to query the LangChain model
def query_langchain(question, api_key):
    llm_chain = initialize_chain(api_key)
    response = llm_chain({"question": question})
    return response["text"]

def main():
    # Set up the app title and header
    st.set_page_config(page_title="Chatbot", page_icon=":robot_face:")
    st.markdown("<h1 style='text-align: center; color: #4c7ef3;'>AspireBot</h1>", unsafe_allow_html=True)

    # Initialize conversation history in the session state
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []

    # Define function to add message to conversation
    def add_message(is_bot, message):
        st.session_state.conversation.append({"is_bot": is_bot, "message": message})

    # Create input field for user
    user_input = st.text_input("Type a new message here", key="user_input", placeholder="Enter your message...", label_visibility="collapsed")

    # If user enters a message, add it to the conversation and get a response from the model
    if user_input:
        add_message(is_bot=False, message=user_input)

        # Display the user's message
        st.markdown(f"<div style='background-color: #f2f2f2; padding: 10px; border-radius: 10px; display: flex; align-items: center;'><img src='https://img.icons8.com/color/48/000000/user-male-circle.png' style='width: 32px; height: 32px; margin-right: 10px;'><p style='color: #333333; font-weight: bold; margin: 0;'>{user_input}</p></div>", unsafe_allow_html=True)

        # Query the LangChain model
        api_key = st.secrets["HF_TOKEN"]
        try:
            bot_response = query_langchain(user_input, api_key)
        except Exception as err:
            bot_response = f"Error occurred: {err}"

        # Add the bot response to the conversation
        add_message(is_bot=True, message=bot_response)

        # Display the bot's message
        st.markdown(f"<div style='background-color: #e6f7ff; padding: 10px; border-radius: 10px; display: flex; align-items: center;'><img src='https://img.icons8.com/color/48/000000/robot-2.png' style='width: 32px; height: 32px; margin-right: 10px;'><p style='color: #4c7ef3; font-weight: bold; margin: 0;'>{bot_response}</p></div>", unsafe_allow_html=True)

    # Display conversation history
    for message in st.session_state.conversation:
        if message["is_bot"]:
            st.markdown(f"<div style='background-color: #e6f7ff; padding: 10px; border-radius: 10px; display: flex; align-items: center;'><img src='https://img.icons8.com/color/48/000000/robot-2.png' style='width: 32px; height: 32px; margin-right: 10px;'><p style='color: #4c7ef3; font-weight: bold; margin: 0;'>{message['message']}</p></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background-color: #f2f2f2; padding: 10px; border-radius: 10px; display: flex; align-items: center;'><img src='https://img.icons8.com/color/48/000000/user-male-circle.png' style='width: 32px; height: 32px; margin-right: 10px;'><p style='color: #333333; font-weight: bold; margin: 0;'>{message['message']}</p></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
