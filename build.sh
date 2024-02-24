#!/usr/bin/env bash
# exit on error
set -o errexit

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
mv yogo /usr/local/bin/yogo
chmod +x /usr/local/bin/yogo
cd $HOME/project/src # Make sure we return to where we were

/opt/render/project/src/.venv/bin/python3.11 -m pip install --upgrade pip
pip install setuptools wheel
pip install -r requirements.txt
go install github.com/antham/yogo/v4@latest
