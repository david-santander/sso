# Custom Keycloak Image for SSO POC
# Extends official Keycloak image with pre-configured realm
# This simplifies deployment by including all IdP configuration

FROM quay.io/keycloak/keycloak:latest

# Copy pre-configured realm with:
# - SAML and OIDC clients configured
# - Test users with different roles (admin, editor, viewer)
# - Role mappings and client scopes
COPY realms/sso-poc-realm.json /opt/keycloak/data/import/

# Configure Keycloak to import the realm on first startup
# This creates all necessary configuration automatically
ENV KC_IMPORT=/opt/keycloak/data/import/sso-poc-realm.json

# The base image already provides the necessary entrypoint
# It will start Keycloak with the imported realm configuration