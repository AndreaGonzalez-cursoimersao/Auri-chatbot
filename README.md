# 🤖 Assistente Virtual de Atendimento - Auri

## 📋 Descrição Geral do Projeto
Este projeto consiste no desenvolvimento de um chatbot inteligente de atendimento para a loja virtual fictícia "Auri". 
O objetivo principal é automatizar o suporte ao cliente em tópicos recorrentes e burocráticos, como políticas de trocas e devoluções, diretrizes de privacidade, segurança de dados, prazos de entrega e aplicação de cupons de descontos. 

O diferencial do sistema é que ele utiliza a técnica de **RAG (Retrieval-Augmented Generation)**. 
Isso significa que a inteligência artificial não inventa respostas; ela lê arquivos PDF reais fornecidos pela loja e responde ao cliente baseando-se estritamente nesses manuais. Caso a dúvida não esteja nos documentos, o robô direciona o atendimento de forma educada para um atendente humano.

---

## 🏛️ Arquitetura da Solução Implementada
A arquitetura do chatbot foi desenhada para ser leve, estável e imune a conflitos de versões no servidor. O fluxo funciona da seguinte forma:

1. **Camada de Dados (Ingestão):** Os documentos com as regras da loja são armazenados fisicamente em formato PDF dentro da pasta `/documentos`.
2. **Processamento e Extração:** Ao inicializar a aplicação, o sistema utiliza um leitor nativo de PDF para extrair todo o conteúdo de texto dos arquivos e unificá-lo na memória do servidor.
3. **Injeção de Contexto (Pipeline RAG):** Esse bloco de texto unificado é injetado diretamente no prompt sistêmico da inteligência artificial, servindo como o "manual de regras" absoluto do robô.
4. **Camada de Inteligência (LLM):** Através de uma conexão segura via API, as perguntas dos usuários e o contexto dos PDFs são enviados para o motor de inferência da nuvem, que processa a informação e gera a resposta ideal.
5. **Interface de Usuário (UI):** Uma aplicação web moderna gerencia o histórico de mensagens e exibe o chat de forma fluida para o cliente final.

---

## 🛠️ Tecnologias e Ferramentas Utilizadas
- **Linguagem de Programação:** Python 3.14
- **Interface Gráfica (Frontend):** `Streamlit` para a criação da página web e componentes visuais do chat.
- **Processamento de Documentos:** `PyPDF` (`PdfReader`) para a leitura nativa e extração de strings dos arquivos PDF.
- **Orquestração de Prompt:** `LangChain Core` para a estruturação das mensagens e manutenção do histórico da conversa.
- **Provedor de IA (LLM):** `Groq Cloud` operando o modelo de última geração `qwen/qwen3.6-27b`, garantindo respostas em milissegundos sem custos de infraestrutura.
- **Controle de Versão:** `Git` e `GitHub`.
- **Hospedagem em Nuvem:** `Streamlit Community Cloud`.
  https://auri-chatbot-ysxjzqk8zcrykknq2gbwup.streamlit.app/

---

## 📋 Estrutura de Arquivos do Projeto

```text
meu-chatbot/
│
├── documentos/          # Pasta com os arquivos PDF oficiais lidos pela IA
│   ├── trocas.pdf
│   ├── privacidade.pdf
│   └── faq.pdf
│
├── app.py               # Código principal do robô e interface do chat
├── gerar_pdfs.py        # Script utilitário para automação dos documentos base
├── requirements.txt     # Gerenciador de dependências do servidor
└── README.md            # Documentação técnica do projeto

```

## 🚀 Instruções para Executar o Projeto

### Execução na Nuvem (Pronto para Uso)
O projeto já se encontra implantado e disponível publicamente para testes através do link fornecido na entrega deste trabalho. (https://auri-chatbot-ysxjzqk8zcrykknq2gbwup.streamlit.app/)

### Execução em Ambiente Local (Opcional)
Caso queira rodar o projeto em seu computador, siga os passos abaixo:

1. **Instale as dependências:**
   ```bash
   pip install streamlit pypdf langchain-groq langchain-core
   ```
2. **Gere os arquivos PDF base da loja:**
   ```bash
   python gerar_pdfs.py
   ```
3. **Configure as credenciais:**
   Crie um arquivo chamado `.env` na raiz do projeto e insira sua chave da Groq:
   ```text
   GROQ_API_KEY="sua_chave_gsk_aqui"
   ```
4. **Inicie o servidor local:**
   ```bash
   streamlit run app.py
   ```

---

## ❓ Exemplos de Perguntas que o Agente Consegue Responder
Graças à leitura dos PDFs anexados, o agente está apto a responder perguntas como:
* *Como faço para devolver um produto que comprei por arrependimento?*
* *Vocês guardam os dados do meu cartão de crédito no sistema?*
* *Qual é o prazo médio de entrega para o interior e para capitais?*
* *Existe algum cupom de desconto para quem está comprando pela primeira vez?*
* *Posso pagar com PIX? Tem algum benefício?*

---

## 💬 Exemplos de Respostas Geradas pelo Agente

### Exemplo 1: Dúvida sobre Descontos
- **Usuário:** *Quero comprar pela primeira vez, tem cupom?*
- **Agente 🤖:** *Sim! Para novos clientes, nós temos o cupom **BENVINDO10**, que garante 10% de desconto na sua primeira compra. Atenção: ele é válido apenas para carrinhos com valor total de produtos acima de R$ 100!*

### Exemplo 2: Dúvida sobre Pagamento e Segurança
- **Usuário:** *É seguro pagar com cartão? Vocês salvam meus dados?*
- **Agente 🤖:** *Pode ficar tranquilo! Nossa política de privacidade garante que os dados do seu cartão de crédito são criptografados na ponta e enviados diretamente para a operadora de pagamentos. A nossa loja virtual não armazena nenhuma informação financeira ou de cartões em nossos servidores locais.*

### Exemplo 3: Pergunta fora do escopo (Proteção contra Alucinações)
- **Usuário:** *Vocês vendem ração para cachorro?*
- **Agente 🤖:** *Desculpe, não tenho essa informação nos meus manuais. Por favor, aguarde um atendente humano.*
