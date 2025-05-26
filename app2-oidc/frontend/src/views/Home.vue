<!--
  Home View Component - Landing page for OIDC demo application
  
  This component:
  - Displays user information when authenticated
  - Shows OIDC claims received from the identity provider
  - Provides educational content about OIDC vs SAML
  - Offers login option for unauthenticated users
  
  Key features:
  - Demonstrates OIDC token claims display
  - Shows role-based access information
  - Educates users about OIDC authentication flow
-->
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
        <!-- Display raw OIDC claims from ID token -->
        <!-- These claims are extracted from the JWT ID token by the backend -->
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
/**
 * Home view component
 * 
 * Serves as the landing page and provides:
 * - User information display for authenticated users
 * - OIDC claims visualization
 * - Educational content about OIDC
 * - Login entry point for unauthenticated users
 * 
 * Note: User prop is passed from App.vue root component
 */
export default {
  name: 'Home',
  props: ['user'],
  methods: {
    /**
     * Redirect to OIDC login endpoint
     * Backend will handle the OIDC authorization code flow
     */
    login() {
      window.location.href = '/oidc/login'
    }
  }
}
</script>