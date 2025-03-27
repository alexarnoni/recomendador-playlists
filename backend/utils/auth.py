from fastapi import Request
from fastapi.responses import RedirectResponse, Response

# Nome padrão do cookie de login
COOKIE_NAME = "admin_logged"

# ✅ Cria cookie após login bem-sucedido
def criar_cookie_login(response: Response):
    response.set_cookie(
        key=COOKIE_NAME,
        value="true",
        httponly=True,
        max_age=3600,  # expira em 1 hora
        samesite="Lax",
        path="/"
    )

# ✅ Remove o cookie (logout)
def remover_cookie_login(response: Response):
    response.delete_cookie(COOKIE_NAME)

# ✅ Verifica se o usuário está logado
def esta_logado(request: Request) -> bool:
    return request.cookies.get(COOKIE_NAME, "").lower() == "true"

# ✅ Redireciona se não estiver logado
def redirecionar_se_nao_logado(request: Request):
    if not esta_logado(request):
        print("[🔒 BLOQUEIO] Tentativa de acesso sem login")
        return RedirectResponse(url="/admin", status_code=302)
