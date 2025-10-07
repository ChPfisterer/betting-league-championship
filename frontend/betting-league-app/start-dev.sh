#!/bin/bash

# Ensure we're using the correct Node.js version
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"

# Use Node.js v22.20.0
nvm use 22.20.0

# Verify version
echo "Using Node.js version: $(node --version)"
echo "Using npm version: $(npm --version)"

# Start the Angular development server
npx @angular/cli@latest serve