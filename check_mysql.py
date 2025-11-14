#!/usr/bin/env python3
"""
Script para testar conexão com MySQL e verificar dados disponíveis
"""
from sqlalchemy import create_engine, text
import sys

# Configure aqui suas credenciais MySQL (ou use .mysql_config)
# O script tentará carregar de múltiplas fontes
try:
    from load_mysql_config import load_mysql_url
    MYSQL_URL = load_mysql_url() or "mysql+pymysql://root:xpto1661WIN@localhost:3306/dbarqmanager"
except:
    MYSQL_URL = "mysql+pymysql://root:xpto1661WIN@localhost:3306/dbarqmanager"

def test_connection():
    """Testa conexão e lista tabelas disponíveis"""
    print("=" * 60)
    print("TESTE DE CONEXAO MYSQL")
    print("=" * 60)
    
    # Carregar URL do MySQL
    from load_mysql_config import load_mysql_url
    mysql_url = load_mysql_url() or MYSQL_URL
    
    try:
        host_info = mysql_url.split('@')[1] if '@' in mysql_url else mysql_url
        print(f"\nTentando conectar em: {host_info}")
        engine = create_engine(mysql_url)
        
        with engine.connect() as conn:
            print("OK: Conexao estabelecida com sucesso!\n")
            
            # Listar tabelas
            print("Tabelas disponiveis:")
            result = conn.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result]
            for table in tables:
                print(f"   - {table}")
            
            print("\nContagem de registros:")
            
            # Status
            try:
                result = conn.execute(text("SELECT COUNT(*) FROM status WHERE ativo = 1"))
                count = result.scalar()
                print(f"   OK Status: {count} registros")
            except Exception as e:
                print(f"   AVISO Status: {e}")
            
            # Clientes
            try:
                result = conn.execute(text("SELECT COUNT(*) FROM cliente WHERE ativo = 1"))
                count = result.scalar()
                print(f"   OK Clientes: {count} registros")
            except Exception as e:
                print(f"   AVISO Clientes: {e}")
            
            # Serviços
            try:
                result = conn.execute(text("SELECT COUNT(*) FROM servico WHERE ativo = 1"))
                count = result.scalar()
                print(f"   OK Servicos: {count} registros")
            except Exception as e:
                print(f"   AVISO Servicos: {e}")
            
            # Etapas
            try:
                result = conn.execute(text("SELECT COUNT(*) FROM servico_etapa"))
                count = result.scalar()
                print(f"   OK Etapas: {count} registros")
            except Exception as e:
                print(f"   AVISO Etapas: {e}")
            
            # Tarefas (Microserviços)
            try:
                result = conn.execute(text("SELECT COUNT(*) FROM servico_microservico"))
                count = result.scalar()
                print(f"   OK Tarefas (servico_microservico): {count} registros")
            except Exception as e:
                print(f"   AVISO Tarefas: {e}")
            
            # Propostas
            try:
                result = conn.execute(text("SELECT COUNT(*) FROM proposta"))
                count = result.scalar()
                print(f"   OK Propostas: {count} registros")
            except Exception as e:
                print(f"   AVISO Propostas: {e}")
            
            # Projetos
            try:
                result = conn.execute(text("SELECT COUNT(*) FROM projeto WHERE ativo = 1"))
                count = result.scalar()
                print(f"   OK Projetos: {count} registros")
            except Exception as e:
                print(f"   AVISO Projetos: {e}")
            
            # Movimentos
            try:
                result = conn.execute(text("SELECT COUNT(*) FROM movimento WHERE ativo = 1"))
                count = result.scalar()
                print(f"   OK Movimentos: {count} registros")
            except Exception as e:
                print(f"   AVISO Movimentos: {e}")
            
            print("\n" + "=" * 60)
            print("OK: Teste concluido! Voce pode executar a migracao.")
            print("=" * 60)
            
    except Exception as e:
        print(f"\nERRO ao conectar no MySQL:")
        print(f"   {e}")
        print("\nVerifique:")
        print("   1. MySQL esta rodando")
        print("   2. Credenciais estao corretas")
        print("   3. Banco 'dbarqmanager' existe")
        print("   4. pymysql esta instalado: pip install pymysql")
        print("\nConfigure a conexao em:")
        print("   - Arquivo .mysql_config")
        print("   - Variavel de ambiente MYSQL_URL")
        print("   - Ou edite migrate_data.py linha 38")
        sys.exit(1)

if __name__ == "__main__":
    test_connection()
