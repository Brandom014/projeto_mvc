from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from app.controllers import auth_controller


app = FastAPI(title="Sistema de Ponto de venda")

# Configuração para servir arquivos estáticos (CSS, JS, imagens)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configuração do Jinja2 para renderizar templates HTML
templates = Jinja2Templates(directory="app/templates")

# Incluir as rotas do controlador de autenticação
app.include_router(auth_controller.router)