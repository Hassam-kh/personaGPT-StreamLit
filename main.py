import streamlit as st
import sys
from chatbot import chatting_conv
# response = st.text_input(f">> Define Your Relation With Bot: ")
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.dialog = []
if "page" not in st.session_state:
    st.session_state.page = "Page 1"
    st.session_state.response = ""
if "page" in st.session_state and st.session_state.page == "Page 1":
    st.title("Welcome To PersonaGPT: Nice To Have You Here !!!")
    st.info(">> Enter the facts about the bot (Press Escape or Leave Blank and press Enter to Finish Writing)")
    st.session_state.response = st.text_input(
        f">> Define Your Relation With Bot: ")
    if st.session_state.response:
        st.session_state.page = "Page 2"
if "page" in st.session_state and st.session_state.page == "Page 2":
    st.title("Let's Start Our Conversation")
    st.info(">> Enter the Question to ask the bot (Write exit to end Conversation and press Enter to Finish Writing)")
    transcription = st.text_input(f">> User: ", "")
    if transcription:
        if str(transcription) == "exit":
            st.success("  Good Luck!!")
            st.session_state.page = "Page 3"
            sys.exit(0)
        persona, u, m, user_inp, msg = chatting_conv(
            (st.session_state.response), (transcription), st.session_state.dialog)
        st.text(persona)
        st.session_state.dialog.append(u)
        st.session_state.dialog.append(m)
        st.session_state.messages.append(str(user_inp)[:-13])
        st.session_state.messages.append(">> Bot: "+str(msg)[:-13])
    else:
        st.stop()
    st.sidebar.header("History")
    for message in st.session_state.messages:
        st.sidebar.text(message)
