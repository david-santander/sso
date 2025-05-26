import os
import json
from flask import Flask, request, redirect, session, jsonify, url_for
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth
from functools import wraps
import jwt
from jwt import PyJWKClient

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')

# Configure session - use Flask's built-in cookie-based sessions
app.config['SESSION_COOKIE_NAME'] = 'oidc_session'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour

CORS(app, supports_credentials=True, origins=['http://localhost:4001'])

oauth = OAuth(app)

OIDC_CLIENT_ID = os.environ.get('OIDC_CLIENT_ID', 'app2-oidc')
OIDC_CLIENT_SECRET = os.environ.get('OIDC_CLIENT_SECRET', 'secret')
OIDC_ISSUER = os.environ.get('OIDC_ISSUER', 'http://keycloak:8080/realms/sso-poc')
OIDC_ISSUER_PUBLIC = os.environ.get('OIDC_ISSUER_PUBLIC', 'http://localhost:8080/realms/sso-poc')
OIDC_REDIRECT_URI = os.environ.get('OIDC_REDIRECT_URI', 'http://localhost:4000/oidc/callback')

# Configure OAuth with explicit endpoints to avoid metadata discovery issues
oidc = oauth.register(
    'oidc',
    client_id=OIDC_CLIENT_ID,
    client_secret=OIDC_CLIENT_SECRET,
    access_token_url=f'{OIDC_ISSUER}/protocol/openid-connect/token',
    authorize_url=f'{OIDC_ISSUER_PUBLIC}/protocol/openid-connect/auth',
    jwks_uri=f'{OIDC_ISSUER}/protocol/openid-connect/certs',
    client_kwargs={
        'scope': 'openid email profile roles'
    }
)

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def check_role_hierarchy(user_roles, required_role):
    """Check if user has required role considering role hierarchy"""
    # Define role hierarchy - higher roles inherit permissions of lower roles
    role_hierarchy = {
        'admin': ['editor', 'viewer'],
        'editor': ['viewer'],
        'viewer': []
    }
    
    # Direct role check
    if required_role in user_roles:
        return True
    
    # Check hierarchical roles
    for user_role in user_roles:
        if user_role in role_hierarchy and required_role in role_hierarchy[user_role]:
            return True
    
    return False

def require_role(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user' not in session:
                return jsonify({'error': 'Authentication required'}), 401
            
            user_roles = session.get('user', {}).get('roles', [])
            
            # Check if user has the required role (including hierarchy)
            if not check_role_hierarchy(user_roles, role):
                return jsonify({'error': f'Role {role} required. User has roles: {user_roles}'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def decode_token(token):
    try:
        jwks_client = PyJWKClient(f'{OIDC_ISSUER}/protocol/openid-connect/certs')
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        
        # The token will have the public issuer URL, so we need to validate against that
        data = jwt.decode(
            token,
            signing_key.key,
            algorithms=['RS256'],
            audience=OIDC_CLIENT_ID,
            issuer=OIDC_ISSUER_PUBLIC,
            options={"verify_exp": True}
        )
        return data
    except Exception as e:
        print(f"Token decode error: {e}")
        return None


@app.route('/api/user')
def get_user():
    if 'user' in session:
        return jsonify({
            'authenticated': True,
            'username': session['user'].get('preferred_username', session['user'].get('email', '')),
            'email': session['user'].get('email', ''),
            'roles': session['user'].get('roles', []),
            'attributes': session['user']
        })
    return jsonify({'authenticated': False})

@app.route('/api/protected')
@require_auth
def protected_resource():
    return jsonify({
        'message': 'This is a protected resource',
        'user': session['user'].get('preferred_username', session['user'].get('email', ''))
    })

@app.route('/api/admin')
@require_role('admin')
def admin_resource():
    return jsonify({
        'message': 'This is an admin-only resource',
        'user': session['user'].get('preferred_username', session['user'].get('email', ''))
    })

@app.route('/api/editor')
@require_role('editor')
def editor_resource():
    return jsonify({
        'message': 'This is an editor-only resource',
        'user': session['user'].get('preferred_username', session['user'].get('email', '')),
        'data': 'You can edit this content'
    })

@app.route('/oidc/login')
def oidc_login():
    # Use the configured redirect URI instead of generating it
    redirect_uri = OIDC_REDIRECT_URI
    return oidc.authorize_redirect(redirect_uri)

@app.route('/oidc/callback')
def oidc_callback():
    try:
        token = oidc.authorize_access_token()
        
        id_token = token.get('id_token')
        if id_token:
            claims = decode_token(id_token)
            if claims:
                user_info = {
                    'sub': claims.get('sub'),
                    'email': claims.get('email'),
                    'preferred_username': claims.get('preferred_username'),
                    'name': claims.get('name'),
                    'roles': claims.get('realm_access', {}).get('roles', [])
                }
                
                if 'resource_access' in claims and OIDC_CLIENT_ID in claims['resource_access']:
                    client_roles = claims['resource_access'][OIDC_CLIENT_ID].get('roles', [])
                    user_info['roles'].extend(client_roles)
                
                session['user'] = user_info
                session['tokens'] = {
                    'access_token': token.get('access_token'),
                    'id_token': id_token,
                    'refresh_token': token.get('refresh_token')
                }
        
        return redirect('http://localhost:4001/')
    except Exception as e:
        print(f"OIDC callback error: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/oidc/logout')
def oidc_logout():
    id_token = session.get('tokens', {}).get('id_token')
    session.clear()
    
    if id_token:
        logout_url = f"{OIDC_ISSUER}/protocol/openid-connect/logout"
        params = {
            'id_token_hint': id_token,
            'post_logout_redirect_uri': 'http://localhost:4001'
        }
        logout_url_with_params = logout_url + '?' + '&'.join([f'{k}={v}' for k, v in params.items()])
        return redirect(logout_url_with_params)
    
    return redirect('http://localhost:4001/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)