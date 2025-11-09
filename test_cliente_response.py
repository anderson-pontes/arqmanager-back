"""
Script para testar a resposta da API de clientes
"""
from app.database import SessionLocal
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteResponse

# Criar sessão
db = SessionLocal()

# Buscar primeiro cliente
cliente = db.query(Cliente).first()

if cliente:
    print("=" * 60)
    print("DADOS DO BANCO (Modelo SQLAlchemy):")
    print("=" * 60)
    print(f"ID: {cliente.id}")
    print(f"Nome: {cliente.nome}")
    print(f"Email: {cliente.email}")
    print(f"Telefone: {cliente.telefone}")
    print(f"Identificacao (CPF/CNPJ): {cliente.identificacao}")
    print(f"Tipo Pessoa: {cliente.tipo_pessoa}")
    print(f"Logradouro: {cliente.logradouro}")
    print(f"Cidade: {cliente.cidade}")
    print(f"UF: {cliente.uf}")
    print(f"CEP: {cliente.cep}")
    print(f"Indicado Por: {cliente.indicado_por}")
    print(f"Ativo: {cliente.ativo}")
    
    print("\n" + "=" * 60)
    print("RESPOSTA DA API (ClienteResponse):")
    print("=" * 60)
    
    # Converter para ClienteResponse
    response = ClienteResponse.from_orm(cliente)
    print(response.model_dump())
    
    print("\n" + "=" * 60)
    print("RESPOSTA JSON:")
    print("=" * 60)
    print(response.model_dump_json(indent=2))
else:
    print("Nenhum cliente encontrado no banco!")

db.close()
