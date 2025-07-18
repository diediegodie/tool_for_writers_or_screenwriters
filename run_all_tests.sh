#!/bin/bash

# Universal test script for fullstack Writer & Screenwriter Tool
# Runs both backend (pytest) and frontend (vitest) tests in sequence

set -e  # Exit immediately if a command exits with a non-zero status

echo "🧪 Starting full-stack test suite..."
echo ""

# Change to the project root directory
cd "$(dirname "$0")"

# Run Backend Tests
echo "🐍 Running BACKEND tests..."
if ! pytest; then
    echo "❌ Backend tests failed!"
    exit 1
fi
echo "✅ Backend tests passed!"
echo ""

# Run Frontend Tests
echo "⚛️  Running FRONTEND tests..."
cd frontend
if ! npx vitest run; then
    echo "❌ Frontend tests failed!"
    exit 1
fi
echo "✅ Frontend tests passed!"
echo ""

echo "🎉 ✅ All tests completed successfully!"
