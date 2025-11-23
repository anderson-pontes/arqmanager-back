"""Script para corrigir perfis de colaboradores"""
from sqlalchemy import text
from app.database import engine

def fix_perfis_colaboradores():
    """Corrige perfis de colaboradores para valores válidos"""
    
    with engine.connect() as conn:
        # Mapear perfis antigos para novos
        updates = [
            ("Colaborador", "Produção"),
            ("colaborador", "Produção"),
            ("COLABORADOR", "Produção"),
        ]
        
        for old_perfil, new_perfil in updates:
            result = conn.execute(text("""
                UPDATE colaborador 
                SET perfil = :new_perfil
                WHERE perfil = :old_perfil
            """), {'old_perfil': old_perfil, 'new_perfil': new_perfil})
            
            updated = result.rowcount
            if updated > 0:
                print(f"Atualizados {updated} colaboradores de '{old_perfil}' para '{new_perfil}'")
        
        # Verificar perfis restantes
        result = conn.execute(text("""
            SELECT DISTINCT perfil, COUNT(*) 
            FROM colaborador 
            GROUP BY perfil
        """))
        
        print("\nPerfis apos correcao:")
        for row in result:
            print(f"  {row[0]}: {row[1]} colaboradores")
        
        conn.commit()
        print("\nOK: Perfis corrigidos!")

if __name__ == "__main__":
    fix_perfis_colaboradores()






