#!/usr/bin/env python3
"""
Script para testar as views criadas no PostgreSQL
"""
from sqlalchemy import create_engine, text
from app.core.config import settings

def test_views():
    """Testa as views criadas"""
    engine = create_engine(settings.DATABASE_URL)
    
    views = [
        'v_cliente',
        'v_projeto',
        'v_proposta',
        'v_movimento',
        'v_servico_etapa',
        'v_colaborador'
    ]
    
    print("=" * 60)
    print("🧪 TESTANDO VIEWS DO POSTGRESQL")
    print("=" * 60)
    
    with engine.connect() as conn:
        for view_name in views:
            try:
                print(f"\n📊 Testando: {view_name}")
                
                # Contar registros
                result = conn.execute(text(f"SELECT COUNT(*) FROM {view_name}"))
                count = result.scalar()
                print(f"   ✅ {count} registros encontrados")
                
                # Mostrar primeiros 3 registros
                result = conn.execute(text(f"SELECT * FROM {view_name} LIMIT 3"))
                rows = result.fetchall()
                
                if rows:
                    print(f"   📋 Primeiros registros:")
                    for i, row in enumerate(rows, 1):
                        # Mostrar apenas primeiros 3 campos
                        fields = [str(v)[:50] for v in list(row)[:3]]
                        print(f"      {i}. {' | '.join(fields)}")
                else:
                    print(f"   ⚠️  Nenhum registro encontrado")
                    
            except Exception as e:
                print(f"   ❌ Erro: {str(e)[:100]}")
    
    print("\n" + "=" * 60)
    print("✅ TESTE CONCLUÍDO!")
    print("=" * 60)

if __name__ == "__main__":
    test_views()
