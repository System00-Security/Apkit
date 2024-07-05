#!/bin/bash

echo "Installing Python dependencies..."
pip3 install colorama frida frida-tools androguard==3.4.0a1

echo "Setting up directories..."
mkdir -p bin/jadx

echo "Downloading jadx..."
cd bin/jadx
wget -q --show-progress --progress=bar:force:noscroll https://github.com/skylot/jadx/releases/download/v1.5.0/jadx-1.5.0.zip -O jadx-1.5.0.zip
if [ $? -eq 0 ]; then
    echo "Downloaded jadx-1.5.0.zip successfully."
else
    echo "Failed to download jadx-1.5.0.zip."
    exit 1
fi

echo "Extracting jadx..."
unzip -q jadx-1.5.0.zip -d .
chmod +x bin/jadx
if [ $? -eq 0 ]; then
    echo "Extracted jadx-1.5.0.zip successfully."
    rm jadx-1.5.0.zip
else
    echo "Failed to extract jadx-1.5.0.zip."
    exit 1
fi

echo "Cleaning up..."
rm README.md LICENSE

echo "Dependencies installed successfully."
