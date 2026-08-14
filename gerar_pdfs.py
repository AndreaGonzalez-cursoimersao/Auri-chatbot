import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def criar_pdf(nome_arquivo, titulo, texto_conteudo):
    os.makedirs("documentos", exist_ok=True)
    caminho = os.path.join("documentos", nome_arquivo)
    doc = SimpleDocTemplate(caminho, pagesize=letter)
    story = []
    
    styles = getSampleStyleSheet()
    style_titulo = ParagraphStyle('TituloStyle', parent=styles['Heading1'], spaceAfter=15)
    style_corpo = ParagraphStyle('CorpoStyle', parent=styles['Normal'], spaceAfter=10, leading=14)
    
    story.append(Paragraph(titulo, style_titulo))
    story.append(Spacer(1, 10))
    
    linhas = texto_conteudo.strip().split('\n')
    for linha in linhas:
        if linha.strip():
            story.append(Paragraph(linha.strip(), style_corpo))
            
    doc.build(story)
    print(f"PDF criado com sucesso: {caminho}")

# Conteúdos dos documentos
politica_trocas = """
POLÍTICA DE TROCAS E DEVOLUÇÕES - LOJA TECHEXPRESS
O cliente tem o direito de desistir da compra e solicitar a devolução por arrependimento em até 7 dias corridos após o recebimento.
O produto deve ser devolvido na embalagem original, sem marcas de uso, acompanhado da nota fiscal.
A primeira troca de cada pedido tem o frete de retorno totalmente gratuito por nossa conta.
O reembolso do valor será feito na mesma forma de pagamento da compra após a triagem em nosso centro de distribuição.
"""

politica_privacidade = """
POLÍTICA DE PRIVACIDADE E SEGURANÇA
Coletamos o seu nome, e-mail, CPF e endereço de entrega estritamente para o processamento e envio do seu pedido.
Nós nunca compartilhamos, alugamos ou vendemos os dados cadastrais dos nossos clientes para nenhuma empresa terceira.
Os dados do seu cartão de crédito são criptografados na ponta e enviados diretamente para a operadora de pagamentos.
Nossa loja virtual não armazena nenhuma informação financeira ou de cartões em nossos servidores locais.
"""

faq_descontos = """
PERGUNTAS FREQUENTES E CAMPANHAS DE DESCONTO
Qual o prazo médio de entrega? O prazo estimado varia de 5 a 10 dias úteis para capitais e até 15 dias úteis para o interior.
Quais as formas de pagamento aceitas? Aceitamos PIX com 5% de desconto automático na finalização ou cartão de crédito em até 6x sem juros.
Existe cupom para novos clientes? Sim, utilize o cupom BENVINDO10 na tela de pagamento para ganhar 10% de desconto na primeira compra.
O cupom de primeira compra é válido apenas para carrinhos com valor total de produtos acima de R$ 100.
"""

if __name__ == "__main__":
    criar_pdf("trocas.pdf", "Política de Trocas e Devoluções", politica_trocas)
    criar_pdf("privacidade.pdf", "Política de Privacidade", politica_privacidade)
    criar_pdf("faq.pdf", "Perguntas Frequentes e Descontos", faq_descontos)
