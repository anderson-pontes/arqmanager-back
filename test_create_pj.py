"""Script para testar criação de cliente Pessoa Jurídica"""
import sys
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.cliente import ClienteCreate
from app.services.cliente import ClienteService

def test_create_pj():
    """Testa criação de cliente PJ"""
    db = SessionLocal()
    
    try:
        # Dados de teste para Pessoa Jurídica
        cliente_data = ClienteCreate(
            nome="Empresa Teste LTDA",
            email="empresa@teste.com",
            telefone="(11) 98765-4321",
            cpf_cnpj="12.345.678/0001-90",
            tipo_pessoa="juridica",
            endereco="Rua Teste, 123",
            cidade="São Paulo",
            estado="SP",
            cep="01234-567",
            observacoes="Cliente teste",
            ativo=True
        )
        
        print("=" * 60)
        print("TESTANDO CRIAÇÃO DE CLIENTE PESSOA JURÍDICA")
        print("=" * 60)
        print(f"\nDados enviados:")
        print(f"  Nome: {cliente_data.nome}")
        print(f"  Email: {cliente_data.email}")
        print(f"  Telefone: {cliente_data.telefone}")
        print(f"  CNPJ: {cliente_data.cpf_cnpj}")
        print(f"  Tipo: {cliente_data.tipo_pessoa}")
        print(f"  Data Nascimento: {cliente_data.data_nascimento}")
        print(f"  Ativo: {cliente_data.ativo}")
        
        # Tentar criar
        service = ClienteService(db)
        result = service.create(cliente_data)
        
        print(f"\n✅ Cliente criado com sucesso!")
        print(f"  ID: {result.id}")
        print(f"  Nome: {result.nome}")
        print(f"  Tipo: {result.tipo_pessoa}")
        
    except Exception as e:
        print(f"\n❌ ERRO ao criar cliente:")
        print(f"  Tipo: {type(e).__name__}")
        print(f"  Mensagem: {str(e)}")
        import traceback
        print(f"\nTraceback completo:")
        traceback.print_exc()
        sys.exit(1)
        
    finally:
        db.close()

if __name__ == "__main__":
    test_create_pj()
