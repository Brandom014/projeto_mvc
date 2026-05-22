from fastapi import APIRouter, Request, Depends, HTTPException, status, Form
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
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
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
    return RedirectResponse(
        url="/auth/login?cadastro=ok",
        status_code=302)


@router.post("/login")
def fazer_login(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db)
):  
    # 1. Busca o usuário pelo email no db
    usuario = db.query(Usuario).filter(Usuario.email == email).first()

    # 2. Verificar a senha com bcrypt
    senha_correta = (
        usuario is not None and verificar_senha(senha, usuario.senha_hash)
    )

    if not senha_correta:
        return templates.TemplateResponse(
            request,
            "auth/login.html",
            {
                "request": request, 
                "erro": "Email ou senha incorretos!"}
        )
    
    if not usuario.ativo:
        return templates.TemplateResponse(
            request,
            "auth/login.html",
            {
                "request": request, 
                "erro": "Usuário inativo! Contate o administrador."}
        )
    

    # 3. Gera o token JWT
    token_data = {
        "sub": usuario.email,
        "nome": usuario.nome,
        "role": usuario.role,
        "id": usuario.id
    }

    token = criar_token(token_data)
    # 4. Salva o token no cookie e redireciona para a página home

    response = RedirectResponse(url="/", status_code=302)

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age= 3600, # 1 hora
        samesite="lax"
    )

    return response


@router.get("/logout")
def sair():
    response = RedirectResponse(url="/auth/login", status_code=302)
    response.delete_cookie(key="access_token")
    return response