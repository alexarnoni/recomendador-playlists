from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from services.sentiment_analysis import analisar_sentimento
from services.spotify_api import buscar_playlist
from services.historico import salvar_recomendacao
from utils.cache import playlist_ja_usada, adicionar_ao_cache
import random
import json
import re
from config import settings

router = APIRouter()
templates = Jinja2Templates(directory="../frontend/templates")

INTROS = [
    "Se quiser mudar o clima,", "Vai com calma e escuta isso:", "Pra melhorar o astral,",
    "Se prepara pra sentir:", "Olha só o que separei pra você:", "Toma essa pra animar o rolê:",
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

@router.get("/")
def serve_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/sobre")
def sobre(request: Request):
    return templates.TemplateResponse("sobre.html", {"request": request})

@router.get("/api/recomendar")
def recomendar_playlist(frase: str):
    if not frase or not frase.strip():
        return JSONResponse(status_code=400, content={"erro": "A frase não pode estar vazia."})

    frase_limpa = re.sub(r"[^\w\s]", "", frase).strip()
    if len(frase_limpa) < 3:
        return JSONResponse(status_code=400, content={"erro": "A frase é muito curta ou confusa para análise."})

    sentimento = analisar_sentimento(frase)
    playlist_1 = playlist_2 = None

    if sentimento in ["tristeza", "raiva", "medo"]:
        playlist_1 = buscar_playlist("alegria")
        tentativas = 0
        while playlist_ja_usada("alegria", playlist_1) and tentativas < 5:
            playlist_1 = buscar_playlist("alegria")
            tentativas += 1
        adicionar_ao_cache("alegria", playlist_1)

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

    salvar_recomendacao(frase, sentimento, playlist_1, playlist_2)
    texto = gerar_mensagem(sentimento)

    return JSONResponse(content={
        "mensagem": texto,
        "playlist_1": playlist_1,
        "playlist_2": playlist_2
    })

@router.get("/api/historico")
def listar_historico(limit: int = 10):
    try:
        with open("historico_recomendacoes.json", "r", encoding="utf-8") as f:
            historico = json.load(f)
    except FileNotFoundError:
        historico = []
    return historico[-limit:][::-1]
