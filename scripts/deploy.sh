#!/bin/bash

# Deploy script for VPS
# This script is executed on the VPS server

set -e  # Exit on error

echo "🚀 Starting deployment process..."

# Configuration
PROJECT_DIR="${PROJECT_DIR:-~/Invisibilidown}"
COMPOSE_FILE="docker-compose.yml"

# Navigate to project directory
cd "$PROJECT_DIR" || {
    echo "❌ Error: Project directory not found at $PROJECT_DIR"
    exit 1
}

echo "📂 Current directory: $(pwd)"

# Pull latest changes
echo "📥 Pulling latest changes from Git..."
git pull origin main || {
    echo "❌ Error: Failed to pull from Git"
    exit 1
}

# Run database migrations
echo "🔄 Running database migrations..."
docker compose run --rm web python manage.py migrate || {
    echo "❌ Error: Migrations failed"
    exit 1
}

# Collect static files
echo "📦 Collecting static files..."
docker compose run --rm web python manage.py collectstatic --noinput || {
    echo "⚠️  Warning: Static files collection failed (non-critical)"
}

# Build and start containers
echo "🐳 Building and starting containers..."
docker compose up -d --build || {
    echo "❌ Error: Failed to start containers"
    exit 1
}

# Wait for containers to be healthy
echo "⏳ Waiting for containers to be ready..."
sleep 5

# Check container status
echo "📊 Container status:"
docker compose ps

# Clean up old images
echo "🧹 Cleaning up old Docker images..."
docker image prune -f

# Check if web service is running
if docker compose ps | grep -q "web.*Up"; then
    echo "✅ Deployment completed successfully!"
    echo "🌐 Application is running"
else
    echo "❌ Warning: Web container may not be running properly"
    docker compose logs --tail=50 web
    exit 1
fi

echo ""
echo "========================================="
echo "   Deployment Summary"
echo "========================================="
echo "✅ Git pull: Success"
echo "✅ Docker build: Success"
echo "✅ Migrations: Success"
echo "✅ Containers: Running"
echo "========================================="
