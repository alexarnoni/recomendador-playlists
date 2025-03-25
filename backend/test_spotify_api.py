# test_spotify_api.py
from unittest.mock import patch
from spotify_api import buscar_playlist

@patch("spotify_api.traduzir_para_ingles", return_value="happy vibes")
@patch("spotify_api.sp.search")
def test_buscar_playlist(mock_search, mock_traduzir):
    mock_search.return_value = {
        "playlists": {
            "items": [
                {
                    "name": "Happy Vibes Playlist",
                    "external_urls": {"spotify": "https://open.spotify.com/playlist/teste"},
                    "images": [{"url": "https://img.com/capa.png"}]
                }
            ]
        }
    }

    resultado = buscar_playlist("alegria")

    assert resultado["nome"] == "Happy Vibes Playlist"
    assert resultado["url"] == "https://open.spotify.com/playlist/teste"
    assert resultado["imagem"] == "https://img.com/capa.png"
