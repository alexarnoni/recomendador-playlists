import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import random
from collections import defaultdict, deque
from config import settings
from tradutor import traduzir_para_ingles

# Carregar variáveis do .env
load_dotenv()

# Configurar autenticação no Spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=settings.SPOTIFY_CLIENT_ID,
    client_secret=settings.SPOTIFY_CLIENT_SECRET
))

# Cache temporário por sentimento
CACHE_PLAYLISTS = defaultdict(lambda: deque(maxlen=3))  # guarda as 3 últimas por sentimento

def buscar_playlist(sentimento):
    termo_busca = traduzir_para_ingles(sentimento)

    try:
        resultado = sp.search(q=termo_busca, type="playlist", limit=10)
        playlists = resultado.get("playlists", {}).get("items", [])

        if not playlists:
            print(f"[Spotify] Nenhuma playlist encontrada para: {termo_busca}")
            return {
                "url": "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M",
                "nome": "Playlist padrão",
                "imagem": None
            }

        # Tenta encontrar uma que ainda não esteja no cache
        tentativas = 5
        ultima_usadas = CACHE_PLAYLISTS[sentimento]
        escolha = None

        while tentativas > 0:
            candidata = random.choice(playlists)
            url = candidata["external_urls"]["spotify"]
            if url not in ultima_usadas:
                escolha = candidata
                break
            tentativas -= 1

        # Se não achou diferente, pega uma qualquer
        playlist = escolha if escolha else random.choice(playlists)

        url = playlist["external_urls"]["spotify"]
        nome = playlist["name"]
        imagem = playlist["images"][0]["url"] if playlist.get("images") else None

        # Atualiza o cache
        CACHE_PLAYLISTS[sentimento].append(url)

        return {"url": url, "nome": nome, "imagem": imagem}

    except Exception as e:
        print(f"[ERRO Spotify] Erro ao buscar playlist: {e}")
        return {
            "url": "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M",
            "nome": "Playlist padrão",
            "imagem": None
        }