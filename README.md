# 🤖 Assistente Virtual de Atendimento com IA e Leitura de PDFs (RAG)

Este projeto consiste em um chatbot inteligente para e-commerce da AURI (fictícia) capaz de responder a dúvidas frequentes, políticas de trocas, cupons de desconto e privacidade com base em documentos PDF oficiais da loja. 

O sistema foi desenvolvido utilizando **Python** e uma arquitetura simplificada de **RAG (Retrieval-Augmented Generation)** de alta performance, garantindo respostas precisas e alinhadas estritamente com os manuais fornecidos.

---

## 🛠️ Tecnologias e Arquitetura Utilizadas

- **Linguagem Principal:** Python 3.14
- **Interface de Usuário:** `Streamlit` para a criação de uma aplicação web de chat fluida, interativa e responsiva.
- **Provedor de Incerência (IA):** `Groq Cloud` – Utilizado para obter respostas em frações de segundo com altíssimo desempenho e custo zero.
- **Modelo de Linguagem (LLM):** `qwen/qwen3.6-27b` via Groq.
- **Orquestração de Prompt:** `LangChain Core` para a estruturação de templates de prompts sistêmicos e tratamento de histórico.
- **Processamento de PDFs:** `PyPDF` (`PdfReader`) para varredura e extração de texto nativa diretamente dos arquivos físicos.
- **Hospedagem em Nuvem:** `Streamlit Community Cloud` integrado ao controle de versão via `GitHub`. https://auri-chatbot-ysxjzqk8zcrykknq2gbwup.streamlit.app/

---

## 📋 Estrutura de Arquivos do Projeto

```text
meu-chatbot/
│
├── documentos/          # Pasta com os arquivos PDF lidos pela IA
│   ├── trocas.pdf
│   ├── privacidade.pdf
│   └── faq.pdf
│
├── app.py               # Código principal do robô e interface do chat
├── gerar_pdfs.py        # Script utilitário para automação dos documentos base
├── requirements.txt     # Gerenciador de dependências do servidor
└── README.md            # Documentação técnica do projeto
```

