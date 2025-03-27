# backend/criar_tabelas.py
from db import Base, engine
from models.usuario import Usuario

Base.metadata.create_all(bind=engine)
