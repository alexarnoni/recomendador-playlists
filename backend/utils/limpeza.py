import re

def limpar_frase(texto: str) -> str:
    """
    Limpa a frase removendo emojis, caracteres especiais e espaços desnecessários.
    Retorna uma string sanitizada para análise de sentimentos.
    """
    # Remove emojis e caracteres não textuais (mas mantém letras, números e pontuação básica)
    texto = re.sub(r'[^\w\s,.\'!?áéíóúãõâêôçÁÉÍÓÚÃÕÂÊÔÇ-]', '', texto)

    # Remove espaços repetidos
    texto = re.sub(r'\s+', ' ', texto)

    return texto.strip()
