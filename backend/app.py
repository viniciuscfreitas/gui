#!/usr/bin/env python3
"""
Backend simples para captura de leads - Grug-approved
Sem complexidade desnecessária, direto ao ponto.
"""
import sqlite3
import os
import logging
import time
from flask import Flask, request, jsonify, render_template_string, session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

# Configurar logging (Grug ama logging!)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'change-me-in-production-12345')
DB_PATH = os.environ.get('DB_PATH', 'leads.db')

# Garantir que o diretório do DB existe
db_dir = os.path.dirname(DB_PATH)
if db_dir and not os.path.exists(db_dir):
    os.makedirs(db_dir, exist_ok=True)

# SQLite thread-safe mode (Grug teme concorrência, mas precisa funcionar)
# timeout=20.0 permite retry automático em caso de lock
def get_db_connection():
    conn = sqlite3.connect(DB_PATH, timeout=20.0)
    conn.row_factory = sqlite3.Row
    return conn

# Inicializar DB se não existir
def init_db():
    conn = get_db_connection()
    try:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                contact TEXT,
                message TEXT,
                budget TEXT,
                form_type TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS admin_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
        # Criar admin padrão se não existir
        cursor = conn.execute('SELECT COUNT(*) FROM admin_users')
        if cursor.fetchone()[0] == 0:
            default_hash = generate_password_hash('admin123')
            conn.execute('INSERT INTO admin_users (username, password_hash) VALUES (?, ?)', 
                        ('admin', default_hash))
            logger.info('Admin user created (default: admin/admin123)')
        conn.commit()
    finally:
        conn.close()

init_db()
logger.info('Database initialized')

# Decorator para rotas protegidas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Validação básica de input (Grug-approved: simples, direto)
def validate_lead_data(name, email, contact, message):
    """Validação básica - sem complexidade desnecessária"""
    if not name or len(name.strip()) == 0:
        return 'Name is required'
    if len(name) > 200:
        return 'Name too long (max 200 chars)'
    if email and len(email) > 200:
        return 'Email too long (max 200 chars)'
    if contact and len(contact) > 200:
        return 'Contact too long (max 200 chars)'
    if message and len(message) > 2000:
        return 'Message too long (max 2000 chars)'
    return None

# API: Receber lead do formulário
@app.route('/api/leads', methods=['POST'])
def create_lead():
    data = request.get_json()
    
    if not data:
        logger.warning('Create lead: No data provided')
        return jsonify({'error': 'No data provided'}), 400
    
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    contact = data.get('contact', '').strip()
    message = data.get('message', '').strip()
    budget = data.get('budget', '').strip()
    form_type = data.get('form_type', 'inline')
    
    # Validação
    validation_error = validate_lead_data(name, email, contact, message)
    if validation_error:
        logger.warning(f'Create lead: Validation failed - {validation_error}')
        return jsonify({'error': validation_error}), 400
    
    # Retry logic para concorrência (Grug teme concorrência, mas precisa funcionar)
    max_retries = 3
    for attempt in range(max_retries):
        try:
            conn = get_db_connection()
            try:
                cursor = conn.execute('''
                    INSERT INTO leads (name, email, contact, message, budget, form_type)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (name, email, contact, message, budget, form_type))
                conn.commit()
                lead_id = cursor.lastrowid
                logger.info(f'Lead created: ID={lead_id}, Name={name}, Type={form_type}')
                return jsonify({'success': True, 'id': lead_id}), 201
            finally:
                conn.close()
        except sqlite3.OperationalError as e:
            if 'database is locked' in str(e).lower() and attempt < max_retries - 1:
                wait_time = 0.1 * (attempt + 1)  # Backoff simples
                logger.warning(f'Database locked, retrying in {wait_time}s (attempt {attempt + 1}/{max_retries})')
                time.sleep(wait_time)
                continue
            logger.error(f'Database operational error creating lead: {e}')
            return jsonify({'error': 'Database temporarily unavailable'}), 503
        except sqlite3.Error as e:
            logger.error(f'Database error creating lead: {e}')
            return jsonify({'error': 'Database error'}), 500
        except Exception as e:
            logger.error(f'Unexpected error creating lead: {e}', exc_info=True)
            return jsonify({'error': 'Internal server error'}), 500
    
    logger.error('Failed to create lead after all retries')
    return jsonify({'error': 'Database temporarily unavailable'}), 503

# API: Listar leads (protegido)
@app.route('/api/leads', methods=['GET'])
@login_required
def list_leads():
    try:
        conn = get_db_connection()
        try:
            cursor = conn.execute('''
                SELECT id, name, email, contact, message, budget, form_type, created_at
                FROM leads
                ORDER BY created_at DESC
            ''')
            leads = []
            for row in cursor.fetchall():
                leads.append({
                    'id': row[0],
                    'name': row[1],
                    'email': row[2],
                    'contact': row[3],
                    'message': row[4],
                    'budget': row[5],
                    'form_type': row[6],
                    'created_at': row[7]
                })
            logger.info(f'Leads listed: {len(leads)} leads by user {session.get("username")}')
            return jsonify({'leads': leads}), 200
        finally:
            conn.close()
    except sqlite3.OperationalError as e:
        logger.error(f'Database operational error listing leads: {e}')
        return jsonify({'error': 'Database temporarily unavailable'}), 503
    except sqlite3.Error as e:
        logger.error(f'Database error listing leads: {e}')
        return jsonify({'error': 'Database error'}), 500
    except Exception as e:
        logger.error(f'Unexpected error listing leads: {e}', exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

# API: Deletar lead (protegido)
@app.route('/api/leads/<int:lead_id>', methods=['DELETE'])
@login_required
def delete_lead(lead_id):
    try:
        conn = get_db_connection()
        try:
            cursor = conn.execute('DELETE FROM leads WHERE id = ?', (lead_id,))
            conn.commit()
            if cursor.rowcount == 0:
                logger.warning(f'Lead not found for deletion: ID={lead_id}')
                return jsonify({'error': 'Lead not found'}), 404
            logger.info(f'Lead deleted: ID={lead_id} by user {session.get("username")}')
            return jsonify({'success': True}), 200
        finally:
            conn.close()
    except sqlite3.OperationalError as e:
        logger.error(f'Database operational error deleting lead {lead_id}: {e}')
        return jsonify({'error': 'Database temporarily unavailable'}), 503
    except sqlite3.Error as e:
        logger.error(f'Database error deleting lead {lead_id}: {e}')
        return jsonify({'error': 'Database error'}), 500
    except Exception as e:
        logger.error(f'Unexpected error deleting lead {lead_id}: {e}', exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

# Login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        logger.warning('Login attempt: Missing credentials')
        return jsonify({'error': 'Username and password required'}), 400
    
    try:
        conn = get_db_connection()
        try:
            cursor = conn.execute('SELECT password_hash FROM admin_users WHERE username = ?', (username,))
            row = cursor.fetchone()
            
            if row and check_password_hash(row[0], password):
                session['logged_in'] = True
                session['username'] = username
                logger.info(f'Login successful: {username}')
                return jsonify({'success': True}), 200
            else:
                logger.warning(f'Login failed: Invalid credentials for {username}')
                return jsonify({'error': 'Invalid credentials'}), 401
        finally:
            conn.close()
    except sqlite3.OperationalError as e:
        logger.error(f'Database operational error during login: {e}')
        return jsonify({'error': 'Database temporarily unavailable'}), 503
    except sqlite3.Error as e:
        logger.error(f'Database error during login: {e}')
        return jsonify({'error': 'Database error'}), 500
    except Exception as e:
        logger.error(f'Unexpected error during login: {e}', exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

# Logout
@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    username = session.get('username', 'unknown')
    session.clear()
    logger.info(f'Logout: {username}')
    return jsonify({'success': True}), 200

# Healthcheck
@app.route('/health')
def health():
    logger.debug('Health check')
    return jsonify({'status': 'ok'}), 200

# Painel admin (HTML/CSS/JS vanilla - Grug-approved)
@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        return render_template_string(LOGIN_HTML), 200
    return render_template_string(ADMIN_HTML), 200

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)

# Templates inline (Locality of Behavior - Grug-approved)
LOGIN_HTML = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin - Login</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #000;
            color: #fff;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            padding: 1rem;
        }
        .login-box {
            background: #0a0a0a;
            border: 1px solid #333;
            padding: 2rem;
            max-width: 400px;
            width: 100%;
        }
        h1 { margin-bottom: 1.5rem; font-size: 1.5rem; }
        .form-group { margin-bottom: 1.5rem; }
        label { display: block; margin-bottom: 0.5rem; font-size: 0.875rem; color: #999; }
        input {
            width: 100%;
            padding: 0.75rem;
            background: #000;
            border: 1px solid #333;
            color: #fff;
            font-size: 1rem;
        }
        input:focus { outline: none; border-color: #ff3333; }
        button {
            width: 100%;
            padding: 0.75rem;
            background: #ff3333;
            color: #000;
            border: none;
            font-weight: 700;
            cursor: pointer;
            font-size: 1rem;
        }
        button:hover { background: #fff; }
        .error { color: #ff3333; margin-top: 1rem; font-size: 0.875rem; display: none; }
    </style>
</head>
<body>
    <div class="login-box">
        <h1>Admin Login</h1>
        <form id="loginForm">
            <div class="form-group">
                <label>Usuário</label>
                <input type="text" name="username" required autocomplete="username">
            </div>
            <div class="form-group">
                <label>Senha</label>
                <input type="password" name="password" required autocomplete="current-password">
            </div>
            <button type="submit">Entrar</button>
            <div class="error" id="error"></div>
        </form>
    </div>
    <script>
        document.getElementById('loginForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);
            
            const res = await fetch('/api/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            
            if (res.ok) {
                window.location.reload();
            } else {
                const error = await res.json();
                document.getElementById('error').textContent = error.error || 'Erro ao fazer login';
                document.getElementById('error').style.display = 'block';
            }
        });
    </script>
</body>
</html>'''

ADMIN_HTML = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin - Leads</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #000;
            color: #fff;
            padding: 2rem;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid #333;
        }
        h1 { font-size: 1.5rem; }
        .logout-btn {
            padding: 0.5rem 1rem;
            background: #333;
            color: #fff;
            border: 1px solid #555;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
        }
        .logout-btn:hover { background: #555; }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }
        .stat-card {
            background: #0a0a0a;
            border: 1px solid #333;
            padding: 1.5rem;
        }
        .stat-value { font-size: 2rem; font-weight: 700; color: #ff3333; }
        .stat-label { font-size: 0.875rem; color: #999; margin-top: 0.5rem; }
        .leads-table {
            width: 100%;
            border-collapse: collapse;
            background: #0a0a0a;
        }
        .leads-table th,
        .leads-table td {
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid #333;
        }
        .leads-table th {
            background: #050505;
            font-weight: 700;
            color: #ff3333;
        }
        .leads-table tr:hover { background: #111; }
        .delete-btn {
            padding: 0.25rem 0.75rem;
            background: #ff3333;
            color: #000;
            border: none;
            cursor: pointer;
            font-size: 0.75rem;
            font-weight: 700;
        }
        .delete-btn:hover { background: #fff; }
        .empty {
            text-align: center;
            padding: 3rem;
            color: #999;
        }
        @media (max-width: 768px) {
            .leads-table { font-size: 0.875rem; }
            .leads-table th,
            .leads-table td { padding: 0.5rem; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Painel de Leads</h1>
        <button class="logout-btn" onclick="logout()">Sair</button>
    </div>
    
    <div class="stats" id="stats"></div>
    
    <table class="leads-table">
        <thead>
            <tr>
                <th>ID</th>
                <th>Nome</th>
                <th>Contato</th>
                <th>Mensagem</th>
                <th>Orçamento</th>
                <th>Data</th>
                <th>Ações</th>
            </tr>
        </thead>
        <tbody id="leadsTable"></tbody>
    </table>
    
    <div class="empty" id="empty" style="display: none;">Nenhum lead encontrado.</div>
    
    <script>
        async function loadLeads() {
            const res = await fetch('/api/leads');
            if (!res.ok) {
                if (res.status === 401) {
                    window.location.reload();
                    return;
                }
                return;
            }
            const data = await res.json();
            const leads = data.leads || [];
            
            // Stats
            document.getElementById('stats').innerHTML = `
                <div class="stat-card">
                    <div class="stat-value">${leads.length}</div>
                    <div class="stat-label">Total de Leads</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${leads.filter(l => l.form_type === 'inline').length}</div>
                    <div class="stat-label">Formulário Inline</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${leads.filter(l => l.form_type === 'modal').length}</div>
                    <div class="stat-label">Formulário Modal</div>
                </div>
            `;
            
            // Table
            const tbody = document.getElementById('leadsTable');
            if (leads.length === 0) {
                document.getElementById('empty').style.display = 'block';
                tbody.innerHTML = '';
            } else {
                document.getElementById('empty').style.display = 'none';
                tbody.innerHTML = leads.map(lead => `
                    <tr>
                        <td>${lead.id}</td>
                        <td>${escapeHtml(lead.name)}</td>
                        <td>${escapeHtml(lead.email || lead.contact || '-')}</td>
                        <td>${escapeHtml(lead.message || '-')}</td>
                        <td>${escapeHtml(lead.budget || '-')}</td>
                        <td>${formatDate(lead.created_at)}</td>
                        <td>
                            <button class="delete-btn" onclick="deleteLead(${lead.id})">Deletar</button>
                        </td>
                    </tr>
                `).join('');
            }
        }
        
        async function deleteLead(id) {
            if (!confirm('Tem certeza que deseja deletar este lead?')) return;
            
            const res = await fetch(`/api/leads/${id}`, { method: 'DELETE' });
            if (res.ok) {
                loadLeads();
            } else {
                alert('Erro ao deletar lead');
            }
        }
        
        async function logout() {
            await fetch('/api/logout', { method: 'POST' });
            window.location.reload();
        }
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        function formatDate(dateStr) {
            const date = new Date(dateStr);
            return date.toLocaleString('pt-BR');
        }
        
        loadLeads();
        setInterval(loadLeads, 30000); // Atualizar a cada 30s
    </script>
</body>
</html>'''

