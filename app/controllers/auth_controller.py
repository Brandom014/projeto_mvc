from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.usuarios import Usuario
from app.auth import hash_senha, verificar_senha, criar_token

router = APIRouter(prefix="/auth", tags=["Autenticação"])

templates = Jinja2Templates(directory="app/templates")


# Tela de cadastro
@router.get("/cadastro")
def tela_cadastro(request: Request):
    return templates.TemplateResponse(
        request,
        "auth/cadastro.html",
        {"request": request}
    )

@router.get("/login")
def tela_login(request: Request):
    return templates.TemplateResponse(
        request,
        "auth/login.html",
        {"request": request}
    )

@router.post("/cadastro")
def fazer_cadastro(
    request: Request,
    nome: str, 
    email: str, 
    senha: str, 
    db: Session = Depends(get_db)
):
    # Verificar se o email já existe
    usuario_existente = db.query(Usuario).filter(Usuario.email == email).first()

    if usuario_existente:
        return templates.TemplateResponse(
            request,
            "auth/cadastro.html",
            {"request": request, "mensagem": "Email já cadastrado!"}
        )
    
    # Criar novo usuário
    novo_usuario = Usuario(
        nome=nome,
        email=email,
        senha_hash=hash_senha(senha)
    )

    # Adicionar usuário ao banco de dados
    db.add(novo_usuario)
    db.commit()

    # Redirecionar para a página de login
    return RedirectResponse(url="/auth/login", status_code=302)