#!/usr/bin/env bash
# exit on error
set -o errexit

# Define paths
SECRETS_DIR="/etc/secrets"
RENDER_DIR="/opt/render/project/src"

# Check if the client_secret.json exists in the secrets directory
if [[ -f "$SECRETS_DIR/client_secret.json" ]]; then
    echo "client_secret.json found in $SECRETS_DIR"
    
    # Create the render directory if it doesn't exist
    
    
    # Copy client_secret.json to the render directory
    cp "$SECRETS_DIR/client_secret.json" "$RENDER_DIR/client_secret.json"
    
    echo "client_secret.json copied to $RENDER_DIR"
    echo "Contents of client_secret.json:"
    cat "$RENDER_DIR/client_secret.json"
    ls
else
    echo "Warning: client_secret.json not found in $SECRETS_DIR (skipping)"
fi

STORAGE_DIR=/opt/render/project/.render

if [[ ! -d $STORAGE_DIR/chrome ]]; then
  echo "...Downloading Chrome"
  mkdir -p $STORAGE_DIR/chrome
  cd $STORAGE_DIR/chrome
  wget -P ./ https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  dpkg -x ./google-chrome-stable_current_amd64.deb $STORAGE_DIR/chrome
  rm ./google-chrome-stable_current_amd64.deb
  cd $HOME/project/src # Make sure we return to where we were
else
  echo "...Using Chrome from cache"
fi

# Build React frontend (using Render's pre-installed Node.js)
echo "...Building React frontend"
cd wfffrontend
npm ci
npm run build
cd ..

# Install Python dependencies  
echo "...Installing Python dependencies"
/opt/render/project/src/.venv/bin/python3.11 -m pip install --upgrade pip
pip install setuptools wheel
pip install -r requirements.txt