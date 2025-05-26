"""SAML Authentication Backend for SSO POC

This module implements SAML 2.0 authentication using OneLogin's python3-saml library.
It provides secure authentication, role-based access control (RBAC), and session management
for the SAML-based application in the SSO proof of concept.
"""

import os
import json
from flask import Flask, request, redirect, session, jsonify, url_for
from flask_cors import CORS
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.utils import OneLogin_Saml2_Utils
from functools import wraps
from urllib.parse import urlparse

# Initialize Flask application
app = Flask(__name__)
# Secret key for session encryption - should be set via environment variable in production
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')

# Configure secure session settings
# Session cookies are used to maintain authentication state
app.config['SESSION_COOKIE_NAME'] = 'saml_session'  # Custom cookie name for SAML sessions
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to session cookie
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection while allowing IdP redirects
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # Session timeout: 1 hour

# Enable CORS for frontend application
# In production, origins should be restricted to actual frontend domains
CORS(app, supports_credentials=True, origins=['http://localhost:3001'])

def init_saml_auth(req):
    """
    Initialize SAML authentication object with configuration.
    
    Args:
        req: Prepared request object containing SAML parameters
        
    Returns:
        OneLogin_Saml2_Auth: Configured SAML auth object
    """
    auth = OneLogin_Saml2_Auth(req, custom_base_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'saml'))
    return auth

def prepare_flask_request(request):
    """
    Prepare Flask request for SAML processing.
    
    Handles X-Forwarded headers from reverse proxy (nginx) to ensure
    proper URL construction for SAML assertions and redirects.
    
    Args:
        request: Flask request object
        
    Returns:
        dict: Request data formatted for SAML library
    """
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
    """
    Decorator to enforce authentication on protected endpoints.
    
    Returns 401 Unauthorized if user is not authenticated.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated', False):
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def check_role_hierarchy(user_roles, required_role):
    """
    Check if user has required role considering role hierarchy.
    
    Implements hierarchical RBAC where higher roles inherit permissions
    of lower roles (admin > editor > viewer).
    
    Args:
        user_roles: List of roles assigned to the user
        required_role: The role required to access the resource
        
    Returns:
        bool: True if user has required role or a higher role
    """
    # Define role hierarchy - higher roles inherit permissions of lower roles
    role_hierarchy = {
        'admin': ['editor', 'viewer'],  # Admin can do everything editor and viewer can
        'editor': ['viewer'],            # Editor can do everything viewer can
        'viewer': []                     # Viewer has no inherited permissions
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
    """
    Decorator factory to enforce role-based access control.
    
    Creates a decorator that checks if the authenticated user has the
    required role (or a higher role in the hierarchy) before allowing
    access to the endpoint.
    
    Args:
        role: The minimum role required to access the endpoint
        
    Returns:
        decorator: Function decorator that enforces the role requirement
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # First check authentication
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
    """
    Get current user information from session.
    
    Returns user details if authenticated, otherwise returns
    authenticated: false.
    
    Returns:
        JSON response with user information or authentication status
    """
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
    """
    Example protected endpoint requiring authentication.
    
    Demonstrates basic authentication requirement without
    specific role requirements.
    """
    return jsonify({
        'message': 'This is a protected resource',
        'user': session.get('username', '')
    })

@app.route('/api/admin')
@require_role('admin')
def admin_resource():
    """
    Admin-only endpoint demonstrating role-based access control.
    
    Only users with 'admin' role can access this endpoint.
    """
    return jsonify({
        'message': 'This is an admin-only resource',
        'user': session.get('username', '')
    })

@app.route('/api/editor')
@require_role('editor')
def editor_resource():
    """
    Editor endpoint demonstrating hierarchical RBAC.
    
    Accessible by users with 'editor' role or higher (admin).
    """
    return jsonify({
        'message': 'This is an editor-only resource',
        'user': session.get('username', ''),
        'data': 'You can edit this content'
    })

@app.route('/saml/login')
def saml_login():
    """
    Initiate SAML authentication flow.
    
    Redirects user to Identity Provider (IdP) for authentication.
    """
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    return redirect(auth.login())

@app.route('/saml/callback', methods=['POST'])
def saml_callback():
    """
    Handle SAML authentication response from IdP.
    
    Processes the SAML assertion, extracts user attributes and roles,
    establishes user session, and redirects to frontend application.
    
    This endpoint handles the special case of duplicate attribute names
    (common with role attributes) by manually parsing the SAML response.
    """
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
        # Handle duplicate attribute error (common with multiple role values)
        # This occurs when IdP sends multiple values for the same attribute name
        if "duplicated Name" in str(e):
            # Parse SAML response manually to handle duplicate attributes
            import xml.etree.ElementTree as ET
            import base64
            
            saml_response = request.form.get('SAMLResponse')
            decoded = base64.b64decode(saml_response)
            root = ET.fromstring(decoded)
            
            # Extract attributes manually from XML
            attributes = {}
            # Define SAML 2.0 XML namespaces
            namespaces = {
                'saml': 'urn:oasis:names:tc:SAML:2.0:assertion',
                'samlp': 'urn:oasis:names:tc:SAML:2.0:protocol'
            }
            
            # Parse all SAML attributes from the assertion
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
                        # Handle multiple attributes with same name (e.g., multiple roles)
                        # This is the case that causes the "duplicated Name" error
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
        # Different IdPs use different attribute names for roles
        roles = []
        # Common role attribute names used by various IdPs
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
        
        # Establish authenticated session with user data
        session['authenticated'] = True
        session['username'] = attributes.get('username', [''])[0] if attributes.get('username') else ''
        session['email'] = attributes.get('email', [''])[0] if attributes.get('email') else ''
        session['roles'] = roles
        # Store SAML-specific data for logout
        session['samlNameId'] = nameid
        session['samlSessionIndex'] = auth.get_session_index() if hasattr(auth, 'get_session_index') else None
        
        # Store sanitized user attributes for frontend use
        session['samlUserdata'] = {
            'username': session['username'],
            'email': session['email'],
            'roles': roles
        }
        
        # Log authentication success for monitoring
        print(f"SAML Auth Success - User: {session['username']}, Roles: {roles}")
        print(f"All SAML Attributes: {attributes}")
        
        # Debug mode: Save SAML response for troubleshooting
        # Remove this block in production
        import base64
        saml_response = request.form.get('SAMLResponse')
        if saml_response:
            try:
                decoded = base64.b64decode(saml_response)
                # Save decoded SAML response for analysis
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
    """
    Initiate SAML Single Logout (SLO) flow.
    
    Sends logout request to IdP with session information to ensure
    proper logout from both SP and IdP.
    """
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    
    # Retrieve SAML session information needed for logout
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
    """
    Handle SAML Single Logout Service (SLS) callback.
    
    Processes logout response from IdP and clears local session.
    Handles both logout requests and responses.
    """
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    
    # Check if this is a SAML logout request/response
    if 'SAMLRequest' not in request.args and 'SAMLResponse' not in request.args:
        # Direct logout without SAML - just clear session
        session.clear()
        return redirect('http://localhost:3001/')
    
    try:
        # Process SAML logout response and clear session
        url = auth.process_slo(delete_session_cb=lambda: session.clear())
        errors = auth.get_errors()
        if not errors:
            # Successful logout - redirect to frontend
            return redirect('http://localhost:3001/')
        else:
            error_reason = auth.get_last_error_reason()
            return jsonify({'error': error_reason}), 400
    except Exception as e:
        # Fallback: ensure session is cleared even if SLO fails
        # This prevents users from being stuck in a logged-in state
        session.clear()
        return redirect('http://localhost:3001/')


if __name__ == '__main__':
    # Run Flask development server
    # In production, use a proper WSGI server like Gunicorn
    app.run(host='0.0.0.0', port=5000, debug=True)