"""Script para testar atualização de PJ com data_nascimento vazia"""
import sys
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.cliente import ClienteUpdate
from app.services.cliente import ClienteService

def test_update_with_empty_date():
    """Testa atualização com data_nascimento como string vazia"""
    db = SessionLocal()
    
    try:
        cliente_id = 232
        
        # Simular dados do frontend com data_nascimento vazia
        raw_data = {
            "nome": "Empresa Frontend Test",
            "email": "frontend@test.com",
            "telefone": "(11) 99999-9999",
            "cpf_cnpj": "95.635.956/0001-76",
            "tipo_pessoa": "juridica",
            "data_nascimento": "",  # String vazia como vem do frontend
            "endereco": "Rua Frontend, 123",
            "cidade": "São Paulo",
            "estado": "SP",
            "cep": "01000-000",
            "observacoes": "Teste frontend",
            "ativo": True
        }
        
        print("=" * 60)
        print(f"TESTANDO UPDATE COM DATA VAZIA (ID: {cliente_id})")
        print("=" * 60)
        print(f"\nDados RAW (como vem do frontend):")
        for field, value in raw_data.items():
            print(f"  {field}: {repr(value)}")
        
        # Criar schema (vai validar)
        update_data = ClienteUpdate(**raw_data)
        
        print(f"\nDados APÓS validação:")
        for field, value in update_data.dict(exclude_unset=True).items():
            print(f"  {field}: {repr(value)}")
        
        # Tentar atualizar
        service = ClienteService(db)
        result = service.update(cliente_id, update_data)
        
        print(f"\n✅ Cliente atualizado com sucesso!")
        print(f"  ID: {result.id}")
        print(f"  Nome: {result.nome}")
        print(f"  Data Nascimento: {result.data_nascimento}")
        
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
    test_update_with_empty_date()
