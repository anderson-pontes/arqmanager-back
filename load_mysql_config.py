"""Carrega configuração MySQL de arquivo ou variável de ambiente"""
import os
from pathlib import Path

def load_mysql_url():
    """Carrega URL do MySQL de arquivo de configuração ou variável de ambiente"""
    # 1. Tentar variável de ambiente
    mysql_url = os.getenv('MYSQL_URL')
    if mysql_url:
        return mysql_url
    
    # 2. Tentar arquivo .mysql_config
    config_file = Path(__file__).parent / '.mysql_config'
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and line.startswith('MYSQL_URL='):
                    return line.split('=', 1)[1].strip()
    
    # 3. Retornar None se não encontrou
    return None

if __name__ == "__main__":
    url = load_mysql_url()
    if url:
        # Mascarar senha na exibição
        if '@' in url:
            parts = url.split('@')
            if ':' in parts[0]:
                user_pass = parts[0].split('://', 1)[1]
                if ':' in user_pass:
                    user = user_pass.split(':')[0]
                    masked = f"mysql+pymysql://{user}:***@{parts[1]}"
                    print(f"URL configurada: {masked}")
                else:
                    print(f"URL configurada: {url}")
            else:
                print(f"URL configurada: {url}")
        else:
            print(f"URL configurada: {url}")
    else:
        print("Nenhuma configuracao encontrada!")
        print("\nConfigure de uma das formas:")
        print("1. Variavel de ambiente: export MYSQL_URL='mysql+pymysql://...'")
        print("2. Arquivo .mysql_config na raiz do projeto")
        print("3. Editar diretamente migrate_data.py linha 13")

