<template>
  <div class="home">
    <h2>Welcome to SAML SP Demo Application</h2>
    
    <div v-if="user" class="user-info">
      <h3>User Information</h3>
      <div class="info-card">
        <p><strong>Username:</strong> {{ user.username }}</p>
        <p><strong>Email:</strong> {{ user.email }}</p>
        <p><strong>Roles:</strong> {{ user.roles.join(', ') || 'No roles assigned' }}</p>
      </div>
      
      <div class="saml-info">
        <h3>SAML Attributes</h3>
        <div class="attributes">
          <pre>{{ JSON.stringify(user.attributes, null, 2) }}</pre>
        </div>
      </div>
    </div>
    
    <div v-else class="welcome-message">
      <p>This is a SAML Service Provider (SP) demo application.</p>
      <p>Please login to access protected resources and view your user information.</p>
      <button @click="login" class="btn-primary">Login with SAML</button>
    </div>
    
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
export default {
  name: 'Home',
  props: ['user'],
  methods: {
    login() {
      window.location.href = '/saml/login'
    }
  }
}
</script>