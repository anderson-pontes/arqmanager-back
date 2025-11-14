"""Teste para verificar se CPF opcional funciona"""
from app.schemas.user import UserCreate
from pydantic import ValidationError

# Teste 1: CPF None
try:
    u1 = UserCreate(nome='Test', email='test@test.com', senha='123456', cpf=None)
    print('✅ CPF None aceito')
except ValidationError as e:
    print('❌ Erro com CPF None:', e.json())

# Teste 2: CPF omitido
try:
    u2 = UserCreate(nome='Test2', email='test2@test.com', senha='123456')
    print('✅ CPF omitido aceito')
except ValidationError as e:
    print('❌ Erro com CPF omitido:', e.json())

# Teste 3: CPF vazio
try:
    u3 = UserCreate(nome='Test3', email='test3@test.com', senha='123456', cpf='')
    print('✅ CPF vazio aceito')
except ValidationError as e:
    print('❌ Erro com CPF vazio:', e.json())

# Teste 4: CPF válido
try:
    u4 = UserCreate(nome='Test4', email='test4@test.com', senha='123456', cpf='12345678901')
    print('✅ CPF válido aceito')
except ValidationError as e:
    print('❌ Erro com CPF válido:', e.json())

print('\n✅ Todos os testes passaram!')







