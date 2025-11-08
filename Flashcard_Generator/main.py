import streamlit as st

from openai import OpenAI

client = OpenAI(
    api_key="your api key here",
)



def response(model: str, messages: list, string):
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that creates flashcards."},
        {"role": "user", "content": "Create flashcards about " + string}
    ]
)

def create_own_flashcards(): 
    number_of_cards = st.slider("How many flashcards do you want to create?", 1, 25, 1)
    for int in range(number_of_cards): 
        term = st.write(input("Give me a term or question: "))
        answer = st.write(input("Give me the answer or explanation: "))



def main():
    st.title("AI-Flashcard Generator")
    st.write("Make flashcards of your own or learn about a topic")
    st.write("Choose a mode below")
    st.button("Create your own")
    st.button("Make flashcards with AI")
    question = "questions.txt"

    if st.button == "Create your own":
        create_own_flashcards()
    if st.button == "Make flashcards with AI":
    
    






st.caption("Created by Kaysen Acfalle & William Xue")