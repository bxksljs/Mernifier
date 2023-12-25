import streamlit as st
import google.generativeai as palm

# Configure the palm API
palm.configure(api_key="AIzaSyC5iqIChPW9mKJmexmtDbrmjj7_AjBbAYw")

# Load the pre-trained AI model
model_id = "models/chat-bison-001"

# Define the prompt with a focus on RESTful API assistance
prompt = "I am an AI-powered Node.js assistant for RESTful API development using Express.js. Ask me for suggestions, code snippets, routing, middleware, error handling, database interactions, security, input validation, and authentication."

# Create a Streamlit app
st.title("AI-powered Node.js RESTful API Assistant")

# Display the prompt
st.write(prompt)

# Get the user's input
user_input = st.text_input("How can I help you with your Node.js RESTful API development?")

# Check if the user's input is empty
if not user_input:
    st.error("Please provide a query or request for assistance.")
    exit()

# Generate a response from the palm model, emphasizing Node.js, Express.js, and RESTful API context
response = palm.chat(
    messages=user_input,
    temperature=0.2,
    context="Provide Node.js code suggestions and snippets for RESTful API development using Express.js, including routing, middleware, error handling, database interactions, security, input validation, and authentication."
)

# Display the response to the user
st.write(response.last)
