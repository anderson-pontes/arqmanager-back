#!/usr/bin/env python3
"""
Script inteligente que mapeia automaticamente colunas MySQL → PostgreSQL
"""
import sys
from sqlalchemy import create_engine, text
from app.core.config import settings

MYSQL_URL = "mysql+pymysql://root:xpto1661WIN@localhost:3306/dbarqmanager"

def get_table_columns(conn, table_name):
    """Obtém colunas de uma tabela"""
    result = conn.execute(text(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}' AND table_schema = DATABASE() ORDER BY ordinal_position"))
    return [row[0] for row in result]

def smart_migrate(mysql_engine, pg_engine, mysql_table, pg_table, column_map, where_clause=""):
    """
    Migra com mapeamento inteligente de colunas
    
    column_map: dict {mysql_col: pg_col}
    """
    print(f"\n📋 Migrando {mysql_table} → {pg_table}...")
    
    with mysql_engine.connect() as mysql_conn:
        # Construir SELECT com colunas do MySQL
        mysql_cols = list(column_map.keys())
        select_sql = f"SELECT {', '.join(mysql_cols)} FROM {mysql_table}"
        if where_clause:
            select_sql += f" WHERE {where_clause}"
        
        try:
            result = mysql_conn.execute(text(select_sql))
        except Exception as e:
            print(f"   ❌ Erro ao ler: {str(e)[:100]}")
            return 0, 0
        
        count = 0
        errors = 0
        
        for row in result:
            try:
                # Mapear dados MySQL → PostgreSQL
                data = {}
                for i, mysql_col in enumerate(mysql_cols):
                    pg_col = column_map[mysql_col]
                    data[pg_col] = row[i]
                
                # Construir INSERT com colunas do PostgreSQL
                pg_cols = list(data.keys())
                cols_str = ', '.join(pg_cols)
                placeholders = ', '.join([f":{col}" for col in pg_cols])
                
                insert_sql = f"""
                    INSERT INTO {pg_table} ({cols_str}, created_at, updated_at)
                    VALUES ({placeholders}, NOW(), NOW())
                    ON CONFLICT (id) DO NOTHING
                """
                
                with pg_engine.connect() as pg_conn:
                    pg_conn.execute(text(insert_sql), data)
                    pg_conn.commit()
                count += 1
                
                if count % 100 == 0:
                    print(f"   ⏳ {count} registros...")
                    
            except Exception as e:
                errors += 1
                if errors <= 3:
                    print(f"   ⚠️  Erro: {str(e)[:100]}")
        
        print(f"   ✅ {count} registros migrados ({errors} erros)")
        return count, errors

def main():
    """Função principal"""
    print("=" * 70)
    print("🔄 MIGRAÇÃO INTELIGENTE - MySQL → PostgreSQL")
    print("=" * 70)
    
    mysql_engine = create_engine(MYSQL_URL)
    pg_engine = create_engine(settings.DATABASE_URL)
    
    # Mapeamentos de colunas
    migrations = [
        {
            'mysql_table': 'escritorio',
            'pg_table': 'escritorio',
            'column_map': {
                'id_escritorio': 'id',
                'nome_fantasia': 'nome',
                'razao_social': 'razao_social',
                'documento': 'cnpj',
                'email': 'email',
                'fone': 'telefone',
                'endereco_completo': 'logradouro',
                'uf': 'uf',
                'cidade': 'cidade',
            },
            'where': ''
        },
        {
            'mysql_table': 'colaborador_escritorio',
            'pg_table': 'colaborador_escritorio',
            'column_map': {
                'cod_colaborador_escritorio': 'id',
                'cod_colaborador': 'colaborador_id',
                'id_escritorio': 'escritorio_id',
                'tipo': 'tipo',
                'socio': 'socio',
                'pix_tipo': 'pix_tipo',
                'pix_chave': 'pix_chave',
            },
            'where': ''
        },
        {
            'mysql_table': 'forma_pagamento',
            'pg_table': 'forma_pagamento',
            'column_map': {
                'cod_forma_pagamento': 'id',
                'descricao': 'descricao',
                'ativo': 'ativo',
            },
            'where': 'ativo = 1'
        },
        {
            'mysql_table': 'projeto_pagamento',
            'pg_table': 'projeto_pagamento',
            'column_map': {
                'cod_projeto_pagamento': 'id',
                'cod_projeto': 'projeto_id',
                'cod_forma_pagamento': 'forma_pagamento_id',
                'valor': 'valor',
                'valor_recebido': 'valor_recebido',
                'data_prevista': 'data_prevista',
                'data_recebimento': 'data_recebimento',
                'observacao': 'observacao',
                'ativo': 'ativo',
            },
            'where': ''
        },
        {
            'mysql_table': 'proposta_servico_etapa',
            'pg_table': 'proposta_servico_etapa',
            'column_map': {
                'cod_proposta_servico_etapa': 'id',
                'cod_proposta': 'proposta_id',
                'cod_etapa': 'etapa_id',
                'prazo': 'prazo',
                'data_prevista': 'data_prevista',
                'data_conclusao': 'data_conclusao',
                'observacao': 'observacao',
            },
            'where': ''
        },
        {
            'mysql_table': 'conta_bancaria',
            'pg_table': 'conta_bancaria',
            'column_map': {
                'cod_conta_bancaria': 'id',
                'nome': 'nome',
                'banco': 'banco',
                'agencia': 'agencia',
                'conta': 'conta',
                'tipo': 'tipo',
                'saldo_inicial': 'saldo_inicial',
                'id_escritorio': 'escritorio_id',
                'ativo': 'ativo',
            },
            'where': 'ativo = 1'
        },
        {
            'mysql_table': 'conta_movimentacao',
            'pg_table': 'conta_movimentacao',
            'column_map': {
                'cod_conta_movimentacao': 'id',
                'cod_conta_bancaria': 'conta_bancaria_id',
                'data': 'data',
                'descricao': 'descricao',
                'valor': 'valor',
                'tipo': 'tipo',
                'saldo': 'saldo',
                'cod_movimento': 'movimento_id',
            },
            'where': ''
        },
        {
            'mysql_table': 'plano_contas',
            'pg_table': 'plano_contas',
            'column_map': {
                'cod_plano_contas': 'id',
                'codigo': 'codigo',
                'descricao': 'descricao',
                'tipo': 'tipo',
                'nivel': 'nivel',
                'cod_plano_contas_pai': 'plano_contas_pai_id',
                'id_escritorio': 'escritorio_id',
                'ativo': 'ativo',
            },
            'where': 'ativo = 1'
        },
        {
            'mysql_table': 'feriados',
            'pg_table': 'feriados',
            'column_map': {
                'id': 'id',
                'data': 'data',
                'descricao': 'descricao',
                'tipo': 'tipo',
            },
            'where': ''
        },
        {
            'mysql_table': 'indicacao',
            'pg_table': 'indicacao',
            'column_map': {
                'cod_indicacao': 'id',
                'nome': 'nome',
                'telefone': 'telefone',
                'email': 'email',
            },
            'where': ''
        },
        {
            'mysql_table': 'acesso_grupo',
            'pg_table': 'acesso_grupo',
            'column_map': {
                'id_grupo': 'id',
                'descricao': 'descricao',
                'ativo': 'ativo',
            },
            'where': 'ativo = 1'
        },
    ]
    
    total_migrated = 0
    total_errors = 0
    
    for migration in migrations:
        try:
            count, errors = smart_migrate(
                mysql_engine, pg_engine,
                migration['mysql_table'],
                migration['pg_table'],
                migration['column_map'],
                migration.get('where', '')
            )
            total_migrated += count
            total_errors += errors
        except Exception as e:
            print(f"   ❌ Erro fatal: {str(e)[:150]}")
            total_errors += 1
    
    print("\n" + "=" * 70)
    print("📊 RESUMO FINAL")
    print("=" * 70)
    print(f"\n✅ Total migrado: {total_migrated} registros")
    print(f"⚠️  Total de erros: {total_errors}")
    
    if total_migrated > 0:
        print("\n🎉 Migração concluída!")
        print("\n💡 Próximos passos:")
        print("   1. Criar views: python create_remaining_views.py")
        print("   2. Verificar: python check_migrated_data.py")
        print("   3. Testar API: uvicorn app.main:app --reload")
    
    mysql_engine.dispose()
    pg_engine.dispose()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Migração cancelada.")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
