#!/usr/bin/env python3
"""
Script para testar conexão com MySQL e verificar dados disponíveis
"""
from sqlalchemy import create_engine, text
import sys

# Configure aqui suas credenciais MySQL
MYSQL_URL = "mysql+pymysql://root:xpto1661WIN@localhost:3306/dbarqmanager"

def test_connection():
    """Testa conexão e lista tabelas disponíveis"""
    print("=" * 60)
    print("🔍 TESTE DE CONEXÃO MYSQL")
    print("=" * 60)
    
    try:
        print(f"\n🔌 Tentando conectar em: {MYSQL_URL.split('@')[1]}")
        engine = create_engine(MYSQL_URL)
        
        with engine.connect() as conn:
            print("✅ Conexão estabelecida com sucesso!\n")
            
            # Listar tabelas
            print("📋 Tabelas disponíveis:")
            result = conn.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result]
            for table in tables:
                print(f"   - {table}")
            
            print("\n📊 Contagem de registros ativos:")
            
            # Status
            try:
                result = conn.execute(text("SELECT COUNT(*) FROM status WHERE ativo = 1"))
                count = result.scalar()
                print(f"   ✅ Status: {count} registros")
            except Exception as e:
                print(f"   ⚠️  Status: {e}")
            
            # Clientes
            try:
                result = conn.execute(text("SELECT COUNT(*) FROM cliente WHERE ativo = 1"))
                count = result.scalar()
                print(f"   ✅ Clientes: {count} registros")
            except Exception as e:
                print(f"   ⚠️  Clientes: {e}")
            
            # Serviços
            try:
                result = conn.execute(text("SELECT COUNT(*) FROM servico WHERE ativo = 1"))
                count = result.scalar()
                print(f"   ✅ Serviços: {count} registros")
            except Exception as e:
                print(f"   ⚠️  Serviços: {e}")
            
            # Etapas
            try:
                result = conn.execute(text("SELECT COUNT(*) FROM servico_etapa"))
                count = result.scalar()
                print(f"   ✅ Etapas: {count} registros")
            except Exception as e:
                print(f"   ⚠️  Etapas: {e}")
            
            # Propostas
            try:
                result = conn.execute(text("SELECT COUNT(*) FROM proposta"))
                count = result.scalar()
                print(f"   ✅ Propostas: {count} registros")
            except Exception as e:
                print(f"   ⚠️  Propostas: {e}")
            
            # Projetos
            try:
                result = conn.execute(text("SELECT COUNT(*) FROM projeto WHERE ativo = 1"))
                count = result.scalar()
                print(f"   ✅ Projetos: {count} registros")
            except Exception as e:
                print(f"   ⚠️  Projetos: {e}")
            
            # Movimentos
            try:
                result = conn.execute(text("SELECT COUNT(*) FROM movimento WHERE ativo = 1"))
                count = result.scalar()
                print(f"   ✅ Movimentos: {count} registros")
            except Exception as e:
                print(f"   ⚠️  Movimentos: {e}")
            
            print("\n" + "=" * 60)
            print("✅ Teste concluído! Você pode executar a migração.")
            print("=" * 60)
            
    except Exception as e:
        print(f"\n❌ Erro ao conectar no MySQL:")
        print(f"   {e}")
        print("\n💡 Verifique:")
        print("   1. MySQL está rodando")
        print("   2. Credenciais estão corretas no arquivo")
        print("   3. Banco 'dbarqmanager' existe")
        print("   4. pymysql está instalado: pip install pymysql")
        sys.exit(1)

if __name__ == "__main__":
    test_connection()
