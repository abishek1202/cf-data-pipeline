import streamlit as st
from chatbot import retrieve_data, ask_llm

st.title("🤖 Supply Chain AI Assistant")

query = st.text_input("Ask your data:")

if query:
    results = retrieve_data(query)
    context = "\n".join(results)

    answer = ask_llm(query, context)

    st.subheader("✅ Answer")
    st.write(answer)