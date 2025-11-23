"""Script para verificar estrutura da tabela colaborador_escritorio no MySQL"""
from sqlalchemy import create_engine, text
from load_mysql_config import load_mysql_url

def check_mysql_colaborador_escritorio():
    """Verifica estrutura da tabela colaborador_escritorio no MySQL"""
    
    mysql_url = load_mysql_url()
    if not mysql_url:
        print("ERRO: Nao foi possivel carregar URL do MySQL")
        return
    
    engine = create_engine(mysql_url)
    
    with engine.connect() as conn:
        # Verificar se a tabela existe
        result = conn.execute(text("""
            SHOW TABLES LIKE 'colaborador_escritorio'
        """))
        
        if not result.first():
            print("Tabela colaborador_escritorio nao existe no MySQL")
            return
        
        # Verificar estrutura
        result = conn.execute(text("""
            DESCRIBE colaborador_escritorio
        """))
        
        print("Estrutura da tabela colaborador_escritorio:")
        for row in result:
            print(f"  {row[0]}: {row[1]} ({row[2]})")
        
        # Contar registros
        result = conn.execute(text("SELECT COUNT(*) FROM colaborador_escritorio"))
        total = result.scalar()
        print(f"\nTotal de registros: {total}")
        
        # Listar alguns registros
        if total > 0:
            # Primeiro, descobrir os nomes das colunas
            result = conn.execute(text("""
                SELECT * FROM colaborador_escritorio LIMIT 1
            """))
            
            if result.rowcount > 0:
                row = result.fetchone()
                print(f"\nPrimeiro registro (exemplo):")
                print(f"  {dict(row._mapping)}")

if __name__ == "__main__":
    check_mysql_colaborador_escritorio()






