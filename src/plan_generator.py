def gerar_plano_acao(pergunta, contexto, modelo):
    """
    Função simplificada que retorna um plano de ação para responder à pergunta
    Não usamos o formato JSON para evitar erros de parsing
    """
    prompt = """
    Crie um plano simples para responder a seguinte pergunta técnica com base nos documentos carregados.
    
    Pergunta: {pergunta}
    
    O plano deve ter os seguintes passos:
    1. Identificar palavras-chave da pergunta
    2. Buscar por estas palavras-chave nos documentos
    3. Extrair informações relevantes
    4. Formatar uma resposta clara e concisa
    
    Retorne apenas os passos enumerados, sem explicações adicionais.
    """.format(pergunta=pergunta)
    
    resposta = modelo(prompt, max_new_tokens=200, temperature=0.1)
    
    # Retornamos um dicionário simples para maior confiabilidade
    return {
        "steps": [
            {"step_description": "Identificar palavras-chave", "requer_conhecimento": False},
            {"step_description": "Buscar por palavras-chave", "requer_conhecimento": True},
            {"step_description": "Extrair informações relevantes", "requer_conhecimento": True},
            {"step_description": "Formatar resposta", "requer_conhecimento": True}
        ]
    }