#!/bin/bash
# HackGPT Installation Script for Kali Linux

echo "🔥 HackGPT Installation Script 🔥"
echo "=================================="

# Update system
echo "[+] Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python dependencies
echo "[+] Installing Python dependencies..."
pip3 install -r requirements.txt

# Install system tools that may not be present
echo "[+] Installing pentesting tools..."
sudo apt install -y \
    nmap \
    masscan \
    nikto \
    gobuster \
    sqlmap \
    hydra \
    theharvester \
    enum4linux \
    whatweb \
    wpscan \
    dnsenum \
    whois \
    exploitdb \
    metasploit-framework \
    netcat-traditional \
    curl \
    wget \
    git

# Install ollama for local AI
echo "[+] Installing ollama for local AI support..."
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a lightweight model
echo "[+] Downloading local AI model..."
ollama pull llama2:7b

# Create reports directory
echo "[+] Creating reports directory..."
sudo mkdir -p /reports
sudo chown -R $USER:$USER /reports

# Make script executable
chmod +x hackgpt.py

# Create symlink for global access
echo "[+] Creating global command..."
sudo ln -sf $(pwd)/hackgpt.py /usr/local/bin/hackgpt

echo ""
echo "✅ Installation Complete!"
echo ""
echo "Usage:"
echo "  ./hackgpt.py                    # Interactive mode"
echo "  ./hackgpt.py --web             # Web dashboard"
echo "  ./hackgpt.py --voice           # Voice command mode"
echo "  hackgpt                        # Global command (if symlink created)"
echo ""
echo "Set OpenAI API key (optional):"
echo "  export OPENAI_API_KEY='your-api-key-here'"
echo ""
