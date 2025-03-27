import json
from datetime import datetime
import os

CAMINHO_ARQUIVO = "historico_recomendacoes.json"

def salvar_recomendacao(frase, sentimento, playlist_1, playlist_2=None):
    nova_entrada = {
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "frase": frase.strip(),
        "sentimento": sentimento.strip(),
        "playlist_1": {
            "nome": playlist_1.get("nome", "").strip(),
            "url": playlist_1.get("url", "").strip()
        },
        "playlist_2": None
    }

    if playlist_2:
        nova_entrada["playlist_2"] = {
            "nome": playlist_2.get("nome", "").strip(),
            "url": playlist_2.get("url", "").strip()
        }

    # Carregar histórico existente
    historico = []
    if os.path.exists(CAMINHO_ARQUIVO):
        with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as f:
            try:
                historico = json.load(f)
            except json.JSONDecodeError:
                historico = []

    # Evita duplicatas idênticas consecutivas
    if historico:
        ultima = historico[-1]
        if (
            ultima["frase"] == nova_entrada["frase"] and
            ultima["sentimento"] == nova_entrada["sentimento"] and
            ultima["playlist_1"] == nova_entrada["playlist_1"] and
            ultima.get("playlist_2") == nova_entrada.get("playlist_2")
        ):
            print("[HISTÓRICO] Entrada idêntica já salva. Ignorando.")
            return

    # Adiciona e salva
    historico.append(nova_entrada)
    with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=2)

