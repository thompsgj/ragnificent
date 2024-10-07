import streamlit as st
import requests
import uuid
import os

API_HOST = os.environ.get("API_HOST", "localhost")

st.title("Rag-nificent Styles")

# Initialize chat history
if "response" not in st.session_state:
    st.session_state.response = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_rating" not in st.session_state:
    st.session_state.user_rating = None
    st.session_state.feedback_key = str(uuid.uuid4())
    st.session_state.query_id = None


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What style-related question can I help you with?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = requests.post(
            url=f"http://{API_HOST}:7860/queries",
            json={"query": prompt},
        ).json()

        answer = response["answer"]
        st.session_state.query_id = response.get("query_id", 1)

        st.write(answer)
        st.session_state.response = answer
    st.session_state.messages.append({"role": "assistant", "content": answer})


if st.session_state.response:
    st.session_state.user_rating = None
    rating = st.feedback("faces", key=st.session_state.feedback_key)
    if rating is not None:
        if rating >= 0:
            requests.post(
                url=f"http://{API_HOST}:7860/queries/{st.session_state.query_id}/feedback",
                json={"rating": rating},
            ).json()
            st.session_state.response = None
            st.session_state.user_rating = rating
            st.session_state.feedback_key = str(uuid.uuid4())
            st.rerun()
