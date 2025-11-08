#!/usr/bin/env python3
"""
Script para migrar TODAS as tabelas restantes do MySQL para PostgreSQL
"""
import sys
from sqlalchemy import create_engine, text
from app.core.config import settings
from datetime import datetime

# Configuração MySQL
MYSQL_URL = "mysql+pymysql://root:xpto1661WIN@localhost:3306/dbarqmanager"

def get_connections():
    """Cria conexões com MySQL e PostgreSQL"""
    try:
        mysql_engine = create_engine(MYSQL_URL)
        pg_engine = create_engine(settings.DATABASE_URL)
        return mysql_engine, pg_engine
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        sys.exit(1)

def migrate_table(mysql_engine, pg_engine, table_name, columns_map, where_clause=""):
    """
    Migra uma tabela genérica
    
    Args:
        table_name: Nome da tabela
        columns_map: Dict com mapeamento {mysql_col: pg_col}
        where_clause: Cláusula WHERE opcional
    """
    print(f"\n📋 Migrando {table_name}...")
    
    # Construir SELECT
    mysql_cols = list(columns_map.keys())
    select_sql = f"SELECT {', '.join(mysql_cols)} FROM {table_name}"
    if where_clause:
        select_sql += f" WHERE {where_clause}"
    
    # Construir INSERT
    pg_cols = list(columns_map.values())
    placeholders = [f":{col}" for col in pg_cols]
    insert_sql = f"""
        INSERT INTO {table_name} ({', '.join(pg_cols)}, created_at, updated_at)
        VALUES ({', '.join(placeholders)}, NOW(), NOW())
        ON CONFLICT (id) DO NOTHING
    """
    
    count = 0
    errors = 0
    
    with mysql_engine.connect() as mysql_conn:
        result = mysql_conn.execute(text(select_sql))
        
        for row in result:
            try:
                # Criar dict de dados
                data = {pg_col: row[i] for i, pg_col in enumerate(pg_cols)}
                
                with pg_engine.connect() as pg_conn:
                    pg_conn.execute(text(insert_sql), data)
                    pg_conn.commit()
                count += 1
            except Exception as e:
                errors += 1
                if errors <= 3:
                    print(f"   ⚠️  Erro: {str(e)[:100]}")
    
    print(f"   ✅ {count} registros migrados ({errors} erros)")
    return count, errors

def main():
    """Função principal"""
    print("=" * 70)
    print("🔄 MIGRAÇÃO COMPLETA DE TABELAS - MySQL → PostgreSQL")
    print("=" * 70)
    
    mysql_engine, pg_engine = get_connections()
    
    total_migrated = 0
    total_errors = 0
    
    # FASE 1: TABELAS CRÍTICAS
    print("\n" + "=" * 70)
    print("FASE 1: TABELAS CRÍTICAS")
    print("=" * 70)
    
    # 1. Escritório
    count, errors = migrate_table(
        mysql_engine, pg_engine,
        'escritorio',
        {
            'id_escritorio': 'id',
            'nome': 'nome',
            'razao_social': 'razao_social',
            'cnpj': 'cnpj',
            'email': 'email',
            'telefone': 'telefone',
            'logradouro': 'logradouro',
            'numero': 'numero',
            'complemento': 'complemento',
            'bairro': 'bairro',
            'cidade': 'cidade',
            'uf': 'uf',
            'cep': 'cep',
            'ativo': 'ativo'
        }
    )
    total_migrated += count
    total_errors += errors
    
    # 2. Colaborador-Escritório
    count, errors = migrate_table(
        mysql_engine, pg_engine,
        'colaborador_escritorio',
        {
            'cod_colaborador_escritorio': 'id',
            'cod_colaborador': 'colaborador_id',
            'id_escritorio': 'escritorio_id',
            'tipo': 'tipo',
            'socio': 'socio',
            'pix_tipo': 'pix_tipo',
            'pix_chave': 'pix_chave'
        }
    )
    total_migrated += count
    total_errors += errors
    
    # 3. Projeto-Colaborador
    count, errors = migrate_table(
        mysql_engine, pg_engine,
        'projeto_colaborador',
        {
            'cod_projeto_colaborador': 'id',
            'cod_projeto': 'projeto_id',
            'cod_colaborador': 'colaborador_id',
            'funcao': 'funcao',
            'ativo': 'ativo'
        },
        where_clause="ativo = 1"
    )
    total_migrated += count
    total_errors += errors
    
    # 4. Projeto-Pagamento
    count, errors = migrate_table(
        mysql_engine, pg_engine,
        'projeto_pagamento',
        {
            'cod_projeto_pagamento': 'id',
            'cod_projeto': 'projeto_id',
            'cod_forma_pagamento': 'forma_pagamento_id',
            'valor': 'valor',
            'valor_recebido': 'valor_recebido',
            'data_prevista': 'data_prevista',
            'data_recebimento': 'data_recebimento',
            'observacao': 'observacao',
            'ativo': 'ativo'
        }
    )
    total_migrated += count
    total_errors += errors
    
    # 5. Proposta-Serviço-Etapa
    count, errors = migrate_table(
        mysql_engine, pg_engine,
        'proposta_servico_etapa',
        {
            'cod_proposta_servico_etapa': 'id',
            'cod_proposta': 'proposta_id',
            'cod_servico_etapa': 'etapa_id',
            'prazo': 'prazo',
            'data_prevista': 'data_prevista',
            'data_conclusao': 'data_conclusao',
            'observacao': 'observacao'
        }
    )
    total_migrated += count
    total_errors += errors
    
    # 6. Conta Bancária
    count, errors = migrate_table(
        mysql_engine, pg_engine,
        'conta_bancaria',
        {
            'cod_conta_bancaria': 'id',
            'nome': 'nome',
            'banco': 'banco',
            'agencia': 'agencia',
            'conta': 'conta',
            'tipo': 'tipo',
            'saldo_inicial': 'saldo_inicial',
            'id_escritorio': 'escritorio_id',
            'ativo': 'ativo'
        },
        where_clause="ativo = 1"
    )
    total_migrated += count
    total_errors += errors
    
    # 7. Conta Movimentação
    count, errors = migrate_table(
        mysql_engine, pg_engine,
        'conta_movimentacao',
        {
            'cod_conta_movimentacao': 'id',
            'cod_conta_bancaria': 'conta_bancaria_id',
            'data': 'data',
            'descricao': 'descricao',
            'valor': 'valor',
            'tipo': 'tipo',
            'saldo': 'saldo',
            'cod_movimento': 'movimento_id'
        }
    )
    total_migrated += count
    total_errors += errors
    
    # 8. Plano de Contas
    count, errors = migrate_table(
        mysql_engine, pg_engine,
        'plano_contas',
        {
            'cod_plano_contas': 'id',
            'codigo': 'codigo',
            'descricao': 'descricao',
            'tipo': 'tipo',
            'nivel': 'nivel',
            'cod_plano_contas_pai': 'plano_contas_pai_id',
            'id_escritorio': 'escritorio_id',
            'ativo': 'ativo'
        },
        where_clause="ativo = 1"
    )
    total_migrated += count
    total_errors += errors
    
    # FASE 2: TABELAS SECUNDÁRIAS
    print("\n" + "=" * 70)
    print("FASE 2: TABELAS SECUNDÁRIAS")
    print("=" * 70)
    
    # 9. Forma de Pagamento
    count, errors = migrate_table(
        mysql_engine, pg_engine,
        'forma_pagamento',
        {
            'cod_forma_pagamento': 'id',
            'descricao': 'descricao',
            'ativo': 'ativo'
        },
        where_clause="ativo = 1"
    )
    total_migrated += count
    total_errors += errors
    
    # 10. Feriados
    count, errors = migrate_table(
        mysql_engine, pg_engine,
        'feriados',
        {
            'cod_feriado': 'id',
            'data': 'data',
            'descricao': 'descricao',
            'tipo': 'tipo',
            'ativo': 'ativo'
        },
        where_clause="ativo = 1"
    )
    total_migrated += count
    total_errors += errors
    
    # 11. Indicação
    count, errors = migrate_table(
        mysql_engine, pg_engine,
        'indicacao',
        {
            'cod_indicacao': 'id',
            'nome': 'nome',
            'telefone': 'telefone',
            'email': 'email',
            'observacao': 'observacao',
            'ativo': 'ativo'
        },
        where_clause="ativo = 1"
    )
    total_migrated += count
    total_errors += errors
    
    # 12. Projeto Documento
    count, errors = migrate_table(
        mysql_engine, pg_engine,
        'projeto_documento',
        {
            'cod_projeto_documento': 'id',
            'cod_projeto': 'projeto_id',
            'cod_arquivo_tipo': 'tipo_documento_id',
            'nome': 'nome',
            'arquivo': 'arquivo',
            'extensao': 'extensao',
            'observacao': 'observacao',
            'ativo': 'ativo'
        },
        where_clause="ativo = 1"
    )
    total_migrated += count
    total_errors += errors
    
    # 13. Acesso Grupo
    count, errors = migrate_table(
        mysql_engine, pg_engine,
        'acesso_grupo',
        {
            'cod_grupo': 'id',
            'descricao': 'descricao',
            'ativo': 'ativo'
        },
        where_clause="ativo = 1"
    )
    total_migrated += count
    total_errors += errors
    
    # RESUMO
    print("\n" + "=" * 70)
    print("📊 RESUMO DA MIGRAÇÃO")
    print("=" * 70)
    print(f"\n✅ Total migrado: {total_migrated} registros")
    print(f"⚠️  Total de erros: {total_errors}")
    print(f"\n🎉 Migração concluída!")
    print("\n💡 Execute 'python check_migrated_data.py' para verificar")
    
    mysql_engine.dispose()
    pg_engine.dispose()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Migração cancelada pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
