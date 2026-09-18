import streamlit as st

st.title("MY History ChatBot")
st.caption("A built-in contextual assistant for learning the history of Nepal.")
st.info(
    """
    **Welcome to MY History ChatBot!** This intelligent assistant is designed to explore the rich heritage of Nepal. 
    It reads your active conversation history to maintain context, allowing you to ask follow-up questions naturally.
    """
)

if "messages" not in st.session_state:
    st.session_state.messages = []
    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
      
prompt = st.chat_input("Say something")
if prompt:
    with st.chat_message("user"):
        st.write(f"{prompt}")
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        response="hi i am bot"
        st.write(f"{response}")
    st.session_state.messages.append({"role": "assistant", "content": response})
        

    
    
    
    