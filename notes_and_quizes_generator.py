import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
import PyPDF2
from io import BytesIO
import os


# Set up the LLMs with OpenRouter models
try:
    api_key = st.secrets["OPENROUTER_API_KEY"]

    llm1 = ChatOpenAI(
        model="mistralai/mixtral-8x7b-instruct",
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        max_tokens=512,
        temperature=0.0,
    )



    llm2 = ChatOpenAI(
        model="mistralai/mistral-7b-instruct",  
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        max_tokens=512,
        temperature=0.0,
    )
except Exception as e:
    st.error(f"Failed to initialize LLMs: {str(e)}")
    st.stop()

# Define prompts
prompt1_notes = PromptTemplate(
    template="Provide detailed notes about the following topic: {topic}",
    input_variables=["topic"]
)

prompt2_quiz = PromptTemplate(
    template="Create a detailed quiz about the following topic: {topic}",
    input_variables=["topic"]
)

prompt3_merge = PromptTemplate(
    template="Merge the following notes --> {notes} and quizzes --> {quizes} into a single document",
    input_variables=["notes", "quizes"]
)

# Parser
parser = StrOutputParser()

# Chains
chain1 = prompt1_notes | llm1 | parser
chain2 = prompt2_quiz | llm2 | parser

parallel_chain = RunnableParallel({
    "notes": chain1,
    "quizes": chain2
})

merge_chain = prompt3_merge | llm1 | parser
chain = parallel_chain | merge_chain

# Streamlit app
st.title("PDF Notes and Quiz Generator (OpenRouter)")

uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

if uploaded_file is not None:
    try:
        # Extract text from PDF
        pdf_reader = PyPDF2.PdfReader(BytesIO(uploaded_file.read()))
        text = ""
        for page in pdf_reader.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"
        
        if text.strip():
            st.subheader("Extracted Text from PDF")
            st.text_area("Text", text, height=200)
            
            if st.button("Generate Notes and Quiz"):
                with st.spinner("Generating notes and quiz..."):
                    try:
                        # Chunk text to avoid exceeding token limits
                        def chunk_text(text, max_length=500):
                            words = text.split()
                            chunks = []
                            current_chunk = []
                            current_length = 0
                            for word in words:
                                current_length += len(word) + 1
                                if current_length > max_length:
                                    chunks.append(" ".join(current_chunk))
                                    current_chunk = [word]
                                    current_length = len(word) + 1
                                else:
                                    current_chunk.append(word)
                            if current_chunk:
                                chunks.append(" ".join(current_chunk))
                            return chunks

                        chunks = chunk_text(text)
                        all_notes = []
                        all_quizzes = []
                        for chunk in chunks:
                            parallel_result = parallel_chain.invoke({"topic": chunk})
                            all_notes.append(parallel_result["notes"])
                            all_quizzes.append(parallel_result["quizes"])
                        notes = "\n\n".join(all_notes)
                        quizzes = "\n\n".join(all_quizzes)
                        merged_result = merge_chain.invoke({"notes": notes, "quizes": quizzes})
                        
                        # Display notes
                        st.subheader("Generated Notes")
                        st.text_area("Notes", notes, height=200)
                        
                        # Display quizzes
                        st.subheader("Generated Quizzes")
                        st.text_area("Quizzes", quizzes, height=200)
                        
                        # Display merged document
                        st.subheader("Overview")
                        st.text_area("Merged Notes and Quizzes", merged_result, height=400)
                    except Exception as e:
                        st.error(f"Error generating notes and quiz: {str(e)}")
        else:
            st.warning("No text extracted from the PDF. Please upload a valid PDF.")
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
else:
    st.info("Please upload a PDF file to proceed.")