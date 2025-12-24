# Multi-stage build for React frontend
# Stage 1: Build the React application
FROM node:20-alpine AS builder

WORKDIR /app

# Accept build arguments for environment variables
ARG VITE_USE_MOCK_API=true
ARG VITE_API_BASE_URL=http://localhost:8000/api

# Set as environment variables for Vite (Vite requires these at build time)
ENV VITE_USE_MOCK_API=$VITE_USE_MOCK_API
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

# Copy package files
COPY package.json ./
COPY package-lock.json* ./

# Install dependencies
# Use npm ci if lock file exists, otherwise npm install
RUN if [ -f package-lock.json ]; then npm ci; else npm install; fi

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Stage 2: Serve with nginx
FROM nginx:alpine

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built assets from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]

