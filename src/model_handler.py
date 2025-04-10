from ctransformers import AutoModelForCausalLM

def carregar_modelo():
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