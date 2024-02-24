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
    echo "Error: client_secret.json not found in $SECRETS_DIR"
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

echo "Downloading yogo..."
mkdir -p $STORAGE_DIR/yogo
cd $STORAGE_DIR/yogo
wget https://github.com/antham/yogo/releases/download/v4.1.1/yogo_4.1.1_linux_amd64.tar.gz
tar -xzf yogo_4.1.1_linux_amd64.tar.gz

# Move yogo binary to a writable directory within the project structure
mkdir -p $HOME/project/bin
mv yogo $HOME/project/bin/yogo
chmod +x $HOME/project/bin/yogo

# Echo the full path of yogo
echo "yogo installed at: $HOME/project/bin/yogo"

# Add yogo directory to the PATH
export PATH="$HOME/project/bin:$PATH"

# Run the yogo command
# echo "Running yogo command"
# yogo inbox show wffpandaexpress1 1
# echo "Yogo command executed successfully"

# Return to the source directory
cd $HOME/project/src

/opt/render/project/src/.venv/bin/python3.11 -m pip install --upgrade pip
pip install setuptools wheel
pip install -r requirements.txt
