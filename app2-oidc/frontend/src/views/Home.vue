<template>
  <div class="home">
    <h2>Welcome to OIDC RP Demo Application</h2>
    
    <div v-if="user" class="user-info">
      <h3>User Information</h3>
      <div class="info-card">
        <p><strong>Username:</strong> {{ user.username }}</p>
        <p><strong>Email:</strong> {{ user.email }}</p>
        <p><strong>Roles:</strong> {{ user.roles.join(', ') || 'No roles assigned' }}</p>
      </div>
      
      <div class="oidc-info">
        <h3>OIDC Claims</h3>
        <div class="attributes">
          <pre>{{ JSON.stringify(user.attributes, null, 2) }}</pre>
        </div>
      </div>
    </div>
    
    <div v-else class="welcome-message">
      <p>This is an OpenID Connect Relying Party (RP) demo application.</p>
      <p>Please login to access protected resources and view your user information.</p>
      <button @click="login" class="btn-primary">Login with OIDC</button>
    </div>
    
    <div class="explanation">
      <h3>How OIDC Authentication Works</h3>
      <ol>
        <li>User clicks login and is redirected to the OpenID Provider (Keycloak)</li>
        <li>User authenticates with Keycloak</li>
        <li>Keycloak redirects back with an authorization code</li>
        <li>RP exchanges the code for ID Token and Access Token</li>
        <li>ID Token contains user identity claims including roles</li>
        <li>RP validates tokens and creates a session</li>
        <li>User can now access protected resources based on their roles</li>
      </ol>
      
      <h3>OIDC vs SAML Key Differences</h3>
      <ul>
        <li><strong>Protocol:</strong> OIDC uses OAuth 2.0 + JWT, SAML uses XML</li>
        <li><strong>Token Format:</strong> OIDC uses JSON Web Tokens, SAML uses XML assertions</li>
        <li><strong>Flow:</strong> OIDC uses Authorization Code flow, SAML uses POST/Redirect bindings</li>
        <li><strong>Modern:</strong> OIDC is more recent and REST-friendly</li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
  props: ['user'],
  methods: {
    login() {
      window.location.href = '/oidc/login'
    }
  }
}
</script>