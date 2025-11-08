"""
Script para criar migration inicial
Execute: python create_migration.py
"""
import sys
import os

# Adicionar diretório raiz ao path
sys.path.insert(0, os.path.dirname(__file__))

# Importar models para que o Alembic os detecte
from app.models.user import User, Escritorio
from app.database import Base

print("✅ Models importados com sucesso!")
print(f"📋 Tabelas detectadas: {list(Base.metadata.tables.keys())}")
print("\n🚀 Agora execute:")
print("   alembic revision --autogenerate -m 'Initial migration - users and escritorios'")
print("   alembic upgrade head")
