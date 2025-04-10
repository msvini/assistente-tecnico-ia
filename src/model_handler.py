from ctransformers import AutoModelForCausalLM

def carregar_modelo():
    """
    Carrega o modelo TinyLlama-1.1B no formato GGUF e retorna uma função de predição configurada.
    O modelo é baixado do Hugging Face Hub e configurado para realizar inferências com parâmetros
    ajustáveis, como temperatura, número máximo de tokens gerados e tokens de parada.
    Returns:
        function: Uma função `predict` que realiza inferências no modelo carregado.
        A função `predict` aceita os seguintes parâmetros:
            - prompt (str): O texto de entrada para o modelo.
            - temperatur    e (float, opcional): Controla a aleatoriedade da geração. Valores mais baixos
              resultam em saídas mais determinísticas. Padrão é 0.1.
            - max_new_tokens (int, opcional): Número máximo de novos tokens a serem gerados. Padrão é 500.
            - stop (list, opcional): Lista de tokens de parada para truncar a geração. Padrão inclui
              ["Documentos disponíveis:", "Pergunta:", "Usuário:"].
        Retorna:
            str: O texto gerado pelo modelo, truncado nos tokens de parada, se aplicável.
    """
    # Baixe o modelo TinyLlama-1.1B (formato GGUF) do Hugging Face Hub
    model = AutoModelForCausalLM.from_pretrained(
        "TheBloke/TinyLlama-1.1B-1T-OpenOrca-GGUF",
        model_file="tinyllama-1.1b-1t-openorca.Q4_K_M.gguf",
        model_type="llama",
        gpu_layers=50,  # Ajuste conforme sua GPU
        context_length=2048  # Aumentar o contexto
    )
    
    # Função wrapper para inferência controlada
    def predict(prompt, temperature=0.1, max_new_tokens=500, stop=None):
        # Definir tokens de parada para evitar geração contínua
        stop_tokens = stop or ["Documentos disponíveis:", "Pergunta:", "Usuário:"]
        
        # Realizar a inferência com parâmetros mais rigorosos
        result = model(
            prompt,
            temperature=temperature,
            max_new_tokens=max_new_tokens,
            top_p=0.95,     # Maior controle de diversidade
            top_k=10,       # Limitar opções de tokens
            repetition_penalty=1.2,  # Penalidade maior para repetições
            stop=stop_tokens
        )
        
        # Verificar e truncar em tokens de parada
        for token in stop_tokens:
            if token in result:
                result = result.split(token)[0]
        
        return result
    
    return predict
