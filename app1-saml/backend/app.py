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
            if not session.get('authenticated', False):
                return jsonify({'error': 'Authentication required'}), 401
            
            user_roles = session.get('roles', [])
            
            # Check if user has the required role (including hierarchy)
            if not check_role_hierarchy(user_roles, role):
                return jsonify({'error': f'Role {role} required. User has roles: {user_roles}'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@app.route('/api/user')
def get_user():
    if session.get('authenticated', False):
        return jsonify({
            'authenticated': True,
            'username': session.get('username', ''),
            'email': session.get('email', ''),
            'roles': session.get('roles', []),
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
        'user': session.get('username', '')
    })

@app.route('/api/editor')
@require_role('editor')
def editor_resource():
    return jsonify({
        'message': 'This is an editor-only resource',
        'user': session.get('username', ''),
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
    
    attributes = None
    nameid = None
    errors = []
    
    try:
        auth.process_response()
        errors = auth.get_errors()
        if not errors:
            attributes = auth.get_attributes()
            nameid = auth.get_nameid()
    except Exception as e:
        # Handle duplicate attribute error by getting raw response
        if "duplicated Name" in str(e):
            # Get attributes manually from the SAML response
            import xml.etree.ElementTree as ET
            import base64
            
            saml_response = request.form.get('SAMLResponse')
            decoded = base64.b64decode(saml_response)
            root = ET.fromstring(decoded)
            
            # Extract attributes manually
            attributes = {}
            namespaces = {
                'saml': 'urn:oasis:names:tc:SAML:2.0:assertion',
                'samlp': 'urn:oasis:names:tc:SAML:2.0:protocol'
            }
            
            # Find all attributes
            for attr in root.findall('.//saml:Attribute', namespaces):
                name = attr.get('Name')
                values = []
                for value in attr.findall('saml:AttributeValue', namespaces):
                    if value.text:
                        values.append(value.text)
                if name and values:
                    if name not in attributes:
                        attributes[name] = values
                    else:
                        # Handle multiple attributes with same name (e.g., roles)
                        if isinstance(attributes[name], list):
                            attributes[name].extend(values)
                        else:
                            attributes[name] = [attributes[name]] + values
            
            # Get NameID
            nameid_elem = root.find('.//saml:NameID', namespaces)
            nameid = nameid_elem.text if nameid_elem is not None else ''
            
            # Process the attributes as if auth.process_response() succeeded
            errors = []
        else:
            return jsonify({'error': str(e)}), 400
    
    if not errors and attributes is not None:
        # Extract roles from SAML attributes
        roles = []
        # Try different possible role attribute names
        role_attrs = ['userRoles', 'Role', 'roles', 'memberOf', 'groups', 'role']
        for attr_name in role_attrs:
            if attr_name in attributes:
                attr_value = attributes[attr_name]
                if isinstance(attr_value, list):
                    roles.extend(attr_value)
                else:
                    roles.append(attr_value)
        
        # Remove duplicates and ensure we have a clean list
        roles = list(set(roles))
        
        # Store user data in session
        session['authenticated'] = True
        session['username'] = attributes.get('username', [''])[0] if attributes.get('username') else ''
        session['email'] = attributes.get('email', [''])[0] if attributes.get('email') else ''
        session['roles'] = roles
        session['samlNameId'] = nameid
        session['samlSessionIndex'] = auth.get_session_index() if hasattr(auth, 'get_session_index') else None
        
        # Store full attributes as simple dict
        session['samlUserdata'] = {
            'username': session['username'],
            'email': session['email'],
            'roles': roles
        }
        
        # Log for debugging
        print(f"SAML Auth Success - User: {session['username']}, Roles: {roles}")
        print(f"All SAML Attributes: {attributes}")
        
        # Debug: Log the raw SAML response
        import base64
        saml_response = request.form.get('SAMLResponse')
        if saml_response:
            try:
                decoded = base64.b64decode(saml_response)
                # Save to file for analysis
                with open('/tmp/saml_response_debug.xml', 'wb') as f:
                    f.write(decoded)
                print("SAML Response saved to /tmp/saml_response_debug.xml")
            except Exception as e:
                print(f"Error saving SAML response: {e}")
        
        # Redirect to frontend
        return redirect('http://localhost:3001/')
    else:
        error_reason = auth.get_last_error_reason() if hasattr(auth, 'get_last_error_reason') else 'Authentication failed'
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
    
    print(f"Logout - NameID: {name_id}, SessionIndex: {session_index}")
    
    logout_url = auth.logout(name_id=name_id, session_index=session_index,
                            nq=name_id_nq, name_id_format=name_id_format,
                            spnq=name_id_spnq, return_to='http://localhost:3001/')
    
    print(f"Logout URL: {logout_url}")
    
    return redirect(logout_url)

@app.route('/saml/sls', methods=['GET', 'POST'])
def saml_sls():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    
    # Check if we have SAML parameters in the request
    if 'SAMLRequest' not in request.args and 'SAMLResponse' not in request.args:
        # No SAML parameters, just clear session and redirect
        session.clear()
        return redirect('http://localhost:3001/')
    
    try:
        url = auth.process_slo(delete_session_cb=lambda: session.clear())
        errors = auth.get_errors()
        if not errors:
            return redirect('http://localhost:3001/')
        else:
            error_reason = auth.get_last_error_reason()
            return jsonify({'error': error_reason}), 400
    except Exception as e:
        # If there's an error, clear session and redirect anyway
        session.clear()
        return redirect('http://localhost:3001/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)