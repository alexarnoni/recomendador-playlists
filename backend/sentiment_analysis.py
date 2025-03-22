from pysentimiento import create_analyzer

# Criar o analisador de emoções
analyzer = create_analyzer(task="emotion", lang="es")  # O modelo é treinado em espanhol, mas entende bem português

MAPEAMENTO = {
    "fear": "medo",
    "joy": "alegria",
    "sadness": "tristeza",
    "anger": "raiva",
    "love": "amor",
    "surprise": "surpresa"
}

def analisar_sentimento(texto):
    resultado = analyzer.predict(texto)
    sentimento_original = resultado.output  # Sentimento que o modelo detectou
    sentimento_corrigido = MAPEAMENTO.get(sentimento_original, sentimento_original)  # Aplicar correção

    print(f"Texto analisado: {texto} -> Sentimento detectado: {sentimento_original} -> Corrigido: {sentimento_corrigido}")
    return sentimento_corrigido