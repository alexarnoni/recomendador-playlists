from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


from api.rotas_publicas import router as rotas_publicas
from api.rotas_admin import router as rotas_admin

app = FastAPI()

app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")
templates = Jinja2Templates(directory="../frontend/templates")

# Registrar as rotas
app.include_router(rotas_publicas)
app.include_router(rotas_admin)

