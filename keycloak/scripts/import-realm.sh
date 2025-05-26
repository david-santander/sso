#!/bin/bash

# Wait for Keycloak to be ready
./wait-for-keycloak.sh

echo "Importing SSO POC realm..."

# Get admin token
ACCESS_TOKEN=$(curl -s -X POST "http://localhost:8080/realms/master/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin" \
  -d "password=admin" \
  -d "grant_type=password" \
  -d "client_id=admin-cli" | jq -r '.access_token')

if [ -z "$ACCESS_TOKEN" ] || [ "$ACCESS_TOKEN" == "null" ]; then
    echo "Failed to get access token"
    exit 1
fi

# Import the realm
curl -s -X POST "http://localhost:8080/admin/realms" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d @../realms/sso-poc-realm.json

if [ $? -eq 0 ]; then
    echo "Realm imported successfully!"
else
    echo "Failed to import realm"
    exit 1
fi