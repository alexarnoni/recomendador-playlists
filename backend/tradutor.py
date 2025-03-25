import random

# Traduções para termos de busca no Spotify
MAPA_BUSCA = {
    "alegria": ["feel good", "good vibes", "party time", "sunny mood"],
    "tristeza": ["sad songs", "melancholy", "heartbreak", "rainy day"],
    "raiva": ["rage", "angry rock", "workout angry", "hardcore"],
    "amor": ["love songs", "romantic", "slow love", "amor acústico"],
    "medo": ["dark ambient", "cinematic tension", "eerie mood", "nightfall"],
    "surpresa": ["unexpected gems", "shuffle playlist", "weird & wonderful"]
}

def traduzir_para_ingles(sentimento: str) -> str:
    """
    Retorna um termo de busca em inglês baseado no sentimento identificado.
    Se o sentimento não estiver no dicionário, retorna o próprio sentimento.
    """
    return random.choice(MAPA_BUSCA.get(sentimento.lower(), [sentimento]))
