#!/bin/bash
# SmishGuard PH - One-Line Deployment for Ubuntu 24.04 & 25.04
set -e
echo "🚀 Starting SmishGuard PH Installation..."
apt-get update -y
if ! command -v docker &> /dev/null; then
    echo "🐳 Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
fi
if [ ! -f .env ]; then
    cp .env.example .env
fi
echo "🏗️ Building and starting the platform..."
docker compose up -d --build
echo "🎉 SmishGuard PH is live!"
