from app.database import Session
from app.models.usuarios import Usuario
from app.auth import hash_senha


def seed():
    db = Session()
    try:
        nome_usuario = "admin"
        email_usuario = "admin@teste.com"
        senha_usuario = "admin@123"
        perfil = "admin"

        existente = db.query(Usuario).filter_by(email=email_usuario).first()

        if not existente:
            usuario = Usuario(
                nome=nome_usuario,
                email=email_usuario,
                senha_hash=hash_senha(senha_usuario),
                role=perfil
            )
            db.add(usuario)
            db.commit()
            print(f"Usuário {nome_usuario} criado com sucesso!")
        else:
            print(f"Esse email já está cadastrado!")

    except Exception as erro:
        db.rollback()
        print(f"Erro: {erro}") 
    finally:
        db.close()



seed()