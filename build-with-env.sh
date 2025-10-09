#!/bin/bash

# Build script with environment variable substitution
# This replaces placeholders in build files with actual environment variables

set -e

echo "🚀 Building Betting League Championship Frontend..."

# Check if FontAwesome kit ID is provided
if [ -z "$FONTAWESOME_KIT_ID" ]; then
    echo "⚠️  WARNING: FONTAWESOME_KIT_ID environment variable not set"
    echo "   FontAwesome icons may not load properly"
    FONTAWESOME_KIT_ID="fallback_kit_id"
fi

# Build the Angular application
cd frontend/betting-league-app
npm run build -- --configuration=production

# Replace placeholders in built files with environment variables
echo "🔧 Substituting environment variables..."

# Replace in index.html
if [ -f "dist/betting-league-app/index.html" ]; then
    sed -i.bak "s/{{FONTAWESOME_KIT_ID}}/$FONTAWESOME_KIT_ID/g" dist/betting-league-app/index.html
    rm dist/betting-league-app/index.html.bak
    echo "✅ FontAwesome kit ID substituted in index.html"
fi

# Replace in any environment files that might contain placeholders
find dist/betting-league-app -name "*.js" -type f -exec sed -i.bak "s/{{FONTAWESOME_KIT_ID}}/$FONTAWESOME_KIT_ID/g" {} \;
find dist/betting-league-app -name "*.js.bak" -type f -delete

echo "✅ Build complete with environment substitution"
echo "🎯 FontAwesome Kit ID: ${FONTAWESOME_KIT_ID:0:8}... (truncated for security)"