import streamlit as st
import os
from pypdf import PdfReader
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Pega a chave do Groq salva nas configurações do Streamlit
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

st.title("🤖 Assistente Virtual - TechExpress")
st.write("Pergunte sobre trocas, privacidade, descontos e prazos!")

# 2. Função para ler os textos dos seus PDFs
@st.cache_resource
def ler_textos_dos_pdfs():
    texto_completo = ""
    pasta = "documentos"
    if os.path.exists(pasta):
        for arquivo in os.listdir(pasta):
            if arquivo.endswith(".pdf"):
                caminho = os.path.join(pasta, arquivo)
                try:
                    reader = PdfReader(caminho)
                    for pagina in reader.pages:
                        texto_completo += pagina.extract_text() + "\n"
                except Exception:
                    pass
    return texto_completo

CONTEXTO_DOS_PDFS = ler_textos_dos_pdfs()

if GROQ_API_KEY:
    # Configura o modelo gratuito do Llama via Groq
    llm = ChatGroq(model="llama-3.3-70b-specdec", groq_api_key=GROQ_API_KEY, temperature=0.2)

    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "Você é um atendente virtual prestativo da loja online TechExpress.\n"
            "Responda às dúvidas dos clientes usando APENAS as informações do contexto abaixo, extraídas dos nossos PDFs.\n"
            "Se o cliente perguntar algo que não está no contexto, diga educadamente que não tem essa informação "
            "e peça para ele aguardar um atendente humano.\n\n"
            "CONTEXTO EXTRAÍDO DOS PDFS DA LOJA:\n"
            f"{CONTEXTO_DOS_PDFS}"
        )),
        ("placeholder", "{messages}"),
    ])

    chain = prompt | llm | StrOutputParser()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_input := st.chat_input("Como posso ajudar você hoje?"):
        with st.chat_message("user"):
            st.markdown(user_input)
        
        api_messages = []
        for msg in st.session_state.messages:
            api_messages.append((msg["role"], msg["content"]))
        api_messages.append(("user", user_input))

        with st.chat_message("assistant"):
            response = chain.invoke({"messages": api_messages})
            st.markdown(response)
        
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.error("Por favor, configure a variável GROQ_API_KEY nos segredos do Streamlit.")
