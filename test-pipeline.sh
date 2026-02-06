#!/bin/bash

echo "==================================="
echo "Testing Data Pipeline"
echo "==================================="

echo ""
echo "Step 1: Starting Docker services..."
docker compose up -d

echo ""
echo "Waiting for services to be ready (60 seconds)..."
sleep 60

echo ""
echo "==================================="
echo "Step 2: Testing Flask Mock Server"
echo "==================================="

echo ""
echo "Testing Flask Health Check..."
curl -s http://localhost:5000/api/health | python3 -m json.tool

echo ""
echo ""
echo "Getting customers from Flask (page 1, limit 5)..."
curl -s "http://localhost:5000/api/customers?page=1&limit=5" | python3 -m json.tool

echo ""
echo ""
echo "Getting specific customer from Flask (CUST001)..."
curl -s http://localhost:5000/api/customers/CUST001 | python3 -m json.tool

echo ""
echo ""
echo "==================================="
echo "Step 3: Testing FastAPI Ingestion"
echo "==================================="

echo ""
echo "Triggering data ingestion..."
curl -s -X POST http://localhost:8000/api/ingest | python3 -m json.tool

echo ""
echo ""
echo "==================================="
echo "Step 4: Testing FastAPI Queries"
echo "==================================="

echo ""
echo "Getting customers from database (page 1, limit 5)..."
curl -s "http://localhost:8000/api/customers?page=1&limit=5" | python3 -m json.tool

echo ""
echo ""
echo "Getting specific customer from database (CUST001)..."
curl -s http://localhost:8000/api/customers/CUST001 | python3 -m json.tool

echo ""
echo ""
echo "==================================="
echo "Testing Complete!"
echo "==================================="
echo ""
echo "To view logs:"
echo "  docker compose logs mock-server"
echo "  docker compose logs pipeline-service"
echo "  docker compose logs postgres"
echo ""
echo "To stop services:"
echo "  docker compose down"
echo ""
echo "To stop and remove volumes:"
echo "  docker compose down -v"
