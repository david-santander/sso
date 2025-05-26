import os
import json
from flask import Flask, request, redirect, session, jsonify, url_for
from flask_cors import CORS
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.utils import OneLogin_Saml2_Utils
from functools import wraps
from urllib.parse import urlparse

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')

# Configure session - use Flask's built-in cookie-based sessions
app.config['SESSION_COOKIE_NAME'] = 'saml_session'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour

CORS(app, supports_credentials=True, origins=['http://localhost:3001'])

def init_saml_auth(req):
    auth = OneLogin_Saml2_Auth(req, custom_base_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'saml'))
    return auth

def prepare_flask_request(request):
    # Handle X-Forwarded headers from nginx proxy
    forwarded_host = request.headers.get('X-Forwarded-Host', request.headers.get('Host'))
    forwarded_proto = request.headers.get('X-Forwarded-Proto', request.scheme)
    
    # Extract port from forwarded host if present
    if forwarded_host and ':' in forwarded_host:
        host, port = forwarded_host.rsplit(':', 1)
    else:
        host = forwarded_host
        port = '443' if forwarded_proto == 'https' else '80'
    
    return {
        'https': 'on' if forwarded_proto == 'https' else 'off',
        'http_host': forwarded_host,
        'server_port': port,
        'script_name': request.path,
        'get_data': request.args.copy(),
        'post_data': request.form.copy()
    }

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated', False):
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def require_role(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('authenticated', False):
                return jsonify({'error': 'Authentication required'}), 401
            
            # For now, disable role checking since we removed roles from SAML
            # Always return 403 for role-protected endpoints
            return jsonify({'error': f'Role {role} required - roles not implemented in this POC'}), 403
        return decorated_function
    return decorator


@app.route('/api/user')
def get_user():
    if session.get('authenticated', False):
        return jsonify({
            'authenticated': True,
            'username': session.get('username', ''),
            'email': session.get('email', ''),
            'roles': [],
            'attributes': session.get('samlUserdata', {})
        })
    return jsonify({'authenticated': False})

@app.route('/api/protected')
@require_auth
def protected_resource():
    return jsonify({
        'message': 'This is a protected resource',
        'user': session.get('username', '')
    })

@app.route('/api/admin')
@require_role('admin')
def admin_resource():
    return jsonify({
        'message': 'This is an admin-only resource',
        'user': session['samlUserdata'].get('username', [''])[0]
    })

@app.route('/api/editor')
@require_role('editor')
def editor_resource():
    return jsonify({
        'message': 'This is an editor-only resource',
        'user': session['samlUserdata'].get('username', [''])[0],
        'data': 'You can edit this content'
    })

@app.route('/saml/login')
def saml_login():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    return redirect(auth.login())

@app.route('/saml/callback', methods=['POST'])
def saml_callback():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    auth.process_response()
    
    errors = auth.get_errors()
    if not errors:
        # Get attributes and ensure they're serializable
        attributes = auth.get_attributes()
        
        # Store user data in session
        session['authenticated'] = True
        session['username'] = attributes.get('username', [''])[0] if attributes.get('username') else ''
        session['email'] = attributes.get('email', [''])[0] if attributes.get('email') else ''
        session['samlNameId'] = auth.get_nameid()
        session['samlSessionIndex'] = auth.get_session_index()
        
        # Store full attributes as simple dict
        session['samlUserdata'] = {
            'username': session['username'],
            'email': session['email']
        }
        
        # Redirect to frontend
        return redirect('http://localhost:3001/')
    else:
        error_reason = auth.get_last_error_reason()
        return jsonify({'error': error_reason}), 400

@app.route('/saml/logout')
def saml_logout():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    
    name_id = session_index = name_id_format = name_id_nq = name_id_spnq = None
    if 'samlNameId' in session:
        name_id = session['samlNameId']
    if 'samlSessionIndex' in session:
        session_index = session['samlSessionIndex']
    if 'samlNameIdFormat' in session:
        name_id_format = session['samlNameIdFormat']
    if 'samlNameIdNameQualifier' in session:
        name_id_nq = session['samlNameIdNameQualifier']
    if 'samlNameIdSPNameQualifier' in session:
        name_id_spnq = session['samlNameIdSPNameQualifier']
    
    return redirect(auth.logout(name_id=name_id, session_index=session_index,
                                nq=name_id_nq, name_id_format=name_id_format,
                                spnq=name_id_spnq))

@app.route('/saml/sls', methods=['GET', 'POST'])
def saml_sls():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    url = auth.process_slo(delete_session_cb=lambda: session.clear())
    errors = auth.get_errors()
    if not errors:
        return redirect('/')
    else:
        error_reason = auth.get_last_error_reason()
        return jsonify({'error': error_reason}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)