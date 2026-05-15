# Instalar as bibliotecas


no terminal: 
```bash
pip install -r requirements.txt
```

# Inicializar o alembic

```bash
python -m alembic init migrations
```

# Editar o arquivo alembic init - na linha 89:
sqalchemy.url =

# gerar a migrations

no terminal:
```bash
python -m alembic revision --autogenerate -m "Criar tabela usuarios"
```

# aplicar a migration no banco
```bash
python -m alembic upgrade head
```

# Rodar o codigo
```bash
python -m uvicorn app.main:app --reload
```