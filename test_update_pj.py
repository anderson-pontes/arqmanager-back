"""Script para testar atualização de cliente Pessoa Jurídica"""
import sys
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.cliente import ClienteUpdate
from app.services.cliente import ClienteService

def test_update_pj():
    """Testa atualização de cliente PJ"""
    db = SessionLocal()
    
    try:
        # ID do cliente criado anteriormente
        cliente_id = 232
        
        # Dados de atualização para Pessoa Jurídica
        update_data = ClienteUpdate(
            nome="Empresa Teste LTDA - Atualizada",
            email="empresa.atualizada@teste.com",
            telefone="(11) 98765-9999",
            cpf_cnpj="95.635.956/0001-76",
            tipo_pessoa="juridica",
            endereco="Rua Atualizada, 999",
            cidade="Rio de Janeiro",
            estado="RJ",
            cep="20000-000",
            observacoes="Cliente atualizado via teste",
            ativo=True
        )
        
        print("=" * 60)
        print(f"TESTANDO ATUALIZAÇÃO DE CLIENTE PJ (ID: {cliente_id})")
        print("=" * 60)
        print(f"\nDados enviados:")
        for field, value in update_data.dict(exclude_unset=True).items():
            print(f"  {field}: {value}")
        
        # Tentar atualizar
        service = ClienteService(db)
        result = service.update(cliente_id, update_data)
        
        print(f"\n✅ Cliente atualizado com sucesso!")
        print(f"  ID: {result.id}")
        print(f"  Nome: {result.nome}")
        print(f"  Email: {result.email}")
        print(f"  Tipo: {result.tipo_pessoa}")
        print(f"  Cidade: {result.cidade}")
        
    except Exception as e:
        print(f"\n❌ ERRO ao atualizar cliente:")
        print(f"  Tipo: {type(e).__name__}")
        print(f"  Mensagem: {str(e)}")
        import traceback
        print(f"\nTraceback completo:")
        traceback.print_exc()
        sys.exit(1)
        
    finally:
        db.close()

if __name__ == "__main__":
    test_update_pj()
