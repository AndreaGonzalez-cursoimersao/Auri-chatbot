import streamlit as st
import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

st.title("🤖 Assistente Virtual - TechExpress")
st.write("Pergunte sobre trocas, privacidade, descontos e prazos!")

@st.cache_resource
def inicializar_banco_dados():
    if not os.path.exists("documentos") or not os.listdir("documentos"):
        st.error("A pasta 'documentos' está vazia. Execute o script 'gerar_pdfs.py' primeiro!")
        return None
        
    loader = PyPDFDirectoryLoader("documentos/")
    docs = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
    chunks = text_splitter.split_documents(docs)
    
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectorstore = Chroma.from_documents(chunks, embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 2})

if OPENAI_API_KEY:
    retriever = inicializar_banco_dados()
    
    if retriever:
        llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=OPENAI_API_KEY, temperature=0.2)

        system_prompt = (
            "Você é um atendente virtual muito educado da loja online TechExpress.\n"
            "Use estritamente os fragmentos de contexto extraídos dos PDFs da loja para responder.\n"
            "Se você não souber a resposta ou ela não estiver nos arquivos, responda exatamente: "
            "'Desculpe, não tenho essa informação nos meus manuais. Por favor, aguarde um atendente humano.'\n\n"
            "CONTEXTO EXTRAÍDO DOS PDFS:\n"
            "{context}"
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])

        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if user_input := st.chat_input("Como posso ajudar você hoje?"):
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("assistant"):
                response = rag_chain.invoke({"input": user_input})
                answer = response["answer"]
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
else:
    st.error("Por favor, configure a variável de ambiente OPENAI_API_KEY para ativar o robô.")
