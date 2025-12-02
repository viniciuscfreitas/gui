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
    <title>Admin • Gui</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>⚡</text></svg>">

    <!-- Grug usa Tailwind CDN. Rápido. Fácil. -->
    <script src="https://cdn.tailwindcss.com"></script>

    <!-- Grug usa Lucide Icons. Bonitos. -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <script>
        // Grug helper: garantir que Lucide está disponível
        window.initLucide = function() {
            if (typeof lucide !== 'undefined' && typeof lucide.createIcons === 'function') {
                lucide.createIcons();
                return true;
            }
            return false;
        };
    </script>

    <!-- Fonte Syne e Inter -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Syne:wght@700;800&display=swap"
        rel="stylesheet">

    <style>
        /* Grug Configurações Visuais */
        body {
            background-color: #0f0f0f;
            color: #f3f4f6;
            font-family: 'Inter', sans-serif;
            overflow: hidden;
            /* App feel */
        }

        .font-syne {
            font-family: 'Syne', sans-serif;
        }

        /* Scrollbar invisível. Grug gosta limpo. */
        ::-webkit-scrollbar {
            width: 0px;
            background: transparent;
        }

        /* Foco acessível mas bonito */
        button:focus-visible,
        input:focus-visible {
            outline: 2px solid #d4af37;
            outline-offset: 2px;
        }

        /* Utilitários de Animação */
        .slide-in {
            transform: translateX(0%);
        }

        .slide-out {
            transform: translateX(100%);
        }

        /* Cores Neon Grug */
        .text-neon-pink {
            color: #ff00aa;
        }

        .bg-neon-pink-10 {
            background-color: rgba(255, 0, 170, 0.1);
        }

        .text-neon-green {
            color: #39ff14;
        }

        .bg-neon-green-10 {
            background-color: rgba(57, 255, 20, 0.1);
        }

        .text-gold {
            color: #d4af37;
        }

        .bg-gold-10 {
            background-color: rgba(212, 175, 55, 0.1);
        }
    </style>
</head>

<body class="selection:bg-[#d4af37] selection:text-black">

    <!-- SOM DE NOTIFICAÇÃO (Base64 para não depender de arquivo) -->
    <audio id="notif-sound" src="data:audio/wav;base64,UklGRl9vT19XQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YU"></audio>

    <!-- TOAST CONTAINER -->
    <div id="toast-container" class="fixed bottom-6 left-24 z-[100]"></div>

    <!-- DASHBOARD -->
    <div id="dashboard" class="flex h-screen">

        <!-- SIDEBAR RAIL -->
        <aside class="w-24 bg-[#0f0f0f] flex flex-col items-center py-6 gap-8 z-50 border-r border-white/0">
            <div
                class="w-12 h-12 bg-[#d4af37] text-black rounded-xl flex items-center justify-center shadow-[4px_4px_0px_0px_#1a1a1a] cursor-pointer hover:-translate-y-0.5 transition-transform">
                <i data-lucide="zap" class="w-6 h-6 fill-current"></i>
            </div>

            <nav class="flex-1 flex flex-col gap-6 w-full px-2" id="nav-buttons">
                <button onclick="app.setFilter('hoje')"
                    class="nav-btn w-12 h-12 rounded-2xl flex items-center justify-center mx-auto text-[#d4af37] bg-[#1a1a1a] shadow-[0_0_20px_rgba(212,175,55,0.1)] transition-all"
                    data-filter="hoje" title="Visão Geral">
                    <i data-lucide="layout-dashboard" class="w-5 h-5"></i>
                </button>
                <button onclick="app.setFilter('quentes')"
                    class="nav-btn w-12 h-12 rounded-2xl flex items-center justify-center mx-auto text-gray-400 hover:text-white hover:bg-[#1a1a1a] transition-all"
                    data-filter="quentes" title="Quentes">
                    <i data-lucide="trending-up" class="w-5 h-5 text-neon-pink"></i>
                </button>
                <button onclick="app.setFilter('whatsapp')"
                    class="nav-btn w-12 h-12 rounded-2xl flex items-center justify-center mx-auto text-gray-400 hover:text-white hover:bg-[#1a1a1a] transition-all"
                    data-filter="whatsapp" title="WhatsApp">
                    <i data-lucide="message-circle" class="w-5 h-5"></i>
                </button>
            </nav>

            <div class="mb-4">
                <div class="w-10 h-10 rounded-full bg-gradient-to-tr from-[#d4af37] to-[#ff00aa] p-[2px]">
                    <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Gui" class="rounded-full bg-black">
                </div>
            </div>
        </aside>

        <!-- MAIN CONTENT -->
        <main class="flex-1 flex flex-col relative overflow-hidden">

            <!-- HEADER -->
            <header class="px-10 py-8 flex items-center justify-between shrink-0">
                <div>
                    <h1 class="text-3xl font-syne font-bold text-white flex items-center gap-3">
                        Olá, Gui! <span class="text-2xl animate-bounce">👋</span>
                    </h1>
                    <p class="text-gray-400 text-sm mt-1">Hoje, <span id="current-date"></span> • Pipeline Atualizado
                    </p>
                </div>

                <div class="flex items-center gap-3">
                    <button onclick="app.exportCSV()"
                        class="flex items-center gap-2 px-4 py-2.5 rounded-full bg-[#1a1a1a] text-gray-300 hover:text-white hover:bg-[#252525] text-sm font-medium transition-all">
                        <i data-lucide="download" class="w-4 h-4"></i> <span class="hidden sm:inline">Exportar
                            Mês</span>
                    </button>
                    <button onclick="app.openCalendly()"
                        class="flex items-center gap-2 px-4 py-2.5 rounded-full bg-[#1a1a1a] text-gray-300 hover:text-white hover:bg-[#252525] text-sm font-medium transition-all">
                        <i data-lucide="calendar-days" class="w-4 h-4"></i> <span class="hidden sm:inline">Agenda</span>
                    </button>
                    <button
                        class="w-10 h-10 rounded-full bg-[#1a1a1a] text-gray-400 flex items-center justify-center hover:text-white relative">
                        <i data-lucide="bell" class="w-5 h-5"></i>
                        <span class="absolute top-2 right-2 w-2 h-2 bg-neon-pink rounded-full animate-pulse"></span>
                    </button>
                    <button onclick="app.openCalendly()"
                        class="hidden md:flex items-center gap-2 bg-[#d4af37] text-black font-bold px-6 py-2.5 rounded-full hover:bg-[#c4a030] shadow-[0_0_20px_rgba(212,175,55,0.2)] active:scale-95 transition-all">
                        <i data-lucide="phone-call" class="w-4 h-4"></i> Marcar Call
                    </button>
                </div>
            </header>

            <!-- SCROLL AREA -->
            <div class="flex-1 overflow-y-auto px-10 pb-10 space-y-8">

                <!-- KPIS -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <!-- KPI 1 -->
                    <div
                        class="bg-[#141414] p-6 rounded-[2rem] border border-white/5 hover:border-[#39ff14]/20 transition-all group relative">
                        <div
                            class="absolute top-4 right-4 w-10 h-10 bg-neon-green-10 rounded-full flex items-center justify-center text-neon-green">
                            <i data-lucide="dollar-sign" class="w-5 h-5"></i>
                        </div>
                        <p class="text-gray-400 text-sm font-medium mb-2">Faturamento Estimado</p>
                        <h3 class="text-3xl font-syne font-bold text-white mb-4" id="kpi-total">R$ 0,00</h3>
                        <div class="flex items-center gap-2 text-xs font-bold text-neon-green">
                            <i data-lucide="trending-up" class="w-3 h-3"></i> <span id="kpi-trend">+0%</span> <span
                                class="text-gray-500 font-normal ml-1">vs mês passado</span>
                        </div>
                    </div>
                    <!-- KPI 2 -->
                    <div
                        class="bg-[#141414] p-6 rounded-[2rem] border border-white/5 hover:border-[#ff00aa]/20 transition-all group relative">
                        <div
                            class="absolute top-4 right-4 w-10 h-10 bg-neon-pink-10 rounded-full flex items-center justify-center text-neon-pink">
                            <i data-lucide="zap" class="w-5 h-5"></i>
                        </div>
                        <p class="text-gray-400 text-sm font-medium mb-2">Novas Oportunidades</p>
                        <h3 class="text-3xl font-syne font-bold text-white mb-4" id="kpi-count">0</h3>
                        <div class="flex items-center gap-2 text-xs font-bold text-neon-pink">
                            <span id="kpi-urgent">0 urgentes</span> <span class="text-gray-500 font-normal ml-1">precisam de atenção</span>
                        </div>
                    </div>
                    <!-- KPI 3 -->
                    <div
                        class="bg-[#141414] p-6 rounded-[2rem] border border-white/5 hover:border-[#d4af37]/20 transition-all group relative">
                        <div
                            class="absolute top-4 right-4 w-10 h-10 bg-gold-10 rounded-full flex items-center justify-center text-gold">
                            <i data-lucide="message-circle" class="w-5 h-5"></i>
                        </div>
                        <p class="text-gray-400 text-sm font-medium mb-2">Taxa de Resposta</p>
                        <h3 class="text-3xl font-syne font-bold text-white mb-4">92%</h3>
                        <div class="flex items-center gap-2 text-xs font-bold text-gold">
                            Tempo recorde <span class="text-gray-500 font-normal ml-1">12min médio</span>
                        </div>
                    </div>
                </div>

                <!-- TABELA -->
                <div class="space-y-4">
                    <div class="flex items-center justify-between px-2">
                        <h2 class="text-xl font-syne font-bold text-white flex items-center gap-2">
                            Leads Recentes <span id="leads-count-badge"
                                class="text-sm font-inter font-normal text-gray-400 bg-[#1a1a1a] px-2 py-0.5 rounded-full">0</span>
                        </h2>
                        <button onclick="app.setFilter('all')"
                            class="text-xs font-bold text-gray-400 hover:text-white px-3 py-1.5 rounded-full hover:bg-[#1a1a1a] transition-colors">Ver
                            todos</button>
                    </div>

                    <div class="bg-[#141414] rounded-[2rem] overflow-hidden border border-white/5">
                        <table class="w-full text-left">
                            <thead>
                                <tr class="border-b border-white/5 text-gray-500 text-xs uppercase tracking-wider">
                                    <th class="p-6 font-medium pl-8">Lead / Cliente</th>
                                    <th class="p-6 font-medium">Canal</th>
                                    <th class="p-6 font-medium">Status</th>
                                    <th class="p-6 font-medium">Valor</th>
                                    <th class="p-6 font-medium text-right pr-8">Ação</th>
                                </tr>
                            </thead>
                            <tbody id="leads-table-body" class="text-sm">
                                <!-- JS vai preencher aqui. Grug espera. -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- DRAWER (MODAL LATERAL) -->
            <div id="drawer-backdrop" onclick="app.closeDrawer()"
                class="fixed inset-0 bg-black/80 backdrop-blur-sm z-[90] hidden transition-opacity"></div>

            <div id="drawer"
                class="fixed inset-y-0 right-0 w-full md:w-[500px] bg-[#141414] shadow-2xl z-[100] border-l border-white/5 transform translate-x-full transition-transform duration-300 ease-in-out flex flex-col">
                <!-- Conteúdo do Drawer preenchido via JS -->
                <div id="drawer-content" class="h-full flex flex-col"></div>
            </div>

        </main>
    </div>

    <!-- GRUG JS: CÓDIGO SIMPLES -->
    <script>
        // --- GRUG STATE ---
        const state = {
            leads: [],
            filter: 'hoje',
            activeLead: null
        };

        // --- GRUG APP LOGIC ---
        const app = {
            init: () => {
                // Configurar Data
                const dateEl = document.getElementById('current-date');
                if (dateEl) {
                    dateEl.innerText = new Date().toLocaleDateString('pt-BR', { day: 'numeric', month: 'long' });
                }

                // Atalhos de Teclado
                document.addEventListener('keydown', (e) => {
                    if (e.key === 'Escape') app.closeDrawer();
                    if (e.key.toLowerCase() === 'w' && state.activeLead) app.openWhatsApp(state.activeLead);
                });

                // Inicializar ícones (Grug-approved: esperar carregar)
                if (window.initLucide && window.initLucide()) {
                    // OK
                } else {
                    // Retry se Lucide ainda não carregou
                    setTimeout(() => {
                        if (window.initLucide) window.initLucide();
                    }, 500);
                    setTimeout(() => {
                        if (window.initLucide) window.initLucide();
                    }, 1500);
                }
                
                app.loadLeads();
                setInterval(app.loadLeads, 30000); // Atualizar a cada 30s
            },

            injectCalendly: () => {
                if (document.querySelector('script[src*="calendly"]')) return;
                const head = document.querySelector('head');
                const script = document.createElement('script');
                script.src = 'https://assets.calendly.com/assets/external/widget.js';
                head.appendChild(script);
                const css = document.createElement('link');
                css.rel = 'stylesheet';
                css.href = 'https://assets.calendly.com/assets/external/widget.css';
                head.appendChild(css);
            },

            formatCurrency: (val) => {
                if (!val || val === '-') return '-';
                if (typeof val === 'number') {
                    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(val);
                }
                const num = parseFloat(String(val).replace(/[^0-9,]/g, '').replace(',', '.'));
                if (isNaN(num)) return val;
                return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(num);
            },

            getTemperature: (ts) => {
                const diff = (Date.now() - new Date(ts).getTime()) / 3600000; // horas
                if (diff < 2) return { label: "FERVENDO", classes: "text-neon-pink bg-neon-pink-10" };
                if (diff < 24) return { label: "MORNO", classes: "text-gold bg-gold-10" };
                return { label: "FRIO", classes: "text-neon-green bg-neon-green-10" };
            },

            setFilter: (f) => {
                state.filter = f;
                document.querySelectorAll('.nav-btn').forEach(btn => {
                    const isActive = btn.dataset.filter === f;
                    btn.classList.toggle('text-[#d4af37]', isActive);
                    btn.classList.toggle('bg-[#1a1a1a]', isActive);
                    btn.classList.toggle('shadow-[0_0_20px_rgba(212,175,55,0.1)]', isActive);
                    if (!isActive) {
                        btn.classList.add('text-gray-400');
                        btn.classList.remove('bg-[#1a1a1a]');
                    }
                });
                app.render();
            },

            openWhatsApp: (lead) => {
                const phoneMatch = String(lead.contact || lead.email || '').match(/([0-9]{10,15})/);
                const phone = phoneMatch ? phoneMatch[1] : '';
                if (!phone) {
                    app.showToast('Telefone não encontrado', 'error');
                    return;
                }
                const msg = `Oi ${lead.name.split(' ')[0]}, tudo certo? Sobre o job que você pediu no site...`;
                window.open(`https://wa.me/${phone}?text=${encodeURIComponent(msg)}`, '_blank');
            },

            openCalendly: (lead) => {
                app.injectCalendly();
                setTimeout(() => {
                    if (window.Calendly) {
                        window.Calendly.initPopupWidget({
                            url: 'https://calendly.com/gui-magellane/reuniao-de-briefing',
                            prefill: lead ? {
                                name: lead.name || '',
                                email: lead.email || ''
                            } : {}
                        });
                    } else {
                        app.showToast('Calendly carregando... Tente novamente em 2 segundos.', 'error');
                    }
                }, 500);
            },

            exportCSV: () => {
                if (state.leads.length === 0) {
                    app.showToast('Nenhum lead para exportar', 'error');
                    return;
                }
                
                function escapeCSV(val) {
                    if (!val) return '';
                    const str = String(val);
                    if (str.includes(',') || str.includes('"') || str.includes('\n')) {
                        return '"' + str.replace(/"/g, '""') + '"';
                    }
                    return str;
                }
                
                const headers = ['ID', 'Nome', 'Email', 'Contato', 'Mensagem', 'Orçamento', 'Tipo', 'Data'];
                const rows = state.leads.map(l => [
                    l.id,
                    escapeCSV(l.name),
                    escapeCSV(l.email || ''),
                    escapeCSV(l.contact || ''),
                    escapeCSV(l.message || ''),
                    escapeCSV(l.budget || ''),
                    escapeCSV(l.form_type || ''),
                    new Date(l.created_at).toLocaleDateString('pt-BR')
                ]);
                
                const csvContent = [headers.map(escapeCSV), ...rows].map(row => row.join(',')).join('\n');
                const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' });
                const link = document.createElement('a');
                const url = URL.createObjectURL(blob);
                link.setAttribute('href', url);
                link.setAttribute('download', `leads-gui-${new Date().toISOString().split('T')[0]}.csv`);
                link.style.visibility = 'hidden';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                URL.revokeObjectURL(url);
                
                app.showToast('CSV exportado com sucesso!', 'success');
            },

            showToast: (msg, type) => {
                const container = document.getElementById('toast-container');
                const el = document.createElement('div');
                el.className = `flex items-center gap-4 px-6 py-4 rounded-xl bg-[#141414] border shadow-2xl mb-2 animate-bounce ${type === 'error' || type === 'alert' ? 'border-[#ff00aa]/30' : 'border-[#39ff14]/30'}`;
                el.innerHTML = `
                    <div class="p-2 rounded-full ${type === 'error' || type === 'alert' ? 'bg-neon-pink-10 text-neon-pink' : 'bg-neon-green-10 text-neon-green'}">
                        <i data-lucide="${type === 'error' || type === 'alert' ? 'zap' : 'check'}" class="w-5 h-5"></i>
                    </div>
                    <div>
                        <p class="font-bold text-white text-sm">${type === 'error' || type === 'alert' ? 'Atenção!' : 'Sucesso'}</p>
                        <p class="text-gray-400 text-xs">${msg}</p>
                    </div>
                `;
                container.appendChild(el);
                if (window.initLucide) window.initLucide();
                setTimeout(() => el.remove(), 4000);
            },

            openDrawer: (lead) => {
                state.activeLead = lead;
                const drawer = document.getElementById('drawer');
                const backdrop = document.getElementById('drawer-backdrop');
                const content = document.getElementById('drawer-content');

                drawer.classList.remove('translate-x-full');
                backdrop.classList.remove('hidden');

                const phoneMatch = String(lead.contact || lead.email || '').match(/([0-9]{10,15})/);
                const phone = phoneMatch ? phoneMatch[1] : '';
                const value = lead.budget ? app.formatCurrency(lead.budget) : 'A definir';
                const notes = lead.message || 'Sem observações.';

                content.innerHTML = `
                    <div class="p-8 flex items-center justify-between border-b border-white/5">
                       <h2 class="text-2xl font-syne font-bold text-white">${app.escapeHtml(lead.name)}</h2>
                       <button onclick="app.closeDrawer()" class="p-2 hover:bg-white/5 rounded-full text-gray-400">
                         <i data-lucide="x" class="w-6 h-6"></i>
                       </button>
                    </div>
                    <div class="p-8 flex-1 overflow-y-auto space-y-8">
                       <div class="p-8 rounded-3xl bg-[#0f0f0f] border border-white/5 text-center relative overflow-hidden">
                          <div class="absolute top-0 right-0 w-32 h-32 bg-gold-10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2"></div>
                          <p class="text-gray-500 text-xs uppercase tracking-widest mb-2">Valor do Projeto</p>
                          <h3 class="text-5xl font-syne font-bold text-[#d4af37] mb-6">${value}</h3>
                          <div class="grid grid-cols-1 gap-3">
                            ${phone ? `<button onclick='app.openWhatsApp(${JSON.stringify(lead)})' class="w-full py-4 bg-[#25D366] text-black font-bold rounded-xl flex items-center justify-center gap-3 hover:scale-[1.02] transition-transform shadow-lg shadow-green-900/20">
                               <i data-lucide="message-circle" class="w-5 h-5"></i> Conversar no WhatsApp
                            </button>` : ''}
                            <button onclick='app.openCalendly(${JSON.stringify(lead)})' class="w-full py-4 bg-[#1a1a1a] text-white border border-white/10 font-bold rounded-xl flex items-center justify-center gap-3 hover:bg-[#252525] transition-colors">
                               <i data-lucide="calendar-days" class="w-5 h-5"></i> Marcar Reunião Agora
                            </button>
                          </div>
                       </div>
                       <div>
                          <h4 class="text-sm font-bold text-white mb-3 uppercase tracking-wider text-gray-500">Briefing Inicial</h4>
                          <p class="text-gray-300 text-lg leading-relaxed font-light italic bg-[#0f0f0f] p-6 rounded-2xl border border-white/5">&quot;${app.escapeHtml(notes)}&quot;</p>
                       </div>
                    </div>
                `;
                if (window.initLucide) window.initLucide();
            },

            closeDrawer: () => {
                state.activeLead = null;
                document.getElementById('drawer').classList.add('translate-x-full');
                document.getElementById('drawer-backdrop').classList.add('hidden');
            },

            escapeHtml: (text) => {
                if (!text) return '';
                const div = document.createElement('div');
                div.textContent = text;
                return div.innerHTML;
            },

            loadLeads: async () => {
                try {
                    const res = await fetch('/api/leads');
                    if (!res.ok) {
                        if (res.status === 401) {
                            window.location.reload();
                            return;
                        }
                        app.showToast('Erro ao carregar leads', 'error');
                        return;
                    }
                    const data = await res.json();
                    state.leads = (data.leads || []).map(lead => ({
                        ...lead,
                        timestamp: new Date(lead.created_at).getTime(),
                        source: lead.form_type === 'modal' ? 'form' : (lead.form_type || 'form'),
                        phone: lead.contact || lead.email || '',
                        value: lead.budget ? parseFloat(String(lead.budget).replace(/[^0-9,]/g, '').replace(',', '.')) || 0 : 0,
                        notes: lead.message || '',
                        contacted: false
                    }));
                    app.render();
                } catch (error) {
                    console.error('Erro ao carregar leads:', error);
                    app.showToast('Erro ao carregar leads', 'error');
                }
            },

            render: () => {
                // Filtra Leads
                const filtered = state.leads.filter(l => {
                    const diff = Date.now() - l.timestamp;
                    if (state.filter === 'hoje') return diff < 86400000;
                    if (state.filter === 'quentes') return diff < 7200000; // 2h
                    if (state.filter === 'whatsapp') {
                        const phoneMatch = String(l.contact || l.email || '').match(/([0-9]{10,15})/);
                        return phoneMatch !== null;
                    }
                    return true;
                });

                // Atualiza KPIs
                const totalValue = state.leads.reduce((acc, l) => acc + (l.value || 0), 0);
                const quentesCount = state.leads.filter(l => {
                    const diff = Date.now() - l.timestamp;
                    return diff < 7200000; // 2h
                }).length;
                
                document.getElementById('kpi-total').innerText = app.formatCurrency(totalValue);
                document.getElementById('kpi-count').innerText = state.leads.length;
                document.getElementById('kpi-urgent').innerText = `${quentesCount} urgentes`;
                document.getElementById('leads-count-badge').innerText = filtered.length;

                // Renderiza Tabela (O jeito Grug: innerHTML limpo)
                const tbody = document.getElementById('leads-table-body');
                if (filtered.length === 0) {
                    tbody.innerHTML = '<tr><td colspan="5" class="p-8 text-center text-gray-500">Nenhum lead encontrado.</td></tr>';
                } else {
                    tbody.innerHTML = filtered.map(lead => {
                        const temp = app.getTemperature(lead.created_at);
                        const phoneMatch = String(lead.contact || lead.email || '').match(/([0-9]{10,15})/);
                        const hasPhone = phoneMatch !== null;
                        return `
                            <tr class="group cursor-pointer hover:bg-white/[0.02] transition-colors border-b border-white/5 last:border-0" onclick='app.openDrawer(${JSON.stringify(lead)})'>
                                <td class="p-6 pl-8">
                                    <div class="flex items-center gap-3">
                                        <div class="w-10 h-10 rounded-full flex items-center justify-center font-bold text-xs relative bg-neon-pink-10 text-neon-pink">
                                            ${app.escapeHtml(lead.name).charAt(0).toUpperCase()}
                                            <span class="absolute -top-1 -right-1 w-3 h-3 bg-neon-pink border-2 border-[#141414] rounded-full"></span>
                                        </div>
                                        <div>
                                            <p class="text-white font-medium group-hover:text-[#d4af37] transition-colors">${app.escapeHtml(lead.name)}</p>
                                            <p class="text-xs text-gray-500">ID #${lead.id}</p>
                                        </div>
                                    </div>
                                </td>
                                <td class="p-6">
                                    <div class="flex items-center gap-2 text-gray-400">
                                        <i data-lucide="${lead.form_type === 'modal' ? 'layout-dashboard' : 'message-circle'}" class="w-4 h-4"></i>
                                        <span class="capitalize">${lead.form_type || 'form'}</span>
                                    </div>
                                </td>
                                <td class="p-6">
                                    <span class="px-3 py-1 rounded-full text-xs font-bold ${temp.classes}">${temp.label}</span>
                                </td>
                                <td class="p-6 font-mono text-gray-300">${lead.budget ? app.formatCurrency(lead.budget) : '-'}</td>
                                <td class="p-6 text-right pr-8">
                                    ${hasPhone ? `<button onclick='event.stopPropagation(); app.openWhatsApp(${JSON.stringify(lead)})' class="w-10 h-10 rounded-full border border-white/10 flex items-center justify-center text-gray-400 hover:text-neon-green hover:border-neon-green hover:bg-neon-green-10 transition-all ml-auto">
                                        <i data-lucide="message-circle" class="w-4 h-4"></i>
                                    </button>` : '<span class="text-gray-500 text-xs">-</span>'}
                                </td>
                            </tr>
                        `;
                    }).join('');
                }

                // Re-inicializa ícones novos
                if (window.initLucide) window.initLucide();
            }
        };

        // Grug Inicializa
        app.init();
    </script>
</body>

</html>'''
# Painel admin (HTML/CSS/JS vanilla - Grug-approved)
@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        return render_template_string(LOGIN_HTML), 200
    return render_template_string(ADMIN_HTML), 200

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)

