#!/usr/bin/env python3
"""
Script FINAL de migração com mapeamentos corretos das estruturas reais
"""
import sys
from sqlalchemy import create_engine, text
from app.core.config import settings

MYSQL_URL = "mysql+pymysql://root:xpto1661WIN@localhost:3306/dbarqmanager"

def migrate_with_map(mysql_engine, pg_engine, mysql_table, pg_table, column_map, where_clause=""):
    """Migra com mapeamento de colunas"""
    print(f"\n📋 Migrando {mysql_table}...")
    
    with mysql_engine.connect() as mysql_conn:
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
                data = {}
                for i, mysql_col in enumerate(mysql_cols):
                    pg_col = column_map[mysql_col]
                    value = row[i]
                    
                    # Converter tinyint para boolean
                    if pg_col in ['ativo', 'socio'] and value is not None:
                        value = bool(value)
                    
                    data[pg_col] = value
                
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
    print("🔄 MIGRAÇÃO FINAL COMPLETA - MySQL → PostgreSQL")
    print("=" * 70)
    
    mysql_engine = create_engine(MYSQL_URL)
    pg_engine = create_engine(settings.DATABASE_URL)
    
    migrations = [
        # 1. Escritório
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
        
        # 2. Colaborador Escritório
        {
            'mysql_table': 'colaborador_escritorio',
            'pg_table': 'colaborador_escritorio',
            'column_map': {
                'cod_colaborador': 'colaborador_id',
                'id_escritorio': 'escritorio_id',
                'tipo': 'tipo',
                'socio': 'socio',
                'pix_tipo': 'pix_tipo',
                'pix_chave': 'pix_chave',
            },
            'where': ''
        },
        
        # 3. Forma de Pagamento
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
        
        # 4. Projeto Pagamento
        {
            'mysql_table': 'projeto_pagamento',
            'pg_table': 'projeto_pagamento',
            'column_map': {
                'cod_projeto_pagamento': 'id',
                'cod_projeto': 'projeto_id',
                'cod_forma_pagamento': 'forma_pagamento_id',
                'valor': 'valor',
                'valor_recebido': 'valor_recebido',
                'data_previsao': 'data_prevista',
                'data_efetivacao': 'data_recebimento',
            },
            'where': ''
        },
        
        # 5. Proposta Serviço Etapa
        {
            'mysql_table': 'proposta_servico_etapa',
            'pg_table': 'proposta_servico_etapa',
            'column_map': {
                'cod_etapa': 'etapa_id',
                'cod_proposta': 'proposta_id',
                'prazo': 'prazo',
                'data_prevista': 'data_prevista',
                'data_conclusao': 'data_conclusao',
            },
            'where': ''
        },
        
        # 6. Conta Bancária
        {
            'mysql_table': 'conta_bancaria',
            'pg_table': 'conta_bancaria',
            'column_map': {
                'cod_conta_bancaria': 'id',
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
        
        # 7. Conta Movimentação
        {
            'mysql_table': 'conta_movimentacao',
            'pg_table': 'conta_movimentacao',
            'column_map': {
                'cod_conta_movimentacao': 'id',
                'cod_conta_bancaria': 'conta_bancaria_id',
                'data_movimentacao': 'data',
                'tipo': 'tipo',
                'valor_receita': 'valor',
                'cod_movimento': 'movimento_id',
            },
            'where': ''
        },
        
        # 8. Plano de Contas
        {
            'mysql_table': 'plano_contas',
            'pg_table': 'plano_contas',
            'column_map': {
                'cod_plano_contas': 'id',
                'codigo': 'codigo',
                'descricao': 'descricao',
                'id_escritorio': 'escritorio_id',
                'ativo': 'ativo',
            },
            'where': 'ativo = 1'
        },
        
        # 9. Feriados
        {
            'mysql_table': 'feriados',
            'pg_table': 'feriados',
            'column_map': {
                'id': 'id',
                'data': 'data',
                'feriado': 'descricao',
                'abrangencia': 'tipo',
            },
            'where': ''
        },
        
        # 10. Indicação
        {
            'mysql_table': 'indicacao',
            'pg_table': 'indicacao',
            'column_map': {
                'cod_indicacao': 'id',
                'descricao': 'nome',
                'ativo': 'ativo',
            },
            'where': 'ativo = 1'
        },
        
        # 11. Projeto Documento
        {
            'mysql_table': 'projeto_documento',
            'pg_table': 'projeto_documento',
            'column_map': {
                'cod_projeto_documento': 'id',
                'cod_projeto': 'projeto_id',
                'descricao': 'nome',
                'url': 'arquivo',
                'extensao': 'extensao',
            },
            'where': ''
        },
        
        # 12. Acesso Grupo
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
        
        # 13. Projeto Arquivamento
        {
            'mysql_table': 'projeto_arquivamento',
            'pg_table': 'projeto_arquivamento',
            'column_map': {
                'id_arquivamento': 'id',
                'cod_projeto': 'projeto_id',
                'data_acao': 'data_arquivamento',
                'motivo_acao': 'motivo',
            },
            'where': ''
        },
    ]
    
    total_migrated = 0
    total_errors = 0
    
    print("\n🚀 Iniciando migração de 13 tabelas...")
    
    for i, migration in enumerate(migrations, 1):
        print(f"\n[{i}/13] ", end='')
        try:
            count, errors = migrate_with_map(
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
    print("📊 RESUMO FINAL DA MIGRAÇÃO")
    print("=" * 70)
    print(f"\n✅ Total migrado: {total_migrated} registros")
    print(f"⚠️  Total de erros: {total_errors}")
    
    if total_migrated > 0:
        print("\n🎉 Migração concluída com sucesso!")
        print("\n📋 Dados migrados por tabela:")
        print("   - escritorio")
        print("   - colaborador_escritorio")
        print("   - forma_pagamento")
        print("   - projeto_pagamento")
        print("   - proposta_servico_etapa")
        print("   - conta_bancaria")
        print("   - conta_movimentacao")
        print("   - plano_contas")
        print("   - feriados")
        print("   - indicacao")
        print("   - projeto_documento")
        print("   - acesso_grupo")
        print("   - projeto_arquivamento")
        
        print("\n💡 Próximos passos:")
        print("   1. Criar views restantes:")
        print("      python create_remaining_views.py")
        print("\n   2. Verificar todos os dados:")
        print("      python check_migrated_data.py")
        print("\n   3. Testar views:")
        print("      python test_views.py")
        print("\n   4. Iniciar API:")
        print("      uvicorn app.main:app --reload")
        print("\n   5. Acessar documentação:")
        print("      http://localhost:8000/docs")
    
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
