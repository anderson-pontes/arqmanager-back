"""
Script para verificar a estrutura da tabela cliente
"""
import sys
sys.path.insert(0, '.')

from app.database import SessionLocal, engine
from sqlalchemy import inspect

# Criar sessão
db = SessionLocal()

# Inspecionar tabela
inspector = inspect(engine)

print("=" * 60)
print("ESTRUTURA DA TABELA 'cliente':")
print("=" * 60)

if 'cliente' in inspector.get_table_names():
    columns = inspector.get_columns('cliente')
    for col in columns:
        print(f"{col['name']:20} | {str(col['type']):15} | Nullable: {col['nullable']}")
    
    print("\n" + "=" * 60)
    print("PRIMEIRO CLIENTE NO BANCO:")
    print("=" * 60)
    
    from app.models.cliente import Cliente
    cliente = db.query(Cliente).first()
    
    if cliente:
        print(f"ID: {cliente.id}")
        print(f"Nome: {cliente.nome}")
        print(f"Email: {cliente.email}")
        print(f"Identificacao: {cliente.identificacao}")
        print(f"Tipo Pessoa: {cliente.tipo_pessoa}")
        print(f"Logradouro: {cliente.logradouro}")
        print(f"Cidade: {cliente.cidade}")
        print(f"UF: {cliente.uf}")
        print(f"CEP: {cliente.cep}")
        print(f"Indicado Por: {cliente.indicado_por}")
        
        # Verificar se tem escritorio_id
        if hasattr(cliente, 'escritorio_id'):
            print(f"Escritorio ID: {cliente.escritorio_id}")
        else:
            print("Escritorio ID: NÃO EXISTE")
    else:
        print("Nenhum cliente encontrado!")
else:
    print("Tabela 'cliente' não encontrada!")

db.close()
