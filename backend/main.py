from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from collections import Counter
from config import settings

from sentiment_analysis import analisar_sentimento
from spotify_api import buscar_playlist
from historico import salvar_recomendacao
from cache import playlist_ja_usada, adicionar_ao_cache

import json
import random


app = FastAPI()

# Servir arquivos estáticos
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")
templates = Jinja2Templates(directory="../frontend/templates")

@app.get("/")
def serve_index(request: Request):
    return templates.TemplateResponse(request, "index.html")

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

@app.get("/admin")
def admin_login(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request, "erro": None})

@app.post("/admin")
def admin_painel(request: Request, token: str = Form(...)):
    if token != settings.ADMIN_TOKEN:
        return templates.TemplateResponse("admin_login.html", {
            "request": request,
            "erro": "Senha incorreta!"
        })

    try:
        with open("historico_recomendacoes.json", "r", encoding="utf-8") as f:
            historico = json.load(f)
    except FileNotFoundError:
        historico = []

    total = len(historico)
    ultimas_frases = [item["frase"] for item in historico[-5:]][::-1]
    sentimentos = [item["sentimento"] for item in historico]
    mais_comuns = Counter(sentimentos).most_common()

    # ✅ Extra: Playlists mais recomendadas
    contagem_playlists = {}
    for item in historico:
        for key in ["playlist_1", "playlist_2"]:
            playlist = item.get(key)
            if playlist:
                url = playlist["url"]
                nome = playlist["nome"]
                chave = (nome, url)
                contagem_playlists[chave] = contagem_playlists.get(chave, 0) + 1

    mais_recomendadas = [
        {"nome": nome, "url": url, "contagem": contagem}
        for (nome, url), contagem in sorted(contagem_playlists.items(), key=lambda x: x[1], reverse=True)
    ][:5]  # Top 5

    return templates.TemplateResponse(request, "admin.html", {
        "total": total,
        "ultimas_frases": ultimas_frases,
        "mais_comuns": mais_comuns,
        "recomendacoes": historico,
        "mais_recomendadas": mais_recomendadas
    })

@app.get("/sobre")
def sobre(request: Request):
    return templates.TemplateResponse(request, "sobre.html")

@app.post("/admin/limpar")
def limpar_historico(request: Request, senha: str = Form(...)):
    if senha != settings.ADMIN_TOKEN:
        return templates.TemplateResponse("admin_login.html", {
            "request": request,
            "erro": "Senha incorreta para limpeza!"
        })

    try:
        with open("historico_recomendacoes.json", "w", encoding="utf-8") as f:
            json.dump([], f)
        print("[ADMIN] Histórico limpo com sucesso!")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao limpar histórico: {str(e)}")

    return RedirectResponse(url="/admin", status_code=302)
