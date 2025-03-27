from pysentimiento import create_analyzer
from utils.limpeza import limpar_frase

# Criar o analisador de emoções
analyzer = create_analyzer(task="emotion", lang="es")  # Modelo entende bem português

# Mapeamento dos sentimentos do modelo para português
MAPEAMENTO = {
    "fear": "medo",
    "joy": "alegria",
    "sadness": "tristeza",
    "anger": "raiva",
    "love": "amor",
    "surprise": "surpresa"
}

def traduzir_sentimento(sentimento_original: str) -> str:
    return MAPEAMENTO.get(sentimento_original, sentimento_original)

def analisar_sentimento(texto: str) -> str:
    texto_limpo = limpar_frase(texto)
    resultado = analyzer.predict(texto_limpo)
    sentimento_original = resultado.output
    sentimento_corrigido = traduzir_sentimento(sentimento_original)

    print(f"[ANÁLISE] Frase original: {texto}")
    print(f"[ANÁLISE] Frase limpa: {texto_limpo}")
    print(f"[ANÁLISE] Sentimento detectado: {sentimento_original} → {sentimento_corrigido}")

    return sentimento_corrigido
