"""Script para verificar colaboradores no MySQL"""
from sqlalchemy import create_engine, text
from load_mysql_config import load_mysql_url

def check_mysql_colaboradores():
    """Verifica colaboradores no MySQL"""
    
    mysql_url = load_mysql_url()
    if not mysql_url:
        print("ERRO: Nao foi possivel carregar URL do MySQL")
        return
    
    engine = create_engine(mysql_url)
    
    with engine.connect() as conn:
        # Contar colaboradores no MySQL
        result = conn.execute(text("SELECT COUNT(*) FROM colaborador"))
        total = result.scalar()
        print(f"Total de colaboradores no MySQL: {total}")
        
        # Verificar estrutura da tabela
        result = conn.execute(text("""
            DESCRIBE colaborador
        """))
        
        print("\nEstrutura da tabela colaborador:")
        for row in result:
            print(f"  {row[0]}: {row[1]} ({row[2]})")
        
        # Listar alguns colaboradores
        if total > 0:
            print("\nPrimeiros 10 colaboradores:")
            result = conn.execute(text("""
                SELECT cod_colaborador, nome, email, cpf, ativo
                FROM colaborador
                ORDER BY cod_colaborador
                LIMIT 10
            """))
            
            for row in result:
                colab_id = row[0]
                nome = row[1] or ''
                email = row[2] or ''
                cpf = row[3] or ''
                ativo = row[4]
                print(f"  Colaborador {colab_id}: {nome} ({email}) - CPF: {cpf} - Ativo: {ativo}")
        
        # Verificar tabela de relacionamento colaborador_escritorio
        try:
            result = conn.execute(text("SELECT COUNT(*) FROM colaborador_escritorio"))
            total_rel = result.scalar()
            print(f"\nTotal de relacionamentos colaborador_escritorio: {total_rel}")
            
            if total_rel > 0:
                print("\nPrimeiros 10 relacionamentos:")
                result = conn.execute(text("""
                    SELECT colaborador_id, escritorio_id, perfil, ativo
                    FROM colaborador_escritorio
                    ORDER BY colaborador_id
                    LIMIT 10
                """))
                
                for row in result:
                    colab_id = row[0]
                    esc_id = row[1]
                    perfil = row[2] or ''
                    ativo = row[3]
                    print(f"  Colaborador {colab_id} -> Escritorio {esc_id} (Perfil: {perfil}, Ativo: {ativo})")
        except Exception as e:
            print(f"\nTabela colaborador_escritorio nao encontrada ou erro: {e}")

if __name__ == "__main__":
    check_mysql_colaboradores()

