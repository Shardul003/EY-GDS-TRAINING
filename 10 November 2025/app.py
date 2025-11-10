import streamlit as st
import requests

st.title("Multi-Task Assistant")

task = st.selectbox("Choose a task:", ["Arithmetic", "Date", "Reverse", "AI"])

if task == "Arithmetic":
    num1 = st.number_input("Enter first number:")
    num2 = st.number_input("Enter second number:")
    operation = st.selectbox("Operation:", ["Add", "Subtract", "Multiply", "Divide"])
elif task == "Reverse":
    query = st.text_input("Enter word to reverse:")
elif task == "AI":
    query = st.text_input("Enter your query:")
else:
    query = None

if st.button("Submit"):
    payload = {"task": task}
    if task == "Arithmetic":
        payload.update({"num1": num1, "num2": num2, "operation": operation})
    else:
        payload.update({"query": query})

    try:
        response = requests.post("http://127.0.0.1:8000/process", json=payload)
        if response.status_code == 200:
            st.success(response.json()["answer"])
        else:
            st.error(f"Error: {response.text}")
    except Exception as e:
        st.error(f"Connection error: {e}")