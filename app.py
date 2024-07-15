import streamlit as st
import requests

# Function to query the Hugging Face model
def query_huggingface(payload, model_id, api_key):
    API_URL = f"https://api-inference.huggingface.co/models/{model_id}"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

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

        # Query the Hugging Face model
        model_id = "mistralai/Mistral-7B-Instruct-v0.3"  
        api_key = st.secrets["HF_TOKEN"]
        data = {"inputs": user_input}
        try:
            output = query_huggingface(data, model_id, api_key)
            if isinstance(output, list) and len(output) > 0 and "generated_text" in output[0]:
                bot_response = output[0]["generated_text"]
            else:
                bot_response = "I am not sure how to respond to that."
        except requests.exceptions.HTTPError as err:
            bot_response = f"HTTP error occurred: {err}"
        except requests.exceptions.RequestException as err:
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
