#!/bin/bash

echo "🛑 remove service"
docker compose down -v

echo "🔨 build service"
docker compose build

echo "✅ run service"
docker compose up -d
