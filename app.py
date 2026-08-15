import streamlit as st
import os
from pypdf import PdfReader
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Pega a chave da OpenAI que você salvou nos Segredos
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

st.title("🤖 Assistente Virtual - TechExpress")
st.write("Pergunte sobre trocas, privacidade, descontos e prazos!")

# 2. Função simples para ler o texto de todos os PDFs da pasta de documentos
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

# Carrega as políticas dos arquivos de verdade que estão no seu GitHub
CONTEXTO_DOS_PDFS = ler_textos_dos_pdfs()

if OPENAI_API_KEY:
    # Configura a Inteligência Artificial
    llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=OPENAI_API_KEY, temperature=0.2)

    # Cria o comando mandando o texto extraído dos PDFs como contexto real
    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "Você é um atendente virtual prestativo da loja online TechExpress.\n"
            "Responda às dúvidas dos clientes usando APENAS as informações do contexto abaixo, que foram extraídas dos nossos PDFs oficiais.\n"
            "Se o cliente perguntar algo que não está no contexto, diga educadamente que não tem essa informação "
            "e peça para ele aguardar um atendente humano.\n\n"
            "CONTEXTO EXTRAÍDO DOS PDFS DA LOJA:\n"
            f"{CONTEXTO_DOS_PDFS}"
        )),
        ("placeholder", "{messages}"),
    ])

    chain = prompt | llm | StrOutputParser()

    # Histórico de conversas na tela
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada de texto do usuário
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
    st.error("Por favor, configure a variável OPENAI_API_KEY nas configurações do Streamlit.")
