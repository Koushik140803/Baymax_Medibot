import streamlit as st
import requests

# Initialize session state for colors
if "colors_saved" not in st.session_state:
    st.session_state["colors_saved"] = False
    st.session_state["background_color"] = "#F0F8FF"
    st.session_state["user_message_color"] = "#0d6efd"
    st.session_state["baymax_message_color"] = "#FF6347"

# Set up the title and description of the app
st.title("Baymax AI Healthcare Chatbot")
st.subheader("Ask your healthcare-related questions, and Baymax will assist you!")

# Sidebar for setting the appearance (only when not saved)
if not st.session_state["colors_saved"]:
    st.sidebar.header("Chat Settings")
    background_color = st.sidebar.color_picker("Choose Chat Background Color", "#F0F8FF")
    user_message_color = st.sidebar.color_picker("Choose Your Message Color", "#0d6efd")
    baymax_message_color = st.sidebar.color_picker("Choose Baymax Message Color", "#FF6347")
    if st.sidebar.button("Save Colors"):
        st.session_state["background_color"] = background_color
        st.session_state["user_message_color"] = user_message_color
        st.session_state["baymax_message_color"] = baymax_message_color
        st.session_state["colors_saved"] = True
else:
    st.sidebar.success("Colors saved! Reload the app to reset.")

# Set background color
st.markdown(
    f"""
    <style>
    body {{
        background-color: {st.session_state['background_color']};
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Display Baymax image
st.image("baymax_image.jpg", width=400, caption="Baymax AI Healthcare Companion")  # Replace 'baymax_image.png' with your image file

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Function to display the chat history
def display_chat(messages):
    for message in messages:
        if message["role"] == "user":
            st.markdown(
                f'<div style="background-color:{st.session_state["user_message_color"]};'
                f'padding:10px;border-radius:10px;margin-bottom:10px;width:max-content;">{message["text"]}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div style="background-color:{st.session_state["baymax_message_color"]};'
                f'padding:10px;border-radius:10px;margin-bottom:10px;width:max-content;">{message["text"]}</div>',
                unsafe_allow_html=True,
            )

# Get user input (query)
user_query = st.text_input("Please ask a healthcare-related question:")

# Backend API URL (adjust if necessary)
API_URL = "http://localhost:8000/query/"

# Handle the query input
if user_query:
    # Display the user message in the chat
    st.session_state["messages"].append({"role": "user", "text": user_query})

    # Prepare the payload for the request
    payload = {
        "query": user_query,
        "top_k": 5,
    }

    # Send a POST request to the FastAPI backend
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()  # Raise an exception for non-2xx status codes

        # Parse the response
        data = response.json()
        answer = data.get("response", "Sorry, I couldn't get the answer.")
        context = data.get("context", "No relevant context found.")

        # Display the Baymax message in the chat
        st.session_state["messages"].append({"role": "baymax", "text": answer})

    except requests.exceptions.RequestException as e:
        st.error(f"Error contacting the backend: {e}")

# Display chat history after the message is submitted
display_chat(st.session_state["messages"])
