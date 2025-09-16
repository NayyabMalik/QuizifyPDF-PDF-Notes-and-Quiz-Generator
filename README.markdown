# QuizifyPDF – PDF Notes and Quiz Generator

This Streamlit application generates detailed notes and quizzes from uploaded PDF files using language models from OpenRouter. It extracts text from PDFs, processes it to create notes and quizzes, and merges them into a single document.

## Features
- **PDF Text Extraction**: Extracts text from uploaded PDF files using PyPDF2.
- **Notes and Quiz Generation**: Uses two language models (MistralAI Mixtral-8x7b and Mistral-7b) to generate detailed notes and quizzes based on the extracted text.
- **Text Chunking**: Splits large text into smaller chunks to handle token limits of the language models.
- **Merged Output**: Combines generated notes and quizzes into a single cohesive document.
- **Streamlit Interface**: Provides a user-friendly web interface for uploading PDFs and viewing results.

## Prerequisites
- Python 3.8 or higher
- Streamlit
- PyPDF2
- LangChain with OpenAI integration
- Access to OpenRouter API (requires an API key)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/NayyabMalik/PDF-Notes-and-Quiz-Generator
   cd  PDF-Notes-and-Quiz-Generator
   ```
2. Install the required packages:
   ```bash
   pip install streamlit PyPDF2 langchain langchain-openai
   ```
3. Set up the OpenRouter API key:
   - Create a `.streamlit/secrets.toml` file in the project directory.
   - Add your OpenRouter API key:
     ```toml
     OPENROUTER_API_KEY = "your-api-key-here"
     ```

## Usage
1. Run the Streamlit app:
   ```bash
   streamlit run notes_and_quizes_generator.py
   ```
2. Open the provided URL in your browser (typically `http://localhost:8501`).
3. Upload a PDF file using the file uploader.
4. View the extracted text from the PDF.
5. Click the "Generate Notes and Quiz" button to process the text and display:
   - Generated notes
   - Generated quizzes
   - Merged document combining both

## How It Works
- **PDF Processing**: The app uses PyPDF2 to extract text from uploaded PDFs.
- **Text Chunking**: Large texts are split into smaller chunks (500 characters or less) to comply with model token limits.
- **LLM Chains**:
  - Two language models (`mistralai/mixtral-8x7b-instruct` and `mistralai/mistral-7b-instruct`) generate notes and quizzes, respectively.
  - LangChain's `PromptTemplate` and `RunnableParallel` are used to process the text in parallel.
  - A final merge chain combines the notes and quizzes into a single document.
- **Output**: The app displays the extracted text, generated notes, quizzes, and merged document in separate text areas.

## Dependencies
- `streamlit`: For the web interface
- `PyPDF2`: For PDF text extraction
- `langchain`: For managing prompts and chains
- `langchain_openai`: For interacting with OpenRouter's language models
- `io`: For handling file streams
- `os`: For environment handling

## Notes
- Ensure your PDF contains extractable text (not scanned images).
- The app requires a valid OpenRouter API key stored in `st.secrets`.
- Error handling is implemented to catch issues with PDF processing or LLM calls.
- The models used (`mixtral-8x7b-instruct` and `mistral-7b-instruct`) are configured with a temperature of 0.0 for deterministic outputs and a max token limit of 512.

## Limitations
- The app may struggle with PDFs that contain images or non-extractable text.
- Large PDFs may result in slower processing due to text chunking and multiple LLM calls.
- The quality of notes and quizzes depends on the input PDF content and the language models' capabilities.

## License
This project is licensed under the MIT License.
