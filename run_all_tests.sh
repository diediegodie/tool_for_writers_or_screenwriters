
#!/bin/bash

# Universal test script for fullstack Writer & Screenwriter Tool
# Runs backend (pytest), frontend (vitest), lint, and format checks in sequence

set -e  # Exit immediately if a command exits with a non-zero status

echo "🧪 Starting full-stack test suite..."
echo ""

# Run Backend Tests
echo "🐍 Running BACKEND tests..."
cd backend || exit 1
if ! pytest; then
    echo "❌ Backend tests failed!"
    exit 1
fi
echo "✅ Backend tests passed!"
cd ..
echo ""

# Run Frontend Tests
echo "⚛️  Running FRONTEND tests..."
cd frontend || exit 1
if ! npx vitest run; then
    echo "❌ Frontend tests failed!"
    exit 1
fi
echo "✅ Frontend tests passed!"
echo ""

# Run ESLint
echo "🔎 Running ESLINT checks..."
if ! npm run lint; then
    echo "❌ ESLint checks failed!"
    exit 1
fi
echo "✅ ESLint checks passed!"
echo ""

# Run Prettier
echo "🎨 Running PRETTIER formatting checks..."
if ! npm run format; then
    echo "❌ Prettier formatting failed!"
    exit 1
fi
echo "✅ Prettier formatting passed!"
echo ""

cd ..
echo "🎉 ✅ All tests and checks completed successfully!"
