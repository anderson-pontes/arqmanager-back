"""
Configuração para migração de dados
"""

# Configurações do MySQL
MYSQL_CONFIG = {
    "host": "dbarqmanager.cdcwiwycwh5a.sa-east-1.rds.amazonaws.com",
    "port": 3306,
    "user": "admin",  # Ajuste conforme necessário
    "password": "SUA_SENHA_AQUI",  # ⚠️ CONFIGURE AQUI
    "database": "dbarqmanager"
}

# Construir URL de conexão
def get_mysql_url():
    """Retorna URL de conexão do MySQL"""
    return (
        f"mysql+pymysql://{MYSQL_CONFIG['user']}:{MYSQL_CONFIG['password']}"
        f"@{MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']}/{MYSQL_CONFIG['database']}"
    )

# Opções de migração
MIGRATION_OPTIONS = {
    "batch_size": 1000,  # Quantidade de registros por lote
    "skip_existing": True,  # Pular registros que já existem
    "verbose": True  # Mostrar detalhes
}
