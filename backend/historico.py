import json
from datetime import datetime
import os

CAMINHO_ARQUIVO = "historico_recomendacoes.json"

def salvar_recomendacao(frase, sentimento, playlist_1, playlist_2=None):
    nova_entrada = {
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "frase": frase,
        "sentimento": sentimento,
        "playlist_1": {
            "nome": playlist_1["nome"],
            "url": playlist_1["url"]
        },
        "playlist_2": None
    }

    if playlist_2:
        nova_entrada["playlist_2"] = {
            "nome": playlist_2["nome"],
            "url": playlist_2["url"]
        }

    # Carregar histórico existente, se houver
    historico = []
    if os.path.exists(CAMINHO_ARQUIVO):
        with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as f:
            try:
                historico = json.load(f)
            except json.JSONDecodeError:
                historico = []

    # Adicionar nova entrada e salvar de volta
    historico.append(nova_entrada)
    with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=2)
