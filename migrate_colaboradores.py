#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de migração de Colaboradores do MySQL para PostgreSQL
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
from app.core.security import get_password_hash
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
        print("\n💡 Configure a URL do MySQL no início do arquivo migrate_colaboradores.py")
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

def migrate_colaboradores(mysql_session, pg_session):
    """Migra tabela colaborador"""
    print("\n👥 Migrando Colaboradores...")
    
    # Buscar do MySQL
    result = mysql_session.execute(text("""
        SELECT 
            cod_colaborador,
            nome,
            email,
            cpf,
            telefone,
            data_nascimento,
            senha,
            foto,
            ultimo_acesso,
            ativo,
            inserido_por,
            alterado_por
        FROM colaborador
        ORDER BY cod_colaborador
    """))
    
    count = 0
    skipped = 0
    errors = 0
    
    for row in result:
        try:
            cod_colaborador = row[0]
            nome = row[1]
            email = row[2] if row[2] else None
            cpf = row[3] if row[3] else None
            telefone = row[4] if row[4] else None
            data_nascimento = row[5] if row[5] else None
            senha = row[6] if row[6] else None
            foto = row[7] if row[7] else None
            ultimo_acesso = row[8] if row[8] else None
            ativo = bool(row[9]) if row[9] is not None else True
            
            # Validar campos obrigatórios
            if not nome or not email or not cpf or not senha:
                print(f"⚠️  Colaborador {cod_colaborador} ({nome}) ignorado: campos obrigatórios faltando")
                skipped += 1
                continue
            
            # Limpar CPF (remover caracteres não numéricos)
            cpf_limpo = ''.join(filter(str.isdigit, cpf))
            if len(cpf_limpo) != 11:
                print(f"⚠️  Colaborador {cod_colaborador} ({nome}) ignorado: CPF inválido ({cpf})")
                skipped += 1
                continue
            
            # Truncar foto se muito grande (limite de 500 caracteres)
            if foto:
                if isinstance(foto, bytes):
                    # Se for bytes, converter para string e truncar
                    foto_str = foto.decode('utf-8', errors='ignore')
                else:
                    foto_str = str(foto)
                
                if len(foto_str) > 500:
                    # Foto muito grande, armazenar apenas referência
                    foto = f"Foto original muito grande ({len(foto_str)} chars)"
                    print(f"  ⚠️  Colaborador {cod_colaborador}: foto truncada (original: {len(foto_str)} chars)")
                else:
                    foto = foto_str
            else:
                foto = None
            
            # Verificar se já existe no PostgreSQL
            existing = pg_session.execute(
                text("SELECT id FROM colaborador WHERE id = :id OR email = :email OR cpf = :cpf"),
                {'id': cod_colaborador, 'email': email, 'cpf': cpf_limpo}
            ).first()
            
            if existing:
                print(f"⏭️  Colaborador {cod_colaborador} ({nome}) já existe, pulando...")
                skipped += 1
                continue
            
            # Determinar perfil (padrão: Colaborador)
            # No sistema PHP não há campo perfil explícito, usar padrão
            perfil = 'Colaborador'
            tipo = 'Geral'
            
            # Inserir no PostgreSQL
            pg_session.execute(text("""
                INSERT INTO colaborador (
                    id, nome, email, cpf, telefone, data_nascimento,
                    senha, foto, ultimo_acesso, ativo, perfil, tipo,
                    created_at, updated_at
                )
                VALUES (
                    :id, :nome, :email, :cpf, :telefone, :data_nascimento,
                    :senha, :foto, :ultimo_acesso, :ativo, :perfil, :tipo,
                    NOW(), NOW()
                )
            """), {
                'id': cod_colaborador,
                'nome': nome,
                'email': email,
                'cpf': cpf_limpo,
                'telefone': telefone,
                'data_nascimento': data_nascimento,
                'senha': senha,  # Senha já vem hasheada do MySQL
                'foto': foto,
                'ultimo_acesso': ultimo_acesso,
                'ativo': ativo,
                'perfil': perfil,
                'tipo': tipo
            })
            
            count += 1
            if count % 10 == 0:
                print(f"  ✅ {count} colaboradores migrados...")
                pg_session.commit()
        
        except Exception as e:
            errors += 1
            # Fazer rollback da transação em caso de erro
            pg_session.rollback()
            print(f"❌ Erro ao migrar colaborador {row[0] if row else 'N/A'}: {e}")
            continue
    
    pg_session.commit()
    print(f"\n✅ Migração concluída!")
    print(f"   - {count} colaboradores migrados")
    print(f"   - {skipped} colaboradores ignorados (já existem ou dados inválidos)")
    print(f"   - {errors} erros")
    
    # Corrigir sequence
    print("\n🔧 Corrigindo sequence...")
    pg_session.execute(text("""
        SELECT setval('colaborador_id_seq', 
            COALESCE((SELECT MAX(id) FROM colaborador), 1), true)
    """))
    pg_session.commit()
    print("✅ Sequence corrigida")

def main():
    """Função principal"""
    print("=" * 60)
    print("🚀 Migração de Colaboradores - MySQL → PostgreSQL")
    print("=" * 60)
    
    # Conectar aos bancos
    print("\n📡 Conectando aos bancos de dados...")
    mysql_session, _ = get_mysql_connection()
    pg_session, _ = get_postgres_connection()
    print("✅ Conexões estabelecidas")
    
    try:
        # Migrar colaboradores
        migrate_colaboradores(mysql_session, pg_session)
        
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

