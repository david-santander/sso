#!/bin/bash

echo "Waiting for Keycloak to start..."

until curl -f -s http://localhost:8080/health/ready > /dev/null; do
    echo "Keycloak is not ready yet..."
    sleep 5
done

echo "Keycloak is ready!"