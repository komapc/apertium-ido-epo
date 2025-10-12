#!/bin/bash
# Deploy frontend and functions to Firebase

set -e

PROJECT_ID="${FIREBASE_PROJECT_ID:-ido-epo-translator}"

echo "=== Deploying to Firebase ==="
echo "Project: $PROJECT_ID"
echo ""

# Navigate to project root
cd "$(dirname "$0")/.."

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
    echo ""
fi

if [ ! -d "functions/node_modules" ]; then
    echo "📦 Installing functions dependencies..."
    cd functions
    npm install
    cd ..
    echo ""
fi

# Build frontend
echo "🔨 Building frontend..."
npm run build
echo ""

# Build functions
echo "🔨 Building functions..."
cd functions
npm run build
cd ..
echo ""

# Deploy to Firebase
echo "🚀 Deploying to Firebase..."
firebase deploy --project "$PROJECT_ID"

echo ""
echo "✅ Deployment complete!"
echo ""

# Get hosting URL
HOSTING_URL="https://$PROJECT_ID.web.app"
echo "🌐 Website URL: $HOSTING_URL"
echo ""

