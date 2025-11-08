#!/usr/bin/env python3
"""
Script de migração de dados MySQL → PostgreSQL (Versão 2 - Melhorada)
Faz commit após cada registro para evitar perda de dados em caso de erro
"""
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from datetime import datetime

# Configuração MySQL
MYSQL_URL = "mysql+pymysql://root:xpto1661WIN@localhost:3306/dbarqmanager"

def get_mysql_connection():
    """Cria conexão com MySQL"""
    try:
        engine = create_engine(MYSQL_URL)
        return engine
    except Exception as e:
        print(f"❌ Erro ao conectar no MySQL: {e}")
        sys.exit(1)

def get_postgres_connection():
    """Cria conexão com PostgreSQL"""
    try:
        engine = create_engine(settings.DATABASE_URL)
        return engine
    except Exception as e:
        print(f"❌ Erro ao conectar no PostgreSQL: {e}")
        sys.exit(1)

def migrate_clientes(mysql_engine, pg_engine):
    """Migra tabela cliente"""
    print("\n👥 Migrando Clientes...")
    
    with mysql_engine.connect() as mysql_conn:
        result = mysql_conn.execute(text("""
            SELECT cod_cliente, nome, razao_social, email, identificacao, 
                   cod_tipo_pessoa, telefones, whatsapp, data_nascimento, ativo,
                   logradouro, numero, complemento, bairro, cidade, uf, cep,
                   inscricao_estadual, inscricao_municipal, indicado_por
            FROM cliente
            WHERE ativo = 1
        """))
        
        count = 0
        errors = 0
        
        for row in result:
            try:
                # Mapear cod_tipo_pessoa para tipo_pessoa (1=PF, 2=PJ)
                tipo_pessoa = 'PF' if row[5] == 1 else 'PJ' if row[5] == 2 else 'PF'
                
                with pg_engine.connect() as pg_conn:
                    pg_conn.execute(text("""
                        INSERT INTO cliente (
                            id, nome, razao_social, email, identificacao, tipo_pessoa,
                            telefone, whatsapp, data_nascimento, ativo,
                            logradouro, numero, complemento, bairro, cidade, uf, cep,
                            inscricao_estadual, inscricao_municipal, indicado_por,
                            created_at, updated_at
                        )
                        VALUES (
                            :id, :nome, :razao_social, :email, :identificacao, :tipo_pessoa,
                            :telefone, :whatsapp, :data_nascimento, :ativo,
                            :logradouro, :numero, :complemento, :bairro, :cidade, :uf, :cep,
                            :inscricao_estadual, :inscricao_municipal, :indicado_por,
                            NOW(), NOW()
                        )
                        ON CONFLICT (id) DO NOTHING
                    """), {
                        'id': row[0],
                        'nome': row[1],
                        'razao_social': row[2],
                        'email': row[3],
                        'identificacao': row[4],
                        'tipo_pessoa': tipo_pessoa,
                        'telefone': row[6],
                        'whatsapp': row[7],
                        'data_nascimento': row[8],
                        'ativo': bool(row[9]),
                        'logradouro': row[10],
                        'numero': row[11],
                        'complemento': row[12],
                        'bairro': row[13],
                        'cidade': row[14],
                        'uf': row[15],
                        'cep': row[16],
                        'inscricao_estadual': row[17],
                        'inscricao_municipal': row[18],
                        'indicado_por': row[19]
                    })
                    pg_conn.commit()
                count += 1
            except Exception as e:
                errors += 1
                if errors <= 5:  # Mostrar apenas os primeiros 5 erros
                    print(f"⚠️  Erro ao migrar cliente {row[0]}: {str(e)[:100]}")
        
        print(f"✅ {count} clientes migrados ({errors} erros)")

def migrate_propostas(mysql_engine, pg_engine):
    """Migra tabela proposta"""
    print("\n💰 Migrando Propostas...")
    
    with mysql_engine.connect() as mysql_conn:
        result = mysql_conn.execute(text("""
            SELECT cod_proposta, cod_cliente, cod_servico, cod_status,
                   nome, descricao, identificacao, numero_proposta, ano_proposta,
                   data_proposta, valor_proposta, valor_avista, valor_parcela_aprazo,
                   forma_pagamento, prazo, entrega_parcial, visitas_incluidas, observacao
            FROM proposta
        """))
        
        count = 0
        errors = 0
        
        for row in result:
            try:
                with pg_engine.connect() as pg_conn:
                    pg_conn.execute(text("""
                        INSERT INTO propostas (
                            id, cliente_id, servico_id, status_id,
                            nome, descricao, identificacao, numero_proposta, ano_proposta,
                            data_proposta, valor_proposta, valor_avista, valor_parcela_aprazo,
                            forma_pagamento, prazo, entrega_parcial, visitas_incluidas, observacao,
                            created_at, updated_at
                        )
                        VALUES (
                            :id, :cliente_id, :servico_id, :status_id,
                            :nome, :descricao, :identificacao, :numero_proposta, :ano_proposta,
                            :data_proposta, :valor_proposta, :valor_avista, :valor_parcela_aprazo,
                            :forma_pagamento, :prazo, :entrega_parcial, :visitas_incluidas, :observacao,
                            NOW(), NOW()
                        )
                        ON CONFLICT (id) DO NOTHING
                    """), {
                        'id': row[0],
                        'cliente_id': row[1],
                        'servico_id': row[2],
                        'status_id': row[3],
                        'nome': row[4],
                        'descricao': row[5],
                        'identificacao': row[6],
                        'numero_proposta': row[7],
                        'ano_proposta': row[8],
                        'data_proposta': row[9],
                        'valor_proposta': row[10],
                        'valor_avista': row[11],
                        'valor_parcela_aprazo': row[12],
                        'forma_pagamento': row[13],
                        'prazo': row[14],
                        'entrega_parcial': row[15] or 'Não',
                        'visitas_incluidas': row[16],
                        'observacao': row[17]
                    })
                    pg_conn.commit()
                count += 1
            except Exception as e:
                errors += 1
                if errors <= 5:
                    print(f"⚠️  Erro ao migrar proposta {row[0]}: {str(e)[:100]}")
        
        print(f"✅ {count} propostas migradas ({errors} erros)")

def migrate_projetos(mysql_engine, pg_engine):
    """Migra tabela projeto"""
    print("\n📁 Migrando Projetos...")
    
    with mysql_engine.connect() as mysql_conn:
        result = mysql_conn.execute(text("""
            SELECT cod_projeto, cod_cliente, cod_servico, cod_proposta, cod_status,
                   descricao, numero_projeto, ano_projeto,
                   data_inicio, data_previsao_fim, data_fim,
                   metragem, valor_contrato, saldo_contrato,
                   observacao, observacao_contrato, cod_contratado, ativo
            FROM projeto
            WHERE ativo = 1
        """))
        
        count = 0
        errors = 0
        
        for row in result:
            try:
                with pg_engine.connect() as pg_conn:
                    pg_conn.execute(text("""
                        INSERT INTO projetos (
                            id, cliente_id, servico_id, proposta_id, status_id,
                            descricao, numero_projeto, ano_projeto,
                            data_inicio, data_previsao_fim, data_fim,
                            metragem, valor_contrato, saldo_contrato,
                            observacao, observacao_contrato, cod_contratado, ativo,
                            created_at, updated_at
                        )
                        VALUES (
                            :id, :cliente_id, :servico_id, :proposta_id, :status_id,
                            :descricao, :numero_projeto, :ano_projeto,
                            :data_inicio, :data_previsao_fim, :data_fim,
                            :metragem, :valor_contrato, :saldo_contrato,
                            :observacao, :observacao_contrato, :cod_contratado, :ativo,
                            NOW(), NOW()
                        )
                        ON CONFLICT (id) DO NOTHING
                    """), {
                        'id': row[0],
                        'cliente_id': row[1],
                        'servico_id': row[2],
                        'proposta_id': row[3],
                        'status_id': row[4],
                        'descricao': row[5],
                        'numero_projeto': row[6],
                        'ano_projeto': row[7],
                        'data_inicio': row[8],
                        'data_previsao_fim': row[9],
                        'data_fim': row[10],
                        'metragem': row[11],
                        'valor_contrato': row[12],
                        'saldo_contrato': row[13],
                        'observacao': row[14],
                        'observacao_contrato': row[15],
                        'cod_contratado': row[16],
                        'ativo': bool(row[17])
                    })
                    pg_conn.commit()
                count += 1
            except Exception as e:
                errors += 1
                if errors <= 5:
                    print(f"⚠️  Erro ao migrar projeto {row[0]}: {str(e)[:100]}")
        
        print(f"✅ {count} projetos migrados ({errors} erros)")

def migrate_movimentos(mysql_engine, pg_engine, limit=None):
    """Migra tabela movimento"""
    print("\n💵 Migrando Movimentos Financeiros...")
    
    query = """
        SELECT cod_movimento, cod_despesa_receita_tipo, data_entrada,
               data_efetivacao, competencia, descricao, observacao,
               valor, valor_acrescido, valor_desconto, valor_resultante,
               comprovante, extensao, codigo_plano_contas, ativo, cod_projeto
        FROM movimento
        WHERE ativo = 1
    """
    if limit:
        query += f" LIMIT {limit}"
    
    with mysql_engine.connect() as mysql_conn:
        result = mysql_conn.execute(text(query))
        
        count = 0
        errors = 0
        
        for row in result:
            try:
                with pg_engine.connect() as pg_conn:
                    pg_conn.execute(text("""
                        INSERT INTO movimentos (
                            id, tipo, data_entrada, data_efetivacao, competencia,
                            descricao, observacao, valor, valor_acrescido, valor_desconto,
                            valor_resultante, comprovante, extensao, codigo_plano_contas,
                            ativo, projeto_id, created_at, updated_at
                        )
                        VALUES (
                            :id, :tipo, :data_entrada, :data_efetivacao, :competencia,
                            :descricao, :observacao, :valor, :valor_acrescido, :valor_desconto,
                            :valor_resultante, :comprovante, :extensao, :codigo_plano_contas,
                            :ativo, :projeto_id, NOW(), NOW()
                        )
                        ON CONFLICT (id) DO NOTHING
                    """), {
                        'id': row[0],
                        'tipo': row[1],
                        'data_entrada': row[2],
                        'data_efetivacao': row[3],
                        'competencia': row[4],
                        'descricao': row[5],
                        'observacao': row[6],
                        'valor': row[7],
                        'valor_acrescido': row[8],
                        'valor_desconto': row[9],
                        'valor_resultante': row[10],
                        'comprovante': row[11],
                        'extensao': row[12],
                        'codigo_plano_contas': row[13],
                        'ativo': bool(row[14]),
                        'projeto_id': row[15]
                    })
                    pg_conn.commit()
                count += 1
            except Exception as e:
                errors += 1
                if errors <= 5:
                    print(f"⚠️  Erro ao migrar movimento {row[0]}: {str(e)[:100]}")
        
        limit_msg = f" (limitado a {limit})" if limit else ""
        print(f"✅ {count} movimentos migrados{limit_msg} ({errors} erros)")

def main():
    """Função principal"""
    print("=" * 60)
    print("🔄 MIGRAÇÃO DE DADOS: MySQL → PostgreSQL (v2)")
    print("=" * 60)
    
    # Conectar nos bancos
    print("\n🔌 Conectando nos bancos de dados...")
    mysql_engine = get_mysql_connection()
    pg_engine = get_postgres_connection()
    print("✅ Conexões estabelecidas")
    
    try:
        # Executar migrações
        migrate_clientes(mysql_engine, pg_engine)
        migrate_propostas(mysql_engine, pg_engine)
        migrate_projetos(mysql_engine, pg_engine)
        migrate_movimentos(mysql_engine, pg_engine, limit=1000)
        
        print("\n" + "=" * 60)
        print("🎉 MIGRAÇÃO CONCLUÍDA!")
        print("=" * 60)
        print("\n💡 Execute 'python check_migrated_data.py' para verificar")
        
    except Exception as e:
        print(f"\n❌ Erro durante a migração: {e}")
    finally:
        mysql_engine.dispose()
        pg_engine.dispose()

if __name__ == "__main__":
    main()
