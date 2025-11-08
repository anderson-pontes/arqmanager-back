#!/usr/bin/env python3
"""
Script para listar views do MySQL
"""
from sqlalchemy import create_engine, text

MYSQL_URL = "mysql+pymysql://root:xpto1661WIN@localhost:3306/dbarqmanager"

def list_views():
    engine = create_engine(MYSQL_URL)
    
    with engine.connect() as conn:
        # Listar views
        result = conn.execute(text("SHOW FULL TABLES WHERE Table_type = 'VIEW'"))
        views = [row[0] for row in result]
        
        print("=" * 60)
        print(f"📋 VIEWS ENCONTRADAS NO MYSQL ({len(views)})")
        print("=" * 60)
        
        for view in views:
            print(f"   - {view}")
        
        print("\n" + "=" * 60)
        print("💡 Views são consultas SQL virtuais")
        print("   Precisam ser recriadas no PostgreSQL")
        print("=" * 60)

if __name__ == "__main__":
    list_views()
