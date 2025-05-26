<template>
  <div class="home">
    <h2>Welcome to SAML SP Demo Application</h2>
    
    <!-- Authenticated user section - displays user details and SAML attributes -->
    <div v-if="user" class="user-info">
      <h3>User Information</h3>
      <div class="info-card">
        <p><strong>Username:</strong> {{ user.username }}</p>
        <p><strong>Email:</strong> {{ user.email }}</p>
        <p><strong>Roles:</strong> {{ user.roles.join(', ') || 'No roles assigned' }}</p>
      </div>
      
      <!-- SAML-specific information section -->
      <div class="saml-info">
        <h3>SAML Attributes</h3>
        <div class="attributes">
          <!-- Display raw SAML attributes received from IdP -->
          <pre>{{ JSON.stringify(user.attributes, null, 2) }}</pre>
        </div>
      </div>
    </div>
    
    <!-- Unauthenticated user section - shows login prompt -->
    <div v-else class="welcome-message">
      <p>This is a SAML Service Provider (SP) demo application.</p>
      <p>Please login to access protected resources and view your user information.</p>
      <button @click="login" class="btn-primary">Login with SAML</button>
    </div>
    
    <!-- Educational section explaining SAML flow -->
    <div class="explanation">
      <h3>How SAML Authentication Works</h3>
      <ol>
        <li>User clicks login and is redirected to the Identity Provider (Keycloak)</li>
        <li>User authenticates with Keycloak</li>
        <li>Keycloak generates a SAML assertion with user attributes and roles</li>
        <li>User is redirected back to this SP with the SAML response</li>
        <li>SP validates the SAML response and creates a session</li>
        <li>User can now access protected resources based on their roles</li>
      </ol>
    </div>
  </div>
</template>

<script>
/**
 * @component Home
 * @description Home page component that serves as the landing page for the SAML SP demo
 * 
 * Features:
 * - Displays welcome message for unauthenticated users
 * - Shows detailed user information for authenticated users
 * - Displays raw SAML attributes received from the IdP
 * - Provides educational content about SAML authentication flow
 */
export default {
  name: 'Home',
  props: {
    /**
     * User object passed from parent component
     * Contains username, email, roles, and SAML attributes
     */
    user: {
      type: Object,
      default: null
    }
  },
  methods: {
    /**
     * Initiates SAML login by redirecting to the backend login endpoint
     * The backend will generate a SAML request and redirect to Keycloak
     */
    login() {
      window.location.href = '/saml/login'
    }
  }
}
</script>