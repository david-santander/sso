# Multi-stage Dockerfile for OIDC Frontend Application
# Stage 1: Build the Vue.js application
# Stage 2: Serve static files with nginx

# Build stage - compile Vue.js application
FROM node:18-alpine as builder

# Set working directory for build
WORKDIR /app

# Copy package files first for better layer caching
# This allows Docker to cache dependencies if package.json hasn't changed
COPY package*.json ./
RUN npm install

# Copy application source code
COPY . .

# Build the Vue.js application for production
# Creates optimized static files in the dist directory
RUN npm run build

# Production stage - lightweight nginx server
# Uses Alpine Linux for minimal image size
FROM nginx:alpine

# Copy built static files from builder stage
# These are the compiled Vue.js assets (HTML, CSS, JS)
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom nginx configuration
# Includes SPA routing support and API proxy settings
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose HTTP port
EXPOSE 80

# Start nginx in foreground mode
# "daemon off" keeps nginx in the foreground for Docker
CMD ["nginx", "-g", "daemon off;"]