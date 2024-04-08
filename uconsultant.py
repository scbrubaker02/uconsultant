

import streamlit as st
from agent import get_invoke_fn

def just_st():
    st.title("UConsultant Bot")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "response_fn" not in st.session_state:
        st.session_state.response_fn = get_invoke_fn()

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if usr_msg := st.chat_input("Describe your learning goals for your self or your team."):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(usr_msg)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": usr_msg})

        response = st.session_state.response_fn(usr_msg)['output']
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

def main():
    just_st()

if __name__ == "__main__":
    main()