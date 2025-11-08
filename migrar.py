#!/usr/bin/env python3
"""
Script assistente para migração de dados MySQL → PostgreSQL
Executa todos os passos necessários de forma interativa
"""
import sys
import subprocess
import os

def print_header(text):
    """Imprime cabeçalho formatado"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")

def print_step(number, text):
    """Imprime passo numerado"""
    print(f"\n{'='*60}")
    print(f"  PASSO {number}: {text}")
    print(f"{'='*60}\n")

def ask_yes_no(question):
    """Pergunta sim/não ao usuário"""
    while True:
        response = input(f"{question} (s/n): ").lower().strip()
        if response in ['s', 'sim', 'y', 'yes']:
            return True
        elif response in ['n', 'não', 'nao', 'no']:
            return False
        print("Por favor, responda 's' para sim ou 'n' para não.")

def run_script(script_name):
    """Executa um script Python"""
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=False,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Erro ao executar {script_name}: {e}")
        return False

def main():
    """Função principal do assistente"""
    print_header("🔄 ASSISTENTE DE MIGRAÇÃO MySQL → PostgreSQL")
    
    print("Este assistente vai guiá-lo através do processo de migração.")
    print("Certifique-se de ter:")
    print("  ✅ Acesso ao banco MySQL")
    print("  ✅ PostgreSQL configurado")
    print("  ✅ Ambiente virtual ativado")
    
    if not ask_yes_no("\nDeseja continuar?"):
        print("\n👋 Migração cancelada.")
        return
    
    # Passo 1: Verificar pymysql
    print_step(1, "Verificar dependências")
    try:
        import pymysql
        print("✅ pymysql instalado")
    except ImportError:
        print("⚠️  pymysql não encontrado")
        if ask_yes_no("Deseja instalar agora?"):
            print("\nInstalando pymysql...")
            subprocess.run([sys.executable, "-m", "pip", "install", "pymysql"])
        else:
            print("\n❌ pymysql é necessário. Execute: pip install pymysql")
            return
    
    # Passo 2: Configurar credenciais
    print_step(2, "Configurar credenciais MySQL")
    print("Você precisa editar os arquivos:")
    print("  - check_mysql.py (linha 8)")
    print("  - migrate_data.py (linha 11)")
    print("\nFormato: mysql+pymysql://usuario:senha@host:3306/dbarqmanager")
    
    if not ask_yes_no("\nJá configurou as credenciais?"):
        print("\n⚠️  Configure as credenciais antes de continuar.")
        print("Edite os arquivos mencionados e execute este script novamente.")
        return
    
    # Passo 3: Testar MySQL
    print_step(3, "Testar conexão MySQL")
    if ask_yes_no("Deseja testar a conexão com MySQL?"):
        if not run_script("check_mysql.py"):
            print("\n❌ Erro ao conectar no MySQL.")
            if not ask_yes_no("Deseja continuar mesmo assim?"):
                return
    
    # Passo 4: Verificar PostgreSQL
    print_step(4, "Verificar PostgreSQL")
    print("Verificando se as migrations foram aplicadas...")
    
    try:
        from app.core.config import settings
        from sqlalchemy import create_engine, inspect
        
        engine = create_engine(settings.DATABASE_URL)
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        required_tables = ['status', 'cliente', 'servicos', 'etapas', 'propostas', 'projetos', 'movimentos']
        missing = [t for t in required_tables if t not in tables]
        
        if missing:
            print(f"\n⚠️  Tabelas faltando: {missing}")
            print("\nExecute: alembic upgrade head")
            if not ask_yes_no("Deseja continuar mesmo assim?"):
                return
        else:
            print("✅ Todas as tabelas necessárias existem")
            
    except Exception as e:
        print(f"⚠️  Erro ao verificar PostgreSQL: {e}")
        if not ask_yes_no("Deseja continuar mesmo assim?"):
            return
    
    # Passo 5: Executar migração
    print_step(5, "Executar migração")
    print("⚠️  ATENÇÃO: Este processo vai inserir dados no PostgreSQL.")
    print("Os dados do MySQL permanecerão intactos.")
    
    if not ask_yes_no("\nDeseja executar a migração agora?"):
        print("\n👋 Migração cancelada.")
        return
    
    print("\n🚀 Iniciando migração...\n")
    if run_script("migrate_data.py"):
        print("\n✅ Migração concluída!")
    else:
        print("\n❌ Erro durante a migração.")
        return
    
    # Passo 6: Verificar dados
    print_step(6, "Verificar dados migrados")
    if ask_yes_no("Deseja verificar os dados migrados?"):
        run_script("check_migrated_data.py")
    
    # Conclusão
    print_header("🎉 PROCESSO CONCLUÍDO!")
    print("Próximos passos:")
    print("  1. Testar a API: uvicorn app.main:app --reload")
    print("  2. Criar admin: python create_admin.py")
    print("  3. Testar login: python test_login.py")
    print("\n📚 Documentação:")
    print("  - GUIA_MIGRACAO_DADOS.md")
    print("  - CHECKLIST_MIGRACAO.md")
    print("\n✅ Tudo pronto para usar!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Migração cancelada pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
