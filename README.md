
# Assistente Técnico de IA - Documentação do Projeto 

---

## Objetivo 
Desenvolver um assistente virtual para análise técnica de documentos PDF, capaz de:  
- Processar conteúdo complexo  
- Responder perguntas específicas com base no material carregado  
- Manter contexto de conversa com eficiência em hardware limitado  

---
##  Como Usar

1.  Carregue documentos PDF através do painel lateral
    
2.  Faça perguntas técnicas na caixa de chat
    
3.  Revise o histórico de conversa
    
4.  Use "Limpar Histórico" para reiniciar a sessão
    

##  Funcionalidades

### Processamento de Documentos 
- Extração de texto com tratamento de caracteres especiais  
- Divisão inteligente em chunks de 512 tokens  
- Indexação semântica usando FAISS + SentenceTransformer  

### Modelo de Linguagem 
- **TinyLlama-1.1B**:  
  - Contexto de 2048 tokens  
  - Penalidade de repetição (1.2)  
  - Otimizado para CPU/GPU básica  

### Sistema de Memória 
- Histórico circular das últimas 6 interações  
- Limpeza automática para evitar sobrecarga  

### Interface 
- Upload múltiplo de PDFs via Streamlit  
- Visualização em tempo real do histórico  
- Botão para reiniciar contexto  
    

## Solução de Problemas Comuns

-   **Erro ao carregar modelo**: Verifique o caminho `models/` e o arquivo GGUF
    
-   **Problemas com PDFs**: Certifique-se de que os arquivos não estão corrompidos
    
-   **Respostas repetitivas**: Reduza o `max_new_tokens` no model_handler.py
    

##  Estrutura do Projeto

   ```bash  

.
├── models/           # Modelos de linguagem
├── docs/             # Documentação de exemplo
├── chat_interface.py # Interface principal
├── model_handler.py  # Gerenciamento de modelos
├── pdf_processor.py  # Processamento de documentos
└── requirements.txt  # Dependências

   ```
---
## Como Executar 

### Pré-requisitos 
- **Sistema Operacional**: Windows 10+/Linux Ubuntu 20.04+/macOS 12+  
- **Hardware Mínimo**:  
  - 4GB RAM  
  - 2GB de espaço em disco  
  - CPU x86-64 com suporte a AVX2  

### Passo a Passo 
1. **Preparar Ambiente**:  

   ```bash  
   
   git clone https://github.com/seu-usuario/assistente-tecnico-ia.git  
   cd assistente-tecnico-ia  
   python -m venv .venv  
   # Linux/Mac 
   source .venv/bin/activate  
   # Windows 
   .venv\Scripts\activate  

3.  **Instalar Dependências**:
    
    ```bash

    pip install -r requirements.txt  
    
4.  **Baixar Modelo**:
    
    ```bash
    
	# Criando o diretório 'models'
	mkdir -p models  # Linux/Mac
	mkdir models     # Windows

	 Baixando o modelo TinyLlama 1.1B 4-bit
	#Linux/Mac:
	curl -L https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf -o models/tinyllama.gguf
	#Windows:
	curl -L https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf -o models\tinyllama.gguf
	
5.  **Executar Aplicação**:
    
    ```bash

    streamlit run chat_interface.py  
    
    Acesse: `http://localhost:8501`
    
----------


## Arquitetura do Sistema

```flowchart LR  

    A[PDF] --> B(Extrair Texto)  
    B --> C{Chunking 512 tokens}  
    C --> D[Gerar Embeddings]  
    D --> E[Indexar no FAISS]  
    E --> F[Busca Semântica]  

```


## Limitações e Melhorias Futuras

### Limitações Atuais

- **Precisão Reduzida**  
  - Precisão Reduzida:
  	- A versão do TinyLlama-1.1B apresenta limitações inerentes à quantização, com margem de erro 8-12% superior a modelos não quantizados (ex: Llama2-7B em 16-bit). Isso se manifesta em:

        - Alucinações frequentes: Geração de informações não presentes nos documentos, especialmente em consultas ambíguas.

        - Respostas inconsistentes: Variações na qualidade das respostas dependendo da complexidade sintática da pergunta.
   - Inviabilidade de Fine-Tuning: A arquitetura quantizada não permite ajustes pontuais sem reconversão total do modelo, limitando adaptações a domínios específicos.

- **Janela de Contexto**  
  - Máximo de 2048 tokens (cerca de 5 páginas de texto)  
  - Dificuldade em manter coerência em conversas muito longas  

- **Requisitos de Hardware**  
  - CPU moderna com instruções AVX2 obrigatórias  
  - Consumo médio de 2.8GB RAM em uso intensivo  

- **Formato de Documentos**  
  - PDFs com tabelas/imagens são parcialmente suportados  
  - Limite prático de 50 páginas por documento  

---



### Roadmap de Melhorias

-  **Modelos Mais Robustos**
    - Adoção de Modelos de Linguagem Mais Capazes  
	  - Implementação de modelos com arquiteturas modernas e maior capacidade de entendimento contextual  
	  - Exemplos de modelos candidatos:  
	    - *Alta Precisão*: Llama3-70B (70B parâmetros, contexto de 8K tokens)  
	    - *Balanceado*: Mistral-12B (12B parâmetros, excelente custo-benefício)  
	    - *Eficiência*: Phi-3-medium (14B parâmetros, otimizado para raciocínio técnico)  
        
    -   Suporte a múltiplos modelos (usuário escolhe precisão vs. velocidade)
        
-  **Otimizações de Memória**
    
    -   Implementar paginação de contexto
        
    -   Compressão lossless do histórico
        
- **Processamento Avançado**
    
    -   Integração com OCR para tabelas/figuras (ex: Tesseract)
        
    -   Reconhecimento de layout complexo
        
-  **Experiência do Usuário**
    
    -   Sistema de feedback para corrigir respostas
        
    -   Explicação visual do raciocínio (RAG)
        

----------

## Referências Técnicas

-   [TinyLlama: Modelos Quantizados](https://huggingface.co/TheBloke)
    
-   [FAISS: Busca Vetorial Eficiente](https://github.com/facebookresearch/faiss)
    
-   [Streamlit: Melhores Práticas](https://docs.streamlit.io)
    
-   [Otimização de LLMs para CPU](https://arxiv.org/abs/2310.10537)
