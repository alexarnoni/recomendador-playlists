from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from sentiment_analysis import analisar_sentimento
from spotify_api import buscar_playlist
from historico import salvar_recomendacao
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

app = FastAPI()

# Servir arquivos estáticos
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")
templates = Jinja2Templates(directory="../frontend/templates")

@app.get("/")
def serve_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/recomendar")
def recomendar_playlist(frase: str):
    sentimento = analisar_sentimento(frase)

    print(f"Sentimento detectado pela API (corrigido): {sentimento}")

    if sentimento in ["tristeza", "raiva", "medo"]:
        playlist_1 = buscar_playlist("alegria")  # Melhorar o humor
        playlist_2 = buscar_playlist(sentimento)  # Intensificar o sentimento
        texto = "Se quiser sair da fossa, escute isso! Ou, se quiser se afundar mais, tente essa outra:"
    else:
        playlist_1 = buscar_playlist(sentimento)
        playlist_2 = None
        texto = "Aqui está uma playlist para combinar com seu humor!"

    salvar_recomendacao(frase, sentimento, playlist_1, playlist_2)
    
    return JSONResponse(content={
        "mensagem": texto,
        "playlist_1": playlist_1,
        "playlist_2": playlist_2
    })
