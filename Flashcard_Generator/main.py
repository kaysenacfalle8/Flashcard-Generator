import streamlit as st
import PyPDF2
import docx
from openai import OpenAI

# --- OPENAI CLIENT ---
client = OpenAI(api_key="your added key")

FILE_NAME = "questions.txt"

# --- FILE HANDLING FUNCTIONS ---
def extract_text_from_pdf(uploaded_file):
    """Extracts text from a PDF file."""
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text.strip()


def extract_text_from_docx(uploaded_file):
    """Extracts text from a DOCX file."""
    doc = docx.Document(uploaded_file)
    return "\n".join([p.text for p in doc.paragraphs if p.text]).strip()


# --- OPENAI FLASHCARD RESPONSE ---
def response(model: str, messages: list, text):
    res = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that creates flashcards."},
            {"role": "user", "content": "Create flashcards about " + text}
        ]
    )
    return res.choices[0].message.content


# --- USER CREATES OWN FLASHCARDS ---
def create_own_flashcards():
    num_cards = st.number_input("How many flashcards do you want to create?", min_value=1, step=1)
    flashcards = []

    for i in range(int(num_cards)):
        term = st.text_input(f"Card {i+1} - Enter term/question:", key=f"term_{i}")
        definition = st.text_input(f"Card {i+1} - Enter answer/definition:", key=f"def_{i}")
        if term and definition:
            flashcards.append((term, definition))
    
    if st.button("Save Flashcards"):
        with open(FILE_NAME, "w") as f:
            for term, definition in flashcards:
                f.write(f"{term}:{definition}\n")
        st.success("Flashcards saved successfully!")


# --- AI-GENERATED FLASHCARDS ---
def create_ai_flashcards():
    uploaded_file = st.file_uploader("Upload your notes", type=["pdf", "docx"])
    if uploaded_file:
        if uploaded_file.name.endswith(".pdf"):
            text = extract_text_from_pdf(uploaded_file)
        else:
            text = extract_text_from_docx(uploaded_file)

        if not text:
            st.error("Couldn't read text from the file. Try another format.")
            return

        st.info("Generating flashcards... please wait ⏳")
        ai_response = response("gpt-4o", [], text)
        st.subheader("AI-Generated Flashcards")
        st.write(ai_response)

        if st.button("Save AI Flashcards"):
            with open(FILE_NAME, "w") as f:
                f.write(ai_response)
            st.success(f"AI flashcards saved to {FILE_NAME}!")


# --- MAIN APP ---
def main():
    st.title("AI Flashcard Generator")
    st.write("Make flashcards manually or generate them with AI 🤖")
    mode = st.radio("Choose a mode:", ["Create your own", "AI-generated"])

    if mode == "Create your own":
        create_own_flashcards()
    else:
        create_ai_flashcards()


st.caption("Created by Kaysen Acfalle & William Xue")

if __name__ == "__main__":
    main()
