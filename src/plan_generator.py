def gerar_plano_acao(pergunta, contexto, modelo):
    """
    Gera um plano de ação estruturado para responder a uma pergunta técnica com base em documentos fornecidos.
    Args:
        pergunta (str): A pergunta técnica que precisa ser respondida.
        contexto (str): O contexto ou informações adicionais relevantes para a pergunta.
        modelo (callable): Uma função ou modelo que gera respostas baseadas em prompts fornecidos.
    Returns:
        dict: Um dicionário contendo os passos do plano de ação no formato:
            {
                "steps": [
                    {"step_description": "Descrição do passo 1"},
                    {"step_description": "Descrição do passo 2"},
                    ...
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
    
    # Processar a resposta para transformá-la em um formato estruturado
    passos = []
    for linha in resposta.strip().split('\n'):
        linha = linha.strip()
        if linha and any(str(i) in linha[:2] for i in range(1, 10)):
            # Remove o número e o ponto no início
            texto_passo = linha[2:].strip() if linha[1] == '.' else linha[3:].strip()
            passos.append({"step_description": texto_passo})
    
    # Se não conseguiu extrair passos da resposta, use o plano padrão
    if not passos:
        passos = [
            {"step_description": "Identificar palavras-chave"},
            {"step_description": "Buscar por palavras-chave"},
            {"step_description": "Extrair informações relevantes"},
            {"step_description": "Formatar resposta"}
        ]
    
    return {
        "steps": passos
    }
