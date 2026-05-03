#!/bin/bash
set -e

echo "Starting AI Forge Backend..."
docker-compose up --build -d
echo "Backend running on http://localhost:8000"
