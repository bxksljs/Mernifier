import streamlit as st
import google.generativeai as palm

# Configure the palm API
palm.configure(api_key="AIzaSyC5iqIChPW9mKJmexmtDbrmjj7_AjBbAYw")

# Load the pre-trained AI model
model_id = "models/chat-bison-001"

# Define the prompt
prompt = "I am an AI-powered MERN Assistant."

# Define the examples


# Create a Streamlit app
st.title("MERN-GPT")

# Display the prompt
st.write(prompt)

# Get the user's input
user_input = st.text_input("How can I help you")

# Check if the user's input is empty
if not user_input:
  st.error("message must include non empty content")
  exit()

# Generate a response from the palm model
response = palm.chat(messages=user_input, temperature=0.2, context="Speak like you have to answer the doubts user has related to MERN stack")

# Display the response to the user
st.write(response.last)

# Ask the user if they have any other doubts
st.write("Do you have any other doubts?")
ask_for_other_doubts_button = st.button("Yes")

# Define the function to ask the user for other doubts
def ask_for_other_doubts():
  user_input = st.text_input("What is your doubt?")

# Check if the user's input is empty
if not user_input:
   st.error("message must include non empty content")
   exit()

response = palm.chat(messages=user_input, temperature=0.2, context="Speak like you have to answer the doubts user has related to MERN stack")
st.write(response.last)

# If the user clicks the button, ask them for their doubt
if ask_for_other_doubts_button:
  ask_for_other_doubts()
