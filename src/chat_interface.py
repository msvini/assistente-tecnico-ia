import streamlit as st
from model_handler import carregar_modelo
from pdf_processor import processar_documentos
from plan_generator import gerar_plano_acao
import re

final_prompt_template = """
Você é um assistente técnico especializado que SOMENTE responde com base nos documentos fornecidos.

REGRAS RIGOROSAS:
1. Se a resposta EXATA não estiver nos documentos, diga APENAS: "Não encontrei informações sobre isso nos documentos carregados."
2. NUNCA invente informações, use conhecimento externo ou repita a pergunta/documentos disponíveis.
3. SEMPRE cite exatamente de qual parte do documento tirou a informação (ex: "Segundo o Manual X, página 3...").
4. NUNCA repita informações - mencione cada fato apenas UMA vez, mesmo que presente em múltiplos documentos.
5. Responda APENAS ao que foi perguntado, de forma direta e objetiva (sem diálogo ou formato de perguntas/respostas).
6. Limite sua resposta a no máximo 1000 caracteres, priorizando as 3-5 informações mais relevantes.
7. NUNCA inclua frases como "conteúdo disponível", "documentos carregados" ou similares.

FORMATO DA RESPOSTA:
**Resposta:** [Lista concisa de pontos-chave APENAS do documento, com citações explícitas]

Plano de ação para esta pergunta:
{plano}

Documentos disponíveis:
{docs}

Pergunta: {question}
"""

def clean_document_input(text):
    """Limpa o documento de entrada para remover repetições e conteúdo irrelevante"""
    # Remove números aleatórios e sequências repetitivas
    text = re.sub(r'\d{4,}º?.*?(?=\n|\Z)', '', text, flags=re.DOTALL)
    
    # Remove linhas que se repetem mais de 2 vezes
    lines = text.split('\n')
    unique_lines = []
    line_count = {}
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if line in line_count:
            line_count[line] += 1
            if line_count[line] <= 2:  # Permite no máximo 2 ocorrências
                unique_lines.append(line)
        else:
            line_count[line] = 1
            unique_lines.append(line)
    
    return '\n'.join(unique_lines)

def extract_clean_response(text):
    """Extrai uma resposta limpa e focada, sem repetições"""
    # Procura pela resposta formatada
    match = re.search(r'\*\*Resposta:\*\*\s*(.*?)(?=\*\*|\Z)', text, re.DOTALL)
    
    if match:
        content = match.group(1).strip()
    else:
        # Tenta outro formato comum
        match = re.search(r'Resposta:\s*(.*?)(?=Pergunta:|\Z)', text, re.DOTALL)
        if match:
            content = match.group(1).strip()
        else:
            content = text.strip()
    
    # Remove linhas repetidas na resposta
    lines = content.split('\n')
    unique_lines = []
    seen_lines = set()
    
    for line in lines:
        clean_line = re.sub(r'\s+', ' ', line).strip()
        if not clean_line:
            continue
        
        # Ignora linhas muito similares ou idênticas já vistas
        if clean_line not in seen_lines:
            seen_lines.add(clean_line)
            unique_lines.append(line)
    
    clean_content = '\n'.join(unique_lines)
    
    # Se a resposta estiver vazia após limpeza
    if not clean_content or len(clean_content) < 10:
        return "Não encontrei informações específicas sobre isso nos documentos carregados."
    
    return clean_content

def formatar_plano_acao(plano):
    """Formata o plano de ação para incluir no prompt"""
    passos_formatados = []
    
    for idx, passo in enumerate(plano["steps"]):
        passos_formatados.append(f"{idx+1}. {passo['step_description']}")
    
    return "\n".join(passos_formatados)

def main():
    st.title("Assistente Técnico de IA")
    modelo = carregar_modelo()

    # Inicializar sessões
    if "historico" not in st.session_state:
        st.session_state.historico = []
    if "documentos" not in st.session_state:
        st.session_state.documentos = {}
    
    # Upload de PDFs
    with st.sidebar:
        uploaded_files = st.file_uploader("Carregar documentos técnicos (PDF)", type="pdf", accept_multiple_files=True)
        if uploaded_files:
            for file in uploaded_files:
                st.session_state.documentos[file.name] = file.getvalue()
        
        # Botão para limpar histórico
        if st.button("Limpar Histórico"):
            st.session_state.historico = []
            st.rerun()
    
    # Container para o histórico de mensagens
    chat_container = st.container()
    
    # Exibir todo o histórico de mensagens
    with chat_container:
        for pergunta, resposta in st.session_state.historico:
            with st.chat_message("user"):
                st.markdown(f"**Você:** {pergunta}")
            with st.chat_message("assistant"):
                st.markdown(resposta)
    
    # Chat input
    pergunta = st.chat_input("Faça sua pergunta técnica...")
    
    if pergunta:
        # Exibir pergunta do usuário
        with chat_container:
            with st.chat_message("user"):
                st.markdown(f"**Você:** {pergunta}")
        
        # Área de processamento
        with st.spinner("Analisando documentos e preparando resposta..."):
            try:
                # Processar documentos
                docs_processados = processar_documentos(st.session_state.documentos)
                
                # Limpar e preparar o prompt com contexto dos documentos
                documentos_formatados = ""
                for nome, conteudo in docs_processados.items():
                    # Limpa o conteúdo antes de adicionar ao contexto
                    conteudo_limpo = clean_document_input(conteudo)
                    documentos_formatados += f"Documento: {nome}\n{conteudo_limpo}\n\n"
                
                # Gerar plano de ação
                plano = gerar_plano_acao(pergunta, documentos_formatados, modelo)
                plano_formatado = formatar_plano_acao(plano)
                
                # Gerar resposta
                resposta_bruta = modelo(
                    final_prompt_template.format(
                        question=pergunta,
                        docs=documentos_formatados,
                        plano=plano_formatado
                    ),
                    temperature=0.1,
                    max_new_tokens=1000,
                    stop=["Documento:", "Pergunta:"]
                )
                
                # Limpar e focar a resposta
                conteudo_resposta = extract_clean_response(resposta_bruta)
                resposta_final = f"**Resposta:** {conteudo_resposta}"
                
                # Adicionar ao histórico
                st.session_state.historico.append((pergunta, resposta_final))
                
                # Exibir resposta no container
                with chat_container:
                    with st.chat_message("assistant"):
                        st.markdown(resposta_final)

            except Exception as e:
                with chat_container:
                    with st.chat_message("assistant"):
                        st.error(f"Erro ao processar a solicitação: {str(e)}")

if __name__ == "__main__":
    main()
