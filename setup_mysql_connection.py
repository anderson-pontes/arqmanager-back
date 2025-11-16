"""Script interativo para configurar conexão MySQL"""
import sys
import getpass

def configure_mysql():
    """Configura conexão MySQL de forma interativa"""
    print("=" * 60)
    print("CONFIGURACAO DE CONEXAO MYSQL")
    print("=" * 60)
    print("\nPor favor, informe os dados de conexao do MySQL:\n")
    
    # Coletar informações
    host = input("Host (padrao: localhost): ").strip() or "localhost"
    port = input("Porta (padrao: 3306): ").strip() or "3306"
    database = input("Nome do banco (padrao: dbarqmanager): ").strip() or "dbarqmanager"
    user = input("Usuario MySQL: ").strip()
    
    if not user:
        print("ERRO: Usuario e obrigatorio!")
        sys.exit(1)
    
    password = getpass.getpass("Senha MySQL: ")
    
    # Construir URL
    mysql_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    
    print("\n" + "=" * 60)
    print("Testando conexao...")
    print("=" * 60)
    
    # Testar conexão
    try:
        from sqlalchemy import create_engine, text
        engine = create_engine(mysql_url)
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.scalar()
            print("OK: Conexao estabelecida com sucesso!")
            
            # Verificar se o banco tem as tabelas necessárias
            print("\nVerificando tabelas...")
            result = conn.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result]
            
            required_tables = ['servico', 'servico_etapa', 'servico_microservico']
            missing = [t for t in required_tables if t not in tables]
            
            if missing:
                print(f"AVISO: Tabelas nao encontradas: {', '.join(missing)}")
            else:
                print("OK: Todas as tabelas necessarias encontradas!")
            
            # Contar registros
            print("\nContagem de registros:")
            try:
                result = conn.execute(text("SELECT COUNT(*) FROM servico_microservico"))
                count = result.scalar()
                print(f"  - Tarefas (servico_microservico): {count} registros")
            except Exception as e:
                print(f"  - Erro ao contar tarefas: {e}")
            
    except Exception as e:
        print(f"ERRO: Falha ao conectar: {e}")
        print("\nVerifique:")
        print("  1. MySQL esta rodando")
        print("  2. Credenciais estao corretas")
        print("  3. Banco de dados existe")
        print("  4. Usuario tem permissoes")
        sys.exit(1)
    
    # Perguntar se quer salvar
    print("\n" + "=" * 60)
    save = input("Deseja salvar esta configuracao no migrate_data.py? (s/n): ").strip().lower()
    
    if save == 's':
        # Ler arquivo atual
        try:
            with open('migrate_data.py', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Substituir a linha MYSQL_URL
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('MYSQL_URL ='):
                    lines[i] = f'MYSQL_URL = "{mysql_url}"'
                    break
            
            # Salvar
            with open('migrate_data.py', 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
            
            print("OK: Configuracao salva em migrate_data.py")
            print(f"\nURL salva: mysql+pymysql://{user}:***@{host}:{port}/{database}")
            
        except Exception as e:
            print(f"ERRO ao salvar: {e}")
            print(f"\nConfigure manualmente no migrate_data.py:")
            print(f'MYSQL_URL = "{mysql_url}"')
    else:
        print("\nConfiguracao nao salva. Use esta URL no migrate_data.py:")
        print(f'MYSQL_URL = "{mysql_url}"')
    
    print("\n" + "=" * 60)
    print("Configuracao concluida!")
    print("=" * 60)

if __name__ == "__main__":
    configure_mysql()




