#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para migrar dados PIX de colaboradores da tabela colaborador_escritorio (MySQL) 
para a tabela colaborador (PostgreSQL)
"""
import sys
import os
# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from datetime import datetime

# Configuração MySQL (ajuste conforme necessário)
MYSQL_URL = "mysql+pymysql://root:xpto1661WIN@localhost:3306/dbarqmanager"

def get_mysql_connection():
    """Cria conexão com MySQL"""
    try:
        engine = create_engine(MYSQL_URL)
        Session = sessionmaker(bind=engine)
        return Session(), engine
    except Exception as e:
        print(f"❌ Erro ao conectar no MySQL: {e}")
        print("\n💡 Configure a URL do MySQL no início do arquivo migrate_colaboradores_pix.py")
        sys.exit(1)

def get_postgres_connection():
    """Cria conexão com PostgreSQL"""
    try:
        engine = create_engine(settings.DATABASE_URL)
        Session = sessionmaker(bind=engine)
        return Session(), engine
    except Exception as e:
        print(f"❌ Erro ao conectar no PostgreSQL: {e}")
        sys.exit(1)

def migrate_pix_data(mysql_session, pg_session):
    """Migra dados PIX da tabela colaborador_escritorio para colaborador"""
    print("\n💰 Migrando dados PIX de Colaboradores...")
    
    # Buscar dados PIX do MySQL (pegar o primeiro registro de cada colaborador que tem PIX)
    result = mysql_session.execute(text("""
        SELECT 
            cod_colaborador,
            MAX(pix_tipo) as pix_tipo,
            MAX(pix_chave) as pix_chave
        FROM colaborador_escritorio
        WHERE (pix_tipo IS NOT NULL AND pix_tipo != '') 
           OR (pix_chave IS NOT NULL AND pix_chave != '')
        GROUP BY cod_colaborador
        ORDER BY cod_colaborador
    """))
    
    count = 0
    updated = 0
    skipped = 0
    errors = 0
    
    for row in result:
        try:
            cod_colaborador = row[0]
            pix_tipo = row[1] if row[1] else None
            pix_chave = row[2] if row[2] else None
            
            # Limpar dados
            if pix_tipo:
                pix_tipo = pix_tipo.strip()
            if pix_chave:
                pix_chave = pix_chave.strip()
            
            # Normalizar tipo PIX
            tipo_pix_normalizado = None
            if pix_tipo:
                tipo_lower = pix_tipo.lower()
                if 'cpf' in tipo_lower or 'cnpj' in tipo_lower:
                    if 'cpf' in tipo_lower and 'cnpj' in tipo_lower:
                        tipo_pix_normalizado = 'cpf'  # Usar CPF como padrão se ambos
                    elif 'cpf' in tipo_lower:
                        tipo_pix_normalizado = 'cpf'
                    elif 'cnpj' in tipo_lower:
                        tipo_pix_normalizado = 'cnpj'
                elif 'celular' in tipo_lower or 'telefone' in tipo_lower:
                    tipo_pix_normalizado = 'telefone'
                elif 'email' in tipo_lower:
                    tipo_pix_normalizado = 'email'
                elif 'aleatoria' in tipo_lower or 'aleatória' in tipo_lower:
                    tipo_pix_normalizado = 'aleatoria'
                else:
                    tipo_pix_normalizado = pix_tipo.lower()
            
            # Verificar se colaborador existe no PostgreSQL
            existing = pg_session.execute(
                text("SELECT id FROM colaborador WHERE id = :id"),
                {'id': cod_colaborador}
            ).first()
            
            if not existing:
                print(f"⏭️  Colaborador {cod_colaborador} não existe no PostgreSQL, pulando...")
                skipped += 1
                continue
            
            # Limpar chave PIX (remover formatação)
            if pix_chave:
                # Remover caracteres não alfanuméricos exceto @ e .
                if '@' in pix_chave or '.' in pix_chave:
                    # Provavelmente é email, manter como está
                    chave_pix_limpa = pix_chave
                else:
                    # Remover formatação (pontos, traços, parênteses, etc)
                    chave_pix_limpa = ''.join(filter(lambda x: x.isalnum() or x in ['@', '.', '-'], pix_chave))
            else:
                chave_pix_limpa = None
            
            # Atualizar colaborador no PostgreSQL
            pg_session.execute(text("""
                UPDATE colaborador
                SET tipo_pix = :tipo_pix,
                    chave_pix = :chave_pix,
                    updated_at = NOW()
                WHERE id = :id
            """), {
                'id': cod_colaborador,
                'tipo_pix': tipo_pix_normalizado,
                'chave_pix': chave_pix_limpa
            })
            
            updated += 1
            if updated % 10 == 0:
                print(f"  ✅ {updated} colaboradores atualizados...")
                pg_session.commit()
        
        except Exception as e:
            errors += 1
            pg_session.rollback()
            print(f"❌ Erro ao atualizar PIX do colaborador {row[0] if row else 'N/A'}: {e}")
            continue
    
    pg_session.commit()
    print(f"\n✅ Migração de PIX concluída!")
    print(f"   - {updated} colaboradores atualizados com dados PIX")
    print(f"   - {skipped} colaboradores ignorados (não existem no PostgreSQL)")
    print(f"   - {errors} erros")

def main():
    """Função principal"""
    print("=" * 60)
    print("💰 Migração de Dados PIX - MySQL → PostgreSQL")
    print("=" * 60)
    
    # Conectar aos bancos
    print("\n📡 Conectando aos bancos de dados...")
    mysql_session, _ = get_mysql_connection()
    pg_session, _ = get_postgres_connection()
    print("✅ Conexões estabelecidas")
    
    try:
        # Migrar dados PIX
        migrate_pix_data(mysql_session, pg_session)
        
        print("\n" + "=" * 60)
        print("✅ Migração finalizada com sucesso!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Erro durante migração: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    finally:
        mysql_session.close()
        pg_session.close()

if __name__ == "__main__":
    main()

