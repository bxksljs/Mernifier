import streamlit as st
import google.generativeai as palm

# Configure the palm API (replace with your actual API key)
palm.configure(api_key="AIzaSyC5iqIChPW9mKJmexmtDbrmjj7_AjBbAYw")

# Load the pre-trained AI model
model_id = "models/chat-bison-001"

# Create a Streamlit app
st.title("React Code Updater")

# Prompt the user to enter React code
react_code = st.text_area("Enter your React code:")

# Add buttons for updating components and fixing bugs
update_button = st.button("Update Component", key="update_button")
fix_bugs_button = st.button("Fix Bugs", key="fix_bugs_button")

# Style the buttons to make them green
button_style = """
    <style>
        div[data-testid="stButton"] button {
            background-color: #4CAF50;
            color: white;
        }
    </style>
"""

st.markdown(button_style, unsafe_allow_html=True)

if update_button:
    # Generate code to update the component using palm API
    prompt = f"Update the React component based on the following code:\n{react_code}"
    response = palm.chat(messages=prompt, temperature=0.2, context=model_id)
    updated_code = response.last
    st.write("Updated code:", updated_code)

elif fix_bugs_button:
    # Generate code to fix bugs and errors using palm API
    prompt = f"Fix bugs and errors in the following React code:\n{react_code}"
    response = palm.chat(messages=prompt, temperature=0.2, context=model_id)
    fixed_code = response.last
    st.write("Fixed code:", fixed_code)
