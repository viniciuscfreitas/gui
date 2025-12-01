#!/usr/bin/env python3
"""
Testes de integração simples - Grug-approved
Integration tests, não unit tests isolados com mocking excessivo.
"""
import os
import sqlite3
import pytest
from app import app, get_db_connection, init_db

# Usar DB de teste separado
TEST_DB = 'test_leads.db'

@pytest.fixture(scope='function')
def client():
    """Setup cliente de teste e DB limpo"""
    # Backup do DB path original
    import app as app_module
    original_db = app_module.DB_PATH
    
    # Usar DB de teste
    app_module.DB_PATH = TEST_DB
    
    # Limpar DB de teste
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    
    # Inicializar DB de teste
    init_db()
    
    # Configurar app para testes
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    with app.test_client() as client:
        yield client
    
    # Limpar após teste
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    
    # Restaurar DB path original
    app_module.DB_PATH = original_db

def test_health_check(client):
    """Teste básico: health check deve funcionar"""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'ok'

def test_create_lead_success(client):
    """Teste: criar lead deve funcionar"""
    response = client.post('/api/leads', json={
        'name': 'João Silva',
        'email': 'joao@test.com',
        'message': 'Quero fazer campanha',
        'form_type': 'inline'
    })
    assert response.status_code == 201
    assert response.json['success'] == True
    assert 'id' in response.json

def test_create_lead_missing_name(client):
    """Teste: criar lead sem nome deve falhar"""
    response = client.post('/api/leads', json={
        'email': 'joao@test.com'
    })
    assert response.status_code == 400
    assert 'error' in response.json
    assert 'Name is required' in response.json['error']

def test_create_lead_name_too_long(client):
    """Teste: criar lead com nome muito longo deve falhar"""
    response = client.post('/api/leads', json={
        'name': 'A' * 201,  # 201 caracteres
        'email': 'test@test.com'
    })
    assert response.status_code == 400
    assert 'error' in response.json

def test_create_lead_no_data(client):
    """Teste: criar lead sem dados deve falhar"""
    response = client.post('/api/leads', json={})
    assert response.status_code == 400

def test_list_leads_requires_auth(client):
    """Teste: listar leads requer autenticação"""
    response = client.get('/api/leads')
    assert response.status_code == 401

def test_login_success(client):
    """Teste: login com credenciais corretas"""
    response = client.post('/api/login', json={
        'username': 'admin',
        'password': 'admin123'
    })
    assert response.status_code == 200
    assert response.json['success'] == True

def test_login_wrong_password(client):
    """Teste: login com senha errada deve falhar"""
    response = client.post('/api/login', json={
        'username': 'admin',
        'password': 'wrong'
    })
    assert response.status_code == 401

def test_list_leads_after_login(client):
    """Teste: listar leads após login deve funcionar"""
    # Login
    login_res = client.post('/api/login', json={
        'username': 'admin',
        'password': 'admin123'
    })
    assert login_res.status_code == 200
    
    # Criar lead
    client.post('/api/leads', json={
        'name': 'Test Lead',
        'email': 'test@test.com',
        'form_type': 'inline'
    })
    
    # Listar leads
    response = client.get('/api/leads')
    assert response.status_code == 200
    assert 'leads' in response.json
    assert len(response.json['leads']) == 1

def test_delete_lead(client):
    """Teste: deletar lead deve funcionar"""
    # Login
    client.post('/api/login', json={
        'username': 'admin',
        'password': 'admin123'
    })
    
    # Criar lead
    create_res = client.post('/api/leads', json={
        'name': 'Test Delete',
        'email': 'delete@test.com',
        'form_type': 'inline'
    })
    lead_id = create_res.json['id']
    
    # Deletar lead
    delete_res = client.delete(f'/api/leads/{lead_id}')
    assert delete_res.status_code == 200
    
    # Verificar que foi deletado
    list_res = client.get('/api/leads')
    assert len(list_res.json['leads']) == 0

def test_logout(client):
    """Teste: logout deve funcionar"""
    # Login
    client.post('/api/login', json={
        'username': 'admin',
        'password': 'admin123'
    })
    
    # Logout
    response = client.post('/api/logout')
    assert response.status_code == 200
    
    # Verificar que não consegue mais acessar
    list_res = client.get('/api/leads')
    assert list_res.status_code == 401

if __name__ == '__main__':
    pytest.main([__file__, '-v'])

