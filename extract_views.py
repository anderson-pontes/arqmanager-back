#!/usr/bin/env python3
"""
Script para extrair definições de views do MySQL
"""
from sqlalchemy import create_engine, text
import re

MYSQL_URL = "mysql+pymysql://root:xpto1661WIN@localhost:3306/dbarqmanager"

def extract_view_definition(conn, view_name):
    """Extrai a definição SQL de uma view"""
    try:
        result = conn.execute(text(f"SHOW CREATE VIEW {view_name}"))
        row = result.fetchone()
        if row:
            return row[1]  # A definição SQL está na segunda coluna
    except Exception as e:
        print(f"⚠️  Erro ao extrair {view_name}: {e}")
    return None

def main():
    engine = create_engine(MYSQL_URL)
    
    # Views mais importantes para migrar
    important_views = [
        'v_cliente',
        'v_projeto',
        'v_proposta',
        'v_movimento',
        'v_colaborador',
        'v_servico_etapa',
        'v_financeiro_projeto'
    ]
    
    print("=" * 60)
    print("📋 EXTRAINDO DEFINIÇÕES DE VIEWS")
    print("=" * 60)
    
    with engine.connect() as conn:
        for view_name in important_views:
            print(f"\n{'='*60}")
            print(f"VIEW: {view_name}")
            print('='*60)
            
            definition = extract_view_definition(conn, view_name)
            if definition:
                # Limpar a definição
                definition = definition.replace('`', '')
                definition = re.sub(r'DEFINER=.*?SQL SECURITY DEFINER ', '', definition)
                print(definition[:500])  # Mostrar primeiros 500 caracteres
                print("...")
            else:
                print("❌ Não foi possível extrair")
    
    print("\n" + "=" * 60)
    print("💡 OBSERVAÇÕES:")
    print("=" * 60)
    print("1. Views do MySQL usam sintaxe específica")
    print("2. Precisam ser adaptadas para PostgreSQL")
    print("3. Algumas views podem não ser necessárias no novo sistema")
    print("4. Recomenda-se recriar views conforme necessidade")
    print("\n📝 Para o novo sistema FastAPI:")
    print("   - Use queries diretas nos repositories")
    print("   - Ou crie views PostgreSQL quando necessário")

if __name__ == "__main__":
    main()
