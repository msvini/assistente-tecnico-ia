from PyPDF2 import PdfReader
import re
import io

def extrair_texto_pdf(arquivo_pdf_bytes):
    """Extrai e limpa texto de PDFs com tratamento avançado"""
    try:
        texto = ""
        with io.BytesIO(arquivo_pdf_bytes) as arquivo_pdf:
            leitor = PdfReader(arquivo_pdf)
            for pagina in leitor.pages:
                texto_pagina = pagina.extract_text() or ""  # Evita NoneType
                # Limpeza avançada
                texto_pagina = re.sub(r'<[^>]+>', '', texto_pagina)  # Remove HTML
                texto_pagina = re.sub(r'\s+', ' ', texto_pagina)     # Remove espaços múltiplos
                texto += texto_pagina.strip() + "\n"
        return texto
    except Exception as e:
        raise ValueError(f"Erro na leitura do PDF: {str(e)}")

def processar_documentos(pdfs):
    """Processa múltiplos PDFs garantindo integridade do conteúdo"""
    documentos = {}
    for nome, conteudo in pdfs.items():
        if not isinstance(conteudo, bytes):
            raise TypeError("O conteúdo do documento deve ser bytes")
        
        texto = extrair_texto_pdf(conteudo)
        
        # Preservar conteúdo completo mas limitar tamanho total para caber no contexto
        max_chars = 4000
        if len(texto) > max_chars:
            # Dividir em seções com base em numeração ou títulos
            sections = re.split(r'(\d+\.\s+[\w\s]+:|\*\*[\w\s]+\*\*)', texto)
            
            # Reconstruir preservando cabeçalhos de seção
            processed_text = sections[0][:max_chars//2]  # Início do documento
            
            # Adicionar seções importantes inteiras
            for i in range(1, len(sections), 2):
                if i+1 < len(sections) and len(processed_text) + len(sections[i]) + len(sections[i+1]) < max_chars:
                    processed_text += sections[i] + sections[i+1]
            
            texto = processed_text
            
        documentos[nome] = texto
    return documentos