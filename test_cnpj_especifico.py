"""Script para testar criação com CNPJ específico"""
import sys
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.cliente import ClienteCreate
from app.services.cliente import ClienteService

def test_create_with_cnpj():
    """Testa criação com CNPJ específico"""
    db = SessionLocal()
    
    try:
        # Dados de teste com o CNPJ fornecido
        cliente_data = ClienteCreate(
            nome="Empresa Teste CNPJ",
            email="teste.cnpj@empresa.com",
            telefone="(11) 98765-4321",
            cpf_cnpj="95.635.956/0001-76",
            tipo_pessoa="juridica",
            endereco="Rua Teste, 456",
            cidade="São Paulo",
            estado="SP",
            cep="01234-567",
            observacoes="Teste com CNPJ específico",
            ativo=True
        )
        
        print("=" * 60)
        print("TESTANDO CRIAÇÃO COM CNPJ: 95.635.956/0001-76")
        print("=" * 60)
        print(f"\nDados enviados:")
        for field, value in cliente_data.dict().items():
            print(f"  {field}: {value}")
        
        # Tentar criar
        service = ClienteService(db)
        result = service.create(cliente_data)
        
        print(f"\n✅ Cliente criado com sucesso!")
        print(f"  ID: {result.id}")
        print(f"  Nome: {result.nome}")
        print(f"  CNPJ: {result.cpf_cnpj}")
        print(f"  Tipo: {result.tipo_pessoa}")
        
    except Exception as e:
        print(f"\n❌ ERRO ao criar cliente:")
        print(f"  Tipo: {type(e).__name__}")
        print(f"  Mensagem: {str(e)}")
        import traceback
        print(f"\nTraceback completo:")
        traceback.print_exc()
        
        # Verificar se já existe
        print("\n🔍 Verificando se CNPJ já existe no banco...")
        from app.repositories.cliente import ClienteRepository
        repo = ClienteRepository(db)
        existing = repo.get_by_identificacao("95.635.956/0001-76")
        if existing:
            print(f"  ⚠️  CNPJ já cadastrado!")
            print(f"  ID: {existing.id}")
            print(f"  Nome: {existing.nome}")
            print(f"  Email: {existing.email}")
            print(f"  Ativo: {existing.ativo}")
        
    finally:
        db.close()

if __name__ == "__main__":
    test_create_with_cnpj()
