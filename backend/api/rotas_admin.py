from fastapi import APIRouter, Form, HTTPException, Request, status, Depends
from fastapi.responses import RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from collections import Counter
import json

from db import get_db
from models.usuario import Usuario
from utils.hash import verificar_senha, gerar_hash
from utils.auth import criar_cookie_login, remover_cookie_login, redirecionar_se_nao_logado

router = APIRouter()
templates = Jinja2Templates(directory="../frontend/templates")

# 🔐 GET: Página de login
@router.get("/admin")
def admin_login(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request, "erro": None})


# 🔐 POST: Autenticar usuário
@router.post("/admin/login")
def login_usuario(
    request: Request,
    username: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(Usuario).filter(Usuario.username == username).first()
    if not user or not verificar_senha(senha, user.senha_hash):
        return templates.TemplateResponse("admin_login.html", {
            "request": request,
            "erro": "Credenciais inválidas!"
        })

    response = RedirectResponse(url="/admin/painel", status_code=status.HTTP_302_FOUND)
    criar_cookie_login(response)
    print("[LOGIN] Cookie de sessão criado com sucesso")
    return response


# 🔐 GET: Formulário de registro (protegido)
@router.get("/admin/registrar")
def exibir_registro(request: Request, db: Session = Depends(get_db)):
    if db.query(Usuario).first():  # já existe admin
        return RedirectResponse(url="/admin", status_code=302)

    return templates.TemplateResponse("admin_registro.html", {"request": request})


# 🔐 POST: Registrar novo usuário (só se não existir nenhum ainda)
@router.post("/admin/registrar")
def registrar_usuario(
    request: Request,
    username: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db)
):
    if db.query(Usuario).first():
        return templates.TemplateResponse("admin_login.html", {
            "request": request,
            "erro": "Já existe um administrador cadastrado!"
        })

    novo = Usuario(username=username, senha_hash=gerar_hash(senha))
    db.add(novo)
    db.commit()

    return templates.TemplateResponse("admin_login.html", {
        "request": request,
        "mensagem": "Usuário criado com sucesso! Faça login."
    })


# ✅ PAINEL DE ADMIN
@router.get("/admin/painel")
def admin_painel(request: Request):
    redirecao = redirecionar_se_nao_logado(request)
    if isinstance(redirecao, RedirectResponse):
        return redirecao

    response = Response()
    criar_cookie_login(response)  # 🔄 Renova sessão

    try:
        with open("historico_recomendacoes.json", "r", encoding="utf-8") as f:
            historico = json.load(f)
    except FileNotFoundError:
        historico = []

    sentimentos = [item["sentimento"] for item in historico]
    mais_comuns = Counter(sentimentos).most_common()

    contagem_playlists = {}
    for item in historico:
        for key in ["playlist_1", "playlist_2"]:
            playlist = item.get(key)
            if playlist:
                chave = (playlist["nome"], playlist["url"])
                contagem_playlists[chave] = contagem_playlists.get(chave, 0) + 1

    mais_recomendadas = [
        {"nome": nome, "url": url, "contagem": contagem}
        for (nome, url), contagem in sorted(contagem_playlists.items(), key=lambda x: x[1], reverse=True)
    ][:5]

    return templates.TemplateResponse(request, "admin.html", {
        "request": request,
        "total": len(historico),
        "mais_comuns": mais_comuns,
        "ultimas_frases": historico[-5:][::-1],
        "mais_recomendadas": mais_recomendadas
    }, response=response)


# ✅ LIMPAR HISTÓRICO
@router.post("/admin/limpar")
def limpar_historico(request: Request, senha: str = Form(...)):
    if senha != "admin":  # ⚠️ Em breve com banco
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

    return RedirectResponse(url="/admin/painel", status_code=status.HTTP_302_FOUND)


# 🔓 LOGOUT REAL
@router.get("/admin/logout")
def logout():
    response = RedirectResponse(url="/admin")
    remover_cookie_login(response)
    print("[LOGOUT] Cookie de sessão removido")
    return response
