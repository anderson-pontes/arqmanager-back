#!/usr/bin/env python3
"""
Script principal de migração de dados MySQL → PostgreSQL
"""
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models import Base
from datetime import datetime

# Configuração MySQL (ajuste conforme necessário)
# Pode ser configurado via:
# 1. Variável de ambiente MYSQL_URL
# 2. Arquivo .mysql_config
# 3. Editar diretamente esta linha

import os
from pathlib import Path

def get_mysql_url():
    """Carrega URL do MySQL de múltiplas fontes"""
    # 1. Variável de ambiente
    mysql_url = os.getenv('MYSQL_URL')
    if mysql_url:
        return mysql_url
    
    # 2. Arquivo .mysql_config
    config_file = Path(__file__).parent / '.mysql_config'
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and line.startswith('MYSQL_URL='):
                    return line.split('=', 1)[1].strip()
    
    # 3. Valor padrão (edite aqui se necessário)
    return "mysql+pymysql://root:xpto1661WIN@localhost:3306/dbarqmanager"

MYSQL_URL = get_mysql_url()

def get_mysql_connection():
    """Cria conexão com MySQL"""
    try:
        engine = create_engine(MYSQL_URL)
        Session = sessionmaker(bind=engine)
        return Session(), engine
    except Exception as e:
        print(f"ERRO ao conectar no MySQL: {e}")
        print("\nConfigure a URL do MySQL no inicio do arquivo migrate_data.py")
        sys.exit(1)

def get_postgres_connection():
    """Cria conexão com PostgreSQL"""
    try:
        engine = create_engine(settings.DATABASE_URL)
        Session = sessionmaker(bind=engine)
        return Session(), engine
    except Exception as e:
        print(f"ERRO ao conectar no PostgreSQL: {e}")
        sys.exit(1)

def migrate_escritorios(mysql_session, pg_session):
    """Migra tabela escritorio"""
    print("\nMigrando Escritorios...")
    
    # Buscar escritórios do MySQL
    result = mysql_session.execute(text("""
        SELECT id_escritorio, nome_fantasia, razao_social, documento, email, fone,
               cidade, uf, endereco_completo, endereco_reduzido, dias_uteis,
               prazo_arquiva_proposta, email_administrador, envio_email, instagram
        FROM escritorio
    """))
    
    count = 0
    for row in result:
        try:
            # Mapear campos MySQL -> PostgreSQL
            mysql_id = row[0]
            nome_fantasia = row[1] or ''
            razao_social = row[2] or nome_fantasia  # Fallback para nome_fantasia se vazio
            documento = row[3] or ''
            email = row[4] or ''
            telefone = row[5] or ''
            cidade = row[6] or ''
            uf = row[7] or ''
            endereco_completo = row[8] or ''
            endereco_reduzido = row[9] or ''
            dias_uteis = bool(row[10]) if row[10] is not None else True
            prazo_arquiva_proposta = row[11] if row[11] is not None else 30
            email_administrador = row[12] or ''
            envio_email = row[13] or ''
            instagram = row[14] or ''
            
            # Usar endereco_completo como endereco principal
            # Tentar extrair logradouro, numero, etc. do endereco_completo se possível
            # Por enquanto, vamos usar endereco_completo como está
            endereco = endereco_completo or endereco_reduzido
            
            pg_session.execute(text("""
                INSERT INTO escritorio (
                    id, nome_fantasia, razao_social, documento, email, telefone,
                    endereco, cidade, uf, dias_uteis, prazo_arquiva_proposta,
                    ativo, created_at, updated_at
                )
                VALUES (
                    :id, :nome_fantasia, :razao_social, :documento, :email, :telefone,
                    :endereco, :cidade, :uf, :dias_uteis, :prazo_arquiva_proposta,
                    TRUE, NOW(), NOW()
                )
                ON CONFLICT (id) DO UPDATE SET
                    nome_fantasia = EXCLUDED.nome_fantasia,
                    razao_social = EXCLUDED.razao_social,
                    documento = EXCLUDED.documento,
                    email = EXCLUDED.email,
                    telefone = EXCLUDED.telefone,
                    endereco = EXCLUDED.endereco,
                    cidade = EXCLUDED.cidade,
                    uf = EXCLUDED.uf,
                    dias_uteis = EXCLUDED.dias_uteis,
                    prazo_arquiva_proposta = EXCLUDED.prazo_arquiva_proposta,
                    updated_at = NOW()
            """), {
                'id': mysql_id,
                'nome_fantasia': nome_fantasia,
                'razao_social': razao_social,
                'documento': documento if documento else None,  # Pode ser NULL se vazio
                'email': email,
                'telefone': telefone,
                'endereco': endereco,
                'cidade': cidade,
                'uf': uf,
                'dias_uteis': dias_uteis,
                'prazo_arquiva_proposta': prazo_arquiva_proposta
            })
            count += 1
        except Exception as e:
            print(f"AVISO: Erro ao migrar escritorio {row[0]}: {e}")
    
    pg_session.commit()
    print(f"OK: {count} escritorios migrados")

def migrate_status(mysql_session, pg_session):
    """Migra tabela status"""
    print("\nMigrando Status...")
    
    # Buscar do MySQL
    result = mysql_session.execute(text("""
        SELECT cod_status, descricao, cor, ativo 
        FROM status 
        WHERE ativo = 1
    """))
    
    count = 0
    for row in result:
        # Inserir no PostgreSQL
        pg_session.execute(text("""
            INSERT INTO status (id, descricao, cor, ativo, created_at, updated_at)
            VALUES (:id, :descricao, :cor, :ativo, NOW(), NOW())
            ON CONFLICT (id) DO NOTHING
        """), {
            'id': row[0],
            'descricao': row[1],
            'cor': row[2],
            'ativo': bool(row[3])
        })
        count += 1
    
    pg_session.commit()
    print(f"OK: {count} status migrados")

def migrate_clientes(mysql_session, pg_session):
    """Migra tabela cliente"""
    print("\nMigrando Clientes...")
    
    result = mysql_session.execute(text("""
        SELECT cod_cliente, nome, razao_social, email, identificacao, 
               cod_tipo_pessoa, telefones, whatsapp, data_nascimento, ativo,
               logradouro, numero, complemento, bairro, cidade, uf, cep,
               inscricao_estadual, inscricao_municipal, indicado_por
        FROM cliente
        WHERE ativo = 1
    """))
    
    count = 0
    for row in result:
        try:
            # Mapear cod_tipo_pessoa para tipo_pessoa (1=PF, 2=PJ)
            tipo_pessoa = 'PF' if row[5] == 1 else 'PJ' if row[5] == 2 else 'PF'
            
            pg_session.execute(text("""
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
            count += 1
        except Exception as e:
            print(f"AVISO: Erro ao migrar cliente {row[0]}: {e}")
    
    pg_session.commit()
    print(f"OK: {count} clientes migrados")

def migrate_servicos(mysql_session, pg_session):
    """Migra tabela servico"""
    print("\nMigrando Servicos...")
    
    result = mysql_session.execute(text("""
        SELECT cod_servico, desc_servico, desc_documento, 
               codigo_plano_contas, ativo
        FROM servico
        WHERE ativo = 1
    """))
    
    count = 0
    for row in result:
        try:
            pg_session.execute(text("""
                INSERT INTO servicos (
                    id, nome, descricao, codigo_plano_contas, ativo,
                    created_at, updated_at
                )
                VALUES (
                    :id, :nome, :descricao, :codigo_plano_contas, :ativo,
                    NOW(), NOW()
                )
                ON CONFLICT (id) DO NOTHING
            """), {
                'id': row[0],
                'nome': row[1],
                'descricao': row[2],
                'codigo_plano_contas': row[3],
                'ativo': bool(row[4])
            })
            count += 1
        except Exception as e:
            print(f"AVISO: Erro ao migrar servico {row[0]}: {e}")
    
    pg_session.commit()
    print(f"OK: {count} servicos migrados")

def migrate_etapas(mysql_session, pg_session):
    """Migra tabela servico_etapa"""
    print("\nMigrando Etapas...")
    
    result = mysql_session.execute(text("""
        SELECT cod_servico_etapa, descricao, descricao_contrato, 
               ordem, cod_servico, exibir
        FROM servico_etapa
    """))
    
    count = 0
    skipped = 0
    for row in result:
        try:
            # Buscar escritorio_id do serviço
            servico = pg_session.execute(text("""
                SELECT escritorio_id
                FROM servicos
                WHERE id = :servico_id
            """), {'servico_id': row[4]}).first()
            
            if not servico:
                print(f"AVISO: Servico {row[4]} nao encontrado, pulando etapa {row[0]}")
                skipped += 1
                continue
            
            escritorio_id = servico[0]
            
            if not escritorio_id:
                print(f"AVISO: Servico {row[4]} nao tem escritorio_id, pulando etapa {row[0]}")
                skipped += 1
                continue
            
            pg_session.execute(text("""
                INSERT INTO etapas (
                    id, nome, descricao, ordem, servico_id, obrigatoria,
                    escritorio_id, created_at, updated_at
                )
                VALUES (
                    :id, :nome, :descricao, :ordem, :servico_id, :obrigatoria,
                    :escritorio_id, NOW(), NOW()
                )
                ON CONFLICT (id) DO UPDATE SET
                    nome = EXCLUDED.nome,
                    descricao = EXCLUDED.descricao,
                    ordem = EXCLUDED.ordem,
                    obrigatoria = EXCLUDED.obrigatoria,
                    escritorio_id = EXCLUDED.escritorio_id,
                    updated_at = NOW()
            """), {
                'id': row[0],
                'nome': row[1],
                'descricao': row[2],
                'ordem': row[3] or 0,
                'servico_id': row[4],
                'obrigatoria': bool(row[5]),
                'escritorio_id': escritorio_id
            })
            count += 1
        except Exception as e:
            print(f"AVISO: Erro ao migrar etapa {row[0]}: {e}")
            skipped += 1
            pg_session.rollback()  # Rollback apenas desta operação
    
    pg_session.commit()
    print(f"OK: {count} etapas migradas")
    if skipped > 0:
        print(f"AVISO: {skipped} etapas puladas (servicos nao encontrados ou sem escritorio_id)")

def migrate_tarefas(mysql_session, pg_session):
    """Migra tabela servico_microservico para tarefas"""
    print("\nMigrando Tarefas (Microservicos)...")
    
    # Buscar tarefas do MySQL
    result = mysql_session.execute(text("""
        SELECT cod_microservico, cod_etapa, descricao, ordem, cor, prazo, detalhe
        FROM servico_microservico
        ORDER BY cod_etapa, ordem
    """))
    
    count = 0
    skipped = 0
    updated = 0
    
    for row in result:
        mysql_tarefa_id = row[0]
        mysql_etapa_id = row[1]
        descricao = row[2] or ''
        ordem = row[3] or 0
        cor = row[4]
        prazo = bool(row[5]) if row[5] is not None else True
        detalhe = bool(row[6]) if row[6] is not None else False
        
        # Buscar etapa no PostgreSQL (IDs são preservados)
        etapa = pg_session.execute(text("""
            SELECT id, escritorio_id
            FROM etapas
            WHERE id = :etapa_id
        """), {'etapa_id': mysql_etapa_id}).first()
        
        if not etapa:
            print(f"AVISO: Etapa {mysql_etapa_id} nao encontrada no PostgreSQL, pulando tarefa {mysql_tarefa_id}")
            skipped += 1
            continue
        
        etapa_id = etapa[0]
        escritorio_id = etapa[1]
        
        try:
            # Verificar se já existe
            existing = pg_session.execute(text("""
                SELECT id FROM tarefas WHERE id = :id
            """), {'id': mysql_tarefa_id}).first()
            
            if existing:
                # Atualizar se já existe
                pg_session.execute(text("""
                    UPDATE tarefas SET
                        etapa_id = :etapa_id,
                        nome = :nome,
                        ordem = :ordem,
                        cor = :cor,
                        tem_prazo = :tem_prazo,
                        precisa_detalhamento = :precisa_detalhamento,
                        escritorio_id = :escritorio_id,
                        updated_at = NOW()
                    WHERE id = :id
                """), {
                    'id': mysql_tarefa_id,
                    'etapa_id': etapa_id,
                    'nome': descricao,
                    'ordem': ordem,
                    'cor': cor,
                    'tem_prazo': prazo,
                    'precisa_detalhamento': detalhe,
                    'escritorio_id': escritorio_id
                })
                updated += 1
            else:
                # Inserir nova
                pg_session.execute(text("""
                    INSERT INTO tarefas (
                        id, etapa_id, nome, ordem, cor, tem_prazo, precisa_detalhamento,
                        escritorio_id, created_at, updated_at
                    )
                    VALUES (
                        :id, :etapa_id, :nome, :ordem, :cor, :tem_prazo, :precisa_detalhamento,
                        :escritorio_id, NOW(), NOW()
                    )
                """), {
                    'id': mysql_tarefa_id,
                    'etapa_id': etapa_id,
                    'nome': descricao,
                    'ordem': ordem,
                    'cor': cor,
                    'tem_prazo': prazo,
                    'precisa_detalhamento': detalhe,
                    'escritorio_id': escritorio_id
                })
                count += 1
        except Exception as e:
            print(f"AVISO: Erro ao migrar tarefa {mysql_tarefa_id}: {e}")
            skipped += 1
            pg_session.rollback()  # Rollback apenas desta operação
    
    pg_session.commit()
    print(f"OK: {count} tarefas migradas")
    if updated > 0:
        print(f"ATUALIZADO: {updated} tarefas atualizadas")
    if skipped > 0:
        print(f"AVISO: {skipped} tarefas puladas (etapas nao encontradas, sem escritorio_id ou erros)")

def migrate_colaboradores(mysql_session, pg_session):
    """Migra tabela colaborador"""
    print("\nMigrando Colaboradores...")
    
    result = mysql_session.execute(text("""
        SELECT 
            cod_colaborador, nome, email, cpf, telefone, data_nascimento,
            senha, foto, ultimo_acesso, ativo
        FROM colaborador
        ORDER BY cod_colaborador
    """))
    
    count = 0
    skipped = 0
    
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
            if not nome or not email:
                print(f"AVISO: Colaborador {cod_colaborador} ignorado: nome ou email faltando")
                skipped += 1
                continue
            
            # Limpar CPF (remover caracteres não numéricos)
            cpf_limpo = None
            if cpf:
                cpf_limpo = ''.join(filter(str.isdigit, cpf))
                if len(cpf_limpo) != 11:
                    cpf_limpo = None  # CPF inválido, deixar NULL
            
            # Tratar foto (pode ser blob)
            foto_str = None
            if foto:
                if isinstance(foto, bytes):
                    foto_str = foto.decode('utf-8', errors='ignore')[:500]
                else:
                    foto_str = str(foto)[:500]
            
            # Verificar se já existe
            existing = pg_session.execute(text("""
                SELECT id FROM colaborador WHERE id = :id OR email = :email
            """), {'id': cod_colaborador, 'email': email}).first()
            
            if existing:
                # Atualizar se já existe
                pg_session.execute(text("""
                    UPDATE colaborador SET
                        nome = :nome,
                        cpf = :cpf,
                        telefone = :telefone,
                        data_nascimento = :data_nascimento,
                        senha = :senha,
                        foto = :foto,
                        ultimo_acesso = :ultimo_acesso,
                        ativo = :ativo,
                        updated_at = NOW()
                    WHERE id = :id
                """), {
                    'id': cod_colaborador,
                    'nome': nome,
                    'cpf': cpf_limpo,
                    'telefone': telefone,
                    'data_nascimento': data_nascimento,
                    'senha': senha,
                    'foto': foto_str,
                    'ultimo_acesso': ultimo_acesso,
                    'ativo': ativo
                })
            else:
                # Inserir novo
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
                    'foto': foto_str,
                    'ultimo_acesso': ultimo_acesso,
                    'ativo': ativo,
                    'perfil': 'Produção',  # Padrão
                    'tipo': 'Geral'  # Padrão
                })
            
            count += 1
        except Exception as e:
            print(f"AVISO: Erro ao migrar colaborador {row[0] if row else 'N/A'}: {e}")
            skipped += 1
            pg_session.rollback()
    
    pg_session.commit()
    print(f"OK: {count} colaboradores migrados")
    if skipped > 0:
        print(f"AVISO: {skipped} colaboradores pulados (erros ou dados inválidos)")

def migrate_colaborador_escritorio(mysql_session, pg_session):
    """Migra relacionamentos colaborador_escritorio"""
    print("\nMigrando Relacionamentos Colaborador-Escritorio...")
    
    result = mysql_session.execute(text("""
        SELECT 
            cod_colaborador, id_escritorio, socio, tipo, pix_tipo, pix_chave
        FROM colaborador_escritorio
        ORDER BY cod_colaborador, id_escritorio
    """))
    
    count = 0
    skipped = 0
    
    for row in result:
        try:
            cod_colaborador = row[0]
            id_escritorio = row[1]
            socio = row[2]  # '1' ou '0' ou NULL
            tipo = row[3]  # tinyint
            pix_tipo = row[4] if row[4] else None
            pix_chave = row[5] if row[5] else None
            
            # Verificar se colaborador existe no PostgreSQL
            colab = pg_session.execute(text("""
                SELECT id FROM colaborador WHERE id = :id
            """), {'id': cod_colaborador}).first()
            
            if not colab:
                print(f"AVISO: Colaborador {cod_colaborador} nao encontrado, pulando relacionamento")
                skipped += 1
                continue
            
            # Verificar se escritório existe no PostgreSQL
            esc = pg_session.execute(text("""
                SELECT id FROM escritorio WHERE id = :id
            """), {'id': id_escritorio}).first()
            
            if not esc:
                print(f"AVISO: Escritorio {id_escritorio} nao encontrado, pulando relacionamento")
                skipped += 1
                continue
            
            # Determinar perfil baseado em socio e tipo
            # Se for sócio, provavelmente é Administrador
            if socio == '1' or socio == 1:
                perfil = 'Administrador'
            elif tipo == 1:
                perfil = 'Coordenador de Projetos'
            else:
                perfil = 'Produção'
            
            # Verificar se relacionamento já existe
            existing = pg_session.execute(text("""
                SELECT colaborador_id FROM colaborador_escritorio
                WHERE colaborador_id = :colab_id AND escritorio_id = :esc_id
            """), {'colab_id': cod_colaborador, 'esc_id': id_escritorio}).first()
            
            if existing:
                # Atualizar se já existe
                pg_session.execute(text("""
                    UPDATE colaborador_escritorio SET
                        perfil = :perfil,
                        ativo = true
                    WHERE colaborador_id = :colab_id AND escritorio_id = :esc_id
                """), {
                    'colab_id': cod_colaborador,
                    'esc_id': id_escritorio,
                    'perfil': perfil
                })
            else:
                # Inserir novo relacionamento
                pg_session.execute(text("""
                    INSERT INTO colaborador_escritorio (
                        colaborador_id, escritorio_id, perfil, ativo
                    )
                    VALUES (
                        :colab_id, :esc_id, :perfil, true
                    )
                """), {
                    'colab_id': cod_colaborador,
                    'esc_id': id_escritorio,
                    'perfil': perfil
                })
            
            # Atualizar PIX no colaborador se fornecido
            if pix_tipo and pix_chave:
                pg_session.execute(text("""
                    UPDATE colaborador SET
                        tipo_pix = :tipo_pix,
                        chave_pix = :chave_pix
                    WHERE id = :id
                """), {
                    'id': cod_colaborador,
                    'tipo_pix': pix_tipo,
                    'chave_pix': pix_chave
                })
            
            count += 1
        except Exception as e:
            print(f"AVISO: Erro ao migrar relacionamento colaborador {row[0]}-escritorio {row[1]}: {e}")
            skipped += 1
            pg_session.rollback()
    
    pg_session.commit()
    print(f"OK: {count} relacionamentos migrados")
    if skipped > 0:
        print(f"AVISO: {skipped} relacionamentos pulados (colaborador ou escritorio nao encontrados)")

def migrate_propostas(mysql_session, pg_session):
    """Migra tabela proposta"""
    print("\nMigrando Propostas...")
    
    result = mysql_session.execute(text("""
        SELECT cod_proposta, cod_cliente, cod_servico, cod_status,
               nome, descricao, identificacao, numero_proposta, ano_proposta,
               data_proposta, valor_proposta, valor_avista, valor_parcela_aprazo,
               forma_pagamento, prazo, entrega_parcial, visitas_incluidas, observacao
        FROM proposta
    """))
    
    count = 0
    for row in result:
        try:
            pg_session.execute(text("""
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
            count += 1
        except Exception as e:
            print(f"AVISO: Erro ao migrar proposta {row[0]}: {e}")
    
    pg_session.commit()
    print(f"OK: {count} propostas migradas")

def migrate_projetos(mysql_session, pg_session):
    """Migra tabela projeto"""
    print("\nMigrando Projetos...")
    
    result = mysql_session.execute(text("""
        SELECT cod_projeto, cod_cliente, cod_servico, cod_proposta, cod_status,
               descricao, numero_projeto, ano_projeto,
               data_inicio, data_previsao_fim, data_fim,
               metragem, valor_contrato, saldo_contrato,
               observacao, observacao_contrato, cod_contratado, ativo
        FROM projeto
        WHERE ativo = 1
    """))
    
    count = 0
    for row in result:
        try:
            pg_session.execute(text("""
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
            count += 1
        except Exception as e:
            print(f"AVISO: Erro ao migrar projeto {row[0]}: {e}")
    
    pg_session.commit()
    print(f"OK: {count} projetos migrados")

def migrate_movimentos(mysql_session, pg_session):
    """Migra tabela movimento"""
    print("\nMigrando Movimentos Financeiros...")
    
    result = mysql_session.execute(text("""
        SELECT cod_movimento, cod_despesa_receita_tipo, data_entrada,
               data_efetivacao, competencia, descricao, observacao,
               valor, valor_acrescido, valor_desconto, valor_resultante,
               comprovante, extensao, codigo_plano_contas, ativo, cod_projeto
        FROM movimento
        WHERE ativo = 1
        LIMIT 1000
    """))
    
    count = 0
    for row in result:
        try:
            pg_session.execute(text("""
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
            count += 1
        except Exception as e:
            print(f"AVISO: Erro ao migrar movimento {row[0]}: {e}")
    
    pg_session.commit()
    print(f"OK: {count} movimentos migrados (limitado a 1000)")

def main():
    """Função principal"""
    print("=" * 60)
    print("MIGRACAO DE DADOS: MySQL -> PostgreSQL")
    print("=" * 60)
    
    # Conectar nos bancos
    print("\nConectando nos bancos de dados...")
    mysql_session, mysql_engine = get_mysql_connection()
    pg_session, pg_engine = get_postgres_connection()
    print("OK: Conexoes estabelecidas")
    
    try:
        # Executar migrações na ordem correta (respeitando FKs)
        # IMPORTANTE: Escritórios devem ser migrados PRIMEIRO, pois tudo depende de escritorio_id
        migrate_escritorios(mysql_session, pg_session)
        migrate_status(mysql_session, pg_session)
        migrate_clientes(mysql_session, pg_session)
        migrate_colaboradores(mysql_session, pg_session)
        migrate_colaborador_escritorio(mysql_session, pg_session)
        migrate_servicos(mysql_session, pg_session)
        migrate_etapas(mysql_session, pg_session)
        migrate_tarefas(mysql_session, pg_session)  # Migrar tarefas após etapas
        migrate_propostas(mysql_session, pg_session)
        migrate_projetos(mysql_session, pg_session)
        migrate_movimentos(mysql_session, pg_session)
        
        print("\n" + "=" * 60)
        print("MIGRACAO CONCLUIDA COM SUCESSO!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nERRO durante a migracao: {e}")
        pg_session.rollback()
    finally:
        mysql_session.close()
        pg_session.close()
        mysql_engine.dispose()
        pg_engine.dispose()

if __name__ == "__main__":
    main()
