# SAML vs OIDC: Comprehensive Comparison

## Executive Summary

This document provides a detailed comparison between SAML 2.0 and OpenID Connect (OIDC) based on our PoC implementation. Both protocols achieve Single Sign-On (SSO) but with different approaches and trade-offs.

## Protocol Overview

### SAML 2.0 (Security Assertion Markup Language)
- **Released**: 2005
- **Foundation**: XML-based
- **Primary Use**: Enterprise SSO
- **Token Format**: XML Assertions

### OpenID Connect (OIDC)
- **Released**: 2014
- **Foundation**: Built on OAuth 2.0
- **Primary Use**: Modern web and mobile applications
- **Token Format**: JSON Web Tokens (JWT)

## Detailed Comparison

### 1. Architecture & Design

#### SAML
- **Design Philosophy**: Enterprise-focused, comprehensive
- **Message Format**: XML with digital signatures
- **Bindings**: HTTP POST, HTTP Redirect, SOAP
- **Metadata**: XML-based service provider and identity provider metadata

#### OIDC
- **Design Philosophy**: Simple, developer-friendly
- **Message Format**: JSON over HTTPS
- **Flows**: Authorization Code, Implicit, Hybrid
- **Discovery**: Well-known configuration endpoints

### 2. Authentication Flow

#### SAML SP-Initiated Flow
```
User → SP → IdP → User Auth → IdP → SP (POST Assertion) → User
```

1. User accesses protected resource
2. SP generates AuthnRequest
3. Redirects to IdP
4. User authenticates
5. IdP posts assertion to SP
6. SP validates and creates session

#### OIDC Authorization Code Flow
```
User → RP → OP → User Auth → OP → RP (Code) → RP ↔ OP (Tokens) → User
```

1. User accesses protected resource
2. RP redirects to OP with auth request
3. User authenticates
4. OP redirects back with code
5. RP exchanges code for tokens
6. RP validates tokens and creates session

### 3. Message/Token Examples

#### SAML Assertion (Simplified)
```xml
<saml:Assertion>
  <saml:Subject>
    <saml:NameID>user@example.com</saml:NameID>
  </saml:Subject>
  <saml:AttributeStatement>
    <saml:Attribute Name="Role">
      <saml:AttributeValue>admin</saml:AttributeValue>
    </saml:Attribute>
  </saml:AttributeStatement>
</saml:Assertion>
```

#### OIDC ID Token (JWT)
```json
{
  "iss": "http://localhost:8080/realms/sso-poc",
  "sub": "user-id-123",
  "aud": "app2-oidc",
  "exp": 1634567890,
  "iat": 1634567590,
  "email": "user@example.com",
  "realm_access": {
    "roles": ["admin"]
  }
}
```

### 4. Security Mechanisms

#### SAML
- **Assertion Signing**: XML Digital Signatures
- **Encryption**: Optional assertion encryption
- **Trust**: Based on exchanged certificates
- **Replay Prevention**: AssertionID and time conditions

#### OIDC
- **Token Signing**: JWT signatures (typically RS256)
- **Encryption**: Optional JWT encryption
- **Trust**: Based on public key discovery
- **Replay Prevention**: Token expiration and nonce

### 5. Implementation Complexity

#### SAML
- **Setup**: More complex configuration
- **Libraries**: Mature but complex (e.g., python3-saml)
- **Debugging**: XML parsing and signature validation challenges
- **Metadata**: Requires metadata exchange

#### OIDC
- **Setup**: Simpler configuration
- **Libraries**: Modern and straightforward (e.g., Authlib)
- **Debugging**: JSON and standard HTTP
- **Discovery**: Automatic via well-known endpoints

### 6. Role-Based Access Control (RBAC)

#### SAML Implementation
```python
# From our SAML app
user_roles = session.get('samlUserdata', {}).get('Role', [])
if role not in user_roles:
    return jsonify({'error': f'Role {role} required'}), 403
```

#### OIDC Implementation
```python
# From our OIDC app
claims = decode_token(id_token)
user_roles = claims.get('realm_access', {}).get('roles', [])
if role not in user_roles:
    return jsonify({'error': f'Role {role} required'}), 403
```

### 7. Logout Mechanisms

#### SAML Single Logout (SLO)
- Complex coordination between SP and IdP
- Requires logout requests/responses
- Can be unreliable in practice

#### OIDC Logout
- Simple redirect to end_session_endpoint
- Optional ID token hint
- Post-logout redirect URI

### 8. Use Case Recommendations

#### Choose SAML when:
- Integrating with enterprise systems
- Working with legacy applications
- Compliance requires SAML
- Partners only support SAML

#### Choose OIDC when:
- Building modern web applications
- Developing mobile applications
- Need simple integration
- Want RESTful APIs

### 9. Pros and Cons Summary

#### SAML Pros
- Mature and widely supported in enterprises
- Comprehensive security features
- Rich attribute statements
- Well-established in corporate environments

#### SAML Cons
- Complex XML processing
- Verbose messages
- Difficult debugging
- Not mobile-friendly

#### OIDC Pros
- Simple and developer-friendly
- JSON-based and REST-like
- Mobile application support
- Modern token format (JWT)

#### OIDC Cons
- Newer, less enterprise adoption
- Requires HTTPS everywhere
- Token size limitations
- Less feature-rich than SAML

## Performance Considerations

Based on our PoC:

### Message Size
- SAML Assertion: ~2-5 KB (XML)
- OIDC ID Token: ~0.5-1 KB (JWT)

### Round Trips
- SAML: 2-3 HTTP requests
- OIDC: 3-4 HTTP requests (including token exchange)

### Processing Overhead
- SAML: XML parsing and signature validation
- OIDC: JWT validation and JSON parsing

## Migration Considerations

### From SAML to OIDC
1. Map SAML attributes to OIDC claims
2. Update application authentication logic
3. Configure OIDC client in IdP
4. Implement parallel support during transition

### Coexistence Strategy
- Use Keycloak or similar IdP supporting both
- Implement protocol detection in applications
- Gradual migration by application

## Conclusion

Both SAML and OIDC successfully implement SSO with RBAC. The choice depends on:

- **Technical Requirements**: Legacy vs. modern stack
- **Organizational Context**: Enterprise vs. startup
- **Developer Experience**: Complex but complete vs. simple but sufficient
- **Future Direction**: Moving towards API-first architectures favors OIDC

Our PoC demonstrates that Keycloak effectively supports both protocols, allowing organizations to choose based on their specific needs while maintaining a single identity infrastructure.