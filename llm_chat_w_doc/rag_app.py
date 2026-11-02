import streamlit as st
import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

st.set_page_config(page_title="Qwen 14B Local RAG", layout="wide")
st.title("🤖 Advanced Local RAG with Qwen 2.5 14B")

# Initialize isolated system memories
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar panel handling files and global cleanups
with st.sidebar:
    st.header("1. Document Management")
    uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])
    
    if uploaded_file:
        if st.button("Process Document", type="primary"):
            with st.spinner("Shredding and vectorizing document locally..."):
                try:
                    # Streamlit handles files in RAM, write bytes temporarily to read via PyPDFLoader
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name

                    # Ingest text segments
                    loader = PyPDFLoader(tmp_path)
                    docs = loader.load()
                    
                    # Optimized chunking boundaries for large reasoning models like Qwen 14B
                    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2500, chunk_overlap=300)
                    splits = text_splitter.split_documents(docs)
                    
                    # Generate local vector fingerprints
                    embeddings = OllamaEmbeddings(model="nomic-embed-text")
                    
                    # Store vector maps securely within session memory space
                    st.session_state.vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
                    
                    os.unlink(tmp_path)  # File cleanup
                    st.success("Document fully processed and indexed!")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    
    st.divider()
    st.header("2. Reset Application")
    if st.button("Clear App & Load New File", type="secondary"):
        st.session_state.vectorstore = None
        st.session_state.chat_history = []
        st.rerun()

# Main Interactive UI Screen 
if st.session_state.vectorstore is not None:
    st.subheader("Chat with your Document")
    
    # Render persistent conversation arrays
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    # Interactive chat input bar
    if user_query := st.chat_input("Ask something about your document..."):
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.write(user_query)
            
        with st.chat_message("assistant"):
            try:
                # Top 5 context fragments passed directly to Qwen 14B
                retriever = st.session_state.vectorstore.as_retriever(search_kwargs={"k": 5})
                llm = ChatOllama(model="qwen2.5-coder:14b", temperature=0)
                
                # Fetch relevant chunks beforehand to construct the streaming loop manually
                retrieved_docs = retriever.invoke(user_query)
                context_str = "\n\n".join([doc.page_content for doc in retrieved_docs])
                
                system_prompt = (
                    "You are an assistant for question-answering tasks. "
                    "Use the following pieces of retrieved context to answer the question. "
                    "If you don't know the answer, say that you don't know.\n\n"
                    "Context:\n{context}"
                )
                prompt_template = ChatPromptTemplate.from_messages([
                    ("system", system_prompt),
                    ("human", "{input}"),
                ])
                
                formatted_prompt = prompt_template.format_messages(
                    context=context_str, 
                    input=user_query
                )
                
                # Stream the output live to the screen
                def response_generator():
                    for chunk in llm.stream(formatted_prompt):
                        yield chunk.content

                answer = st.write_stream(response_generator())
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
                
            except Exception as e:
                st.error(f"Error generating response: {e}")
else:
    st.info("👈 Please upload a PDF file and click 'Process Document' in the sidebar to get started.")

