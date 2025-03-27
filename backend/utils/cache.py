import time
from collections import defaultdict

# cache_por_sentimento: {"tristeza": [(timestamp, playlist_url), ...]}
cache_por_sentimento = defaultdict(list)
TEMPO_EXPIRACAO = 60 * 10  # 10 minutos

def adicionar_ao_cache(sentimento, playlist_url):
    agora = time.time()
    cache_por_sentimento[sentimento].append((agora, playlist_url))

def limpar_cache_expirado():
    agora = time.time()
    for sentimento in list(cache_por_sentimento):
        cache_por_sentimento[sentimento] = [
            (ts, url) for ts, url in cache_por_sentimento[sentimento]
            if agora - ts < TEMPO_EXPIRACAO
        ]

def playlist_ja_usada(sentimento, playlist_url):
    limpar_cache_expirado()
    return any(url == playlist_url for _, url in cache_por_sentimento[sentimento])
