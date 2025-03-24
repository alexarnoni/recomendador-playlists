from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from sentiment_analysis import analisar_sentimento
from spotify_api import buscar_playlist
from historico import salvar_recomendacao
from cache import playlist_ja_usada, adicionar_ao_cache

import random

app = FastAPI()

# Servir arquivos estáticos
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")
templates = Jinja2Templates(directory="../frontend/templates")

@app.get("/")
def serve_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Frases para gerar mensagem personalizada
INTROS = [
    "Se quiser mudar o clima,",
    "Vai com calma e escuta isso:",
    "Pra melhorar o astral,",
    "Se prepara pra sentir:",
    "Olha só o que separei pra você:",
    "Toma essa pra animar o rolê:",
    "Nada como uma trilha sonora boa, né?",
]

HUMORADAS = {
    "tristeza": ["algo leve", "algo pra levantar o ânimo", "músicas pra sair da fossa"],
    "alegria": ["mais animação", "mais motivos pra sorrir", "um som pra manter o pique"],
    "raiva": ["um som pra descarregar", "algo que acalma a alma", "batidas pra extravasar"],
    "amor": ["algo romântico", "pra curtir juntinho", "trilhas que aquecem o coração"],
    "medo": ["algo reconfortante", "uma trilha pra encorajar", "músicas pra enfrentar qualquer coisa"],
    "surpresa": ["uma surpresa musical", "algo fora do comum", "playlists inesperadas que valem o play"],
}

def gerar_mensagem(sentimento):
    intro = random.choice(INTROS)
    complemento = random.choice(HUMORADAS.get(sentimento, ["uma boa música"]))
    return f"{intro} {complemento} 🎶"

@app.get("/api/recomendar")
def recomendar_playlist(frase: str):
    if not frase or not frase.strip():
        return JSONResponse(
            status_code=400,
            content={"erro": "A frase não pode estar vazia."}
        )

    if len(frase.strip()) < 3:
        return JSONResponse(
            status_code=400,
            content={"erro": "A frase é muito curta para análise."}
        )

    sentimento = analisar_sentimento(frase)

    print(f"Sentimento detectado pela API (corrigido): {sentimento}")

    playlist_1 = playlist_2 = None

    if sentimento in ["tristeza", "raiva", "medo"]:
        # Playlist para melhorar o humor
        playlist_1 = buscar_playlist("alegria")
        tentativas = 0
        while playlist_ja_usada("alegria", playlist_1) and tentativas < 5:
            playlist_1 = buscar_playlist("alegria")
            tentativas += 1
        adicionar_ao_cache("alegria", playlist_1)

        # Playlist para intensificar o sentimento
        playlist_2 = buscar_playlist(sentimento)
        tentativas = 0
        while playlist_ja_usada(sentimento, playlist_2) and tentativas < 5:
            playlist_2 = buscar_playlist(sentimento)
            tentativas += 1
        adicionar_ao_cache(sentimento, playlist_2)
    else:
        playlist_1 = buscar_playlist(sentimento)
        tentativas = 0
        while playlist_ja_usada(sentimento, playlist_1) and tentativas < 5:
            playlist_1 = buscar_playlist(sentimento)
            tentativas += 1
        adicionar_ao_cache(sentimento, playlist_1)

    texto = gerar_mensagem(sentimento)
    salvar_recomendacao(frase, sentimento, playlist_1, playlist_2)

    return JSONResponse(content={
        "mensagem": texto,
        "playlist_1": playlist_1,
        "playlist_2": playlist_2
    })
