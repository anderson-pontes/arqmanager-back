"""
Script para limpar campo indicado_por que contém IDs
"""
import sys
sys.path.insert(0, '.')

from app.database import SessionLocal
from app.models.cliente import Cliente

db = SessionLocal()

print("=" * 60)
print("LIMPANDO CAMPO INDICADO_POR")
print("=" * 60)

# Buscar clientes com indicado_por que parece ser um ID (apenas números)
clientes = db.query(Cliente).all()

count = 0
for cliente in clientes:
    if cliente.indicado_por and cliente.indicado_por.isdigit():
        print(f"Cliente {cliente.id} - {cliente.nome}: '{cliente.indicado_por}' → NULL")
        cliente.indicado_por = None
        count += 1

if count > 0:
    db.commit()
    print(f"\n✅ {count} clientes atualizados!")
else:
    print("\n✅ Nenhum cliente precisa ser atualizado")

db.close()
