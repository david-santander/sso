FROM quay.io/keycloak/keycloak:latest

# Copy realm configuration
COPY realms/sso-poc-realm.json /opt/keycloak/data/import/

# Set environment variable to import realm on startup
ENV KC_IMPORT=/opt/keycloak/data/import/sso-poc-realm.json

# The base image already has the necessary entrypoint