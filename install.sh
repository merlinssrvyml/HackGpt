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

#!/bin/bash

# HackGPT Enterprise Installation Script
# Installs all dependencies for enterprise penetration testing platform
# Version: 2.0.0 (Production-Ready)

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1"
}

info() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] INFO:${NC} $1"
}

# Banner
echo -e "${PURPLE}"
echo "██╗  ██╗ █████╗  ██████╗██╗  ██╗ ██████╗ ██████╗ ████████╗"
echo "██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝ ██╔══██╗╚══██╔══╝"
echo "███████║███████║██║     █████╔╝ ██║  ███╗██████╔╝   ██║   "
echo "██╔══██║██╔══██║██║     ██╔═██╗ ██║   ██║██╔═══╝    ██║   "
echo "██║  ██║██║  ██║╚██████╗██║  ██╗╚██████╔╝██║        ██║   "
echo "╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝        ╚═╝   "
echo -e "${NC}"
echo -e "${CYAN}Enterprise AI-Powered Penetration Testing Platform v2.0${NC}"
echo -e "${GREEN}Production-Ready | Cloud-Native | AI-Enhanced${NC}"
echo

# Check if running as root
if [[ $EUID -eq 0 ]]; then
    warn "Running as root. Some installations may behave differently."
fi

# Detect OS
OS="Unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if [ -f /etc/debian_version ]; then
        OS="Debian/Ubuntu"
    elif [ -f /etc/redhat-release ]; then
        OS="RedHat/CentOS"
    elif [ -f /etc/arch-release ]; then
        OS="Arch"
    else
        OS="Linux"
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]]; then
    OS="Windows"
fi

log "Detected OS: $OS"

# Check Python version
check_python() {
    log "Checking Python installation..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        log "Found Python $PYTHON_VERSION"
        
        # Check if version is 3.8 or higher
        if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
            log "Python version is compatible"
            PYTHON_CMD="python3"
        else
            error "Python 3.8 or higher is required. Found: $PYTHON_VERSION"
            exit 1
        fi
    else
        error "Python 3 is not installed"
        exit 1
    fi
}

# Install system dependencies
install_system_deps() {
    log "Installing system dependencies..."
    
    case $OS in
        "Debian/Ubuntu")
            sudo apt update
            sudo apt install -y 
                python3-dev python3-pip python3-venv 
                build-essential libssl-dev libffi-dev 
                libjpeg-dev zlib1g-dev 
                libpq-dev 
                redis-server 
                postgresql postgresql-contrib 
                docker.io docker-compose 
                nmap masscan 
                git curl wget 
                portaudio19-dev 
                libldap2-dev libsasl2-dev 
                pandoc texlive-latex-recommended 
                gobuster dirbuster dirb 
                nikto sqlmap 
                hydra medusa 
                metasploit-framework 
                wireshark tshark 
                aircrack-ng 
                john hashcat 
                binwalk foremost 
                steghide stegsolve 
                exiftool 
                burpsuite zaproxy
            ;;
        "RedHat/CentOS")
            sudo yum update -y
            sudo yum groupinstall -y "Development Tools"
            sudo yum install -y 
                python3-devel python3-pip 
                openssl-devel libffi-devel 
                postgresql-devel 
                redis 
                postgresql postgresql-server 
                docker docker-compose 
                nmap masscan 
                git curl wget
            ;;
        "Arch")
            sudo pacman -Sy
            sudo pacman -S --noconfirm 
                python python-pip 
                base-devel openssl libffi 
                postgresql-libs 
                redis 
                postgresql 
                docker docker-compose 
                nmap masscan 
                git curl wget
            ;;
        "macOS")
            if ! command -v brew &> /dev/null; then
                log "Installing Homebrew..."
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            fi
            
            brew update
            brew install 
                python@3.11 
                postgresql 
                redis 
                docker docker-compose 
                nmap masscan 
                git curl wget 
                portaudio 
                openldap 
                pandoc
            ;;
    esac
}

# Setup PostgreSQL
setup_postgresql() {
    log "Setting up PostgreSQL database..."
    
    case $OS in
        "Debian/Ubuntu"|"Linux")
            sudo systemctl start postgresql
            sudo systemctl enable postgresql
            
            # Create database and user
            sudo -u postgres psql -c "CREATE DATABASE hackgpt;" 2>/dev/null || warn "Database hackgpt already exists"
            sudo -u postgres psql -c "CREATE USER hackgpt WITH PASSWORD 'hackgpt123';" 2>/dev/null || warn "User hackgpt already exists"
            sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE hackgpt TO hackgpt;" 2>/dev/null
            ;;
        "macOS")
            brew services start postgresql
            
            createdb hackgpt 2>/dev/null || warn "Database hackgpt already exists"
            psql -d postgres -c "CREATE USER hackgpt WITH PASSWORD 'hackgpt123';" 2>/dev/null || warn "User hackgpt already exists"
            psql -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE hackgpt TO hackgpt;" 2>/dev/null
            ;;
    esac
    
    log "PostgreSQL setup completed"
}

# Setup Redis
setup_redis() {
    log "Setting up Redis cache server..."
    
    case $OS in
        "Debian/Ubuntu"|"Linux")
            sudo systemctl start redis-server
            sudo systemctl enable redis-server
            ;;
        "macOS")
            brew services start redis
            ;;
    esac
    
    log "Redis setup completed"
}

# Setup Docker
setup_docker() {
    log "Setting up Docker..."
    
    case $OS in
        "Debian/Ubuntu"|"Linux")
            sudo systemctl start docker
            sudo systemctl enable docker
            sudo usermod -aG docker $USER
            ;;
        "macOS")
            log "Please start Docker Desktop manually"
            ;;
    esac
    
    log "Docker setup completed"
}

# Create Python virtual environment
create_venv() {
    log "Creating Python virtual environment..."
    
    if [ ! -d "venv" ]; then
        $PYTHON_CMD -m venv venv
        log "Virtual environment created"
    else
        log "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    log "Virtual environment activated and pip upgraded"
}

# Install Python dependencies
install_python_deps() {
    log "Installing Python dependencies..."
    
    # Make sure we're in virtual environment
    if [[ "$VIRTUAL_ENV" == "" ]]; then
        source venv/bin/activate
    fi
    
    # Install requirements
    pip install -r requirements.txt
    
    # Install additional security tools via pip
    pip install 
        bandit 
        safety 
        semgrep 
        truffleHog 
        gitpython
    
    log "Python dependencies installed"
}

# Install additional penetration testing tools
install_pentest_tools() {
    log "Installing additional penetration testing tools..."
    
    # Create tools directory
    mkdir -p tools
    cd tools
    
    # Install Go tools (if Go is available)
    if command -v go &> /dev/null; then
        log "Installing Go-based tools..."
        go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
        go install github.com/projectdiscovery/httpx/cmd/httpx@latest
        go install github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest
        go install github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
        go install github.com/OWASP/Amass/v3/...@master
    else
        warn "Go not installed, skipping Go-based tools"
    fi
    
    # Install additional Python tools
    if [[ "$VIRTUAL_ENV" != "" ]]; then
        pip install 
            impacket 
            bloodhound 
            crackmapexec 
            responder 
            mitm6 
            ldapdomaindump
    fi
    
    cd ..
    log "Additional penetration testing tools installed"
}

# Setup Kubernetes tools
setup_kubernetes() {
    log "Setting up Kubernetes tools..."
    
    # Install kubectl
    case $OS in
        "Debian/Ubuntu"|"Linux")
            curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
            chmod +x kubectl
            sudo mv kubectl /usr/local/bin/
            ;;
        "macOS")
            brew install kubectl
            ;;
    esac
    
    # Install Helm
    case $OS in
        "Debian/Ubuntu"|"Linux")
            curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
            echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
            sudo apt-get update
            sudo apt-get install helm
            ;;
        "macOS")
            brew install helm
            ;;
    esac
    
    log "Kubernetes tools installed"
}

# Create configuration files
create_config_files() {
    log "Creating configuration files..."
    
    # Create config.ini if it doesn't exist
    if [ ! -f "config.ini" ]; then
        cat > config.ini << 'EOF'
[app]
debug = false
log_level = INFO

[database]
url = postgresql://hackgpt:hackgpt123@localhost:5432/hackgpt

[cache]
redis_url = redis://localhost:6379/0

[ai]
openai_api_key = 
local_model = llama2:7b

[security]
secret_key = 
jwt_algorithm = HS256
jwt_expiry = 3600

[ldap]
server = 
bind_dn = 
bind_password = 

[performance]
max_workers = 10
cache_ttl = 3600

[features]
enable_voice = true
enable_web_dashboard = true
enable_realtime_dashboard = true

[cloud]
docker_host = unix:///var/run/docker.sock
kubernetes_config = 
service_registry_backend = memory

[compliance]
frameworks = OWASP,NIST,ISO27001,SOC2
auto_compliance_check = true
generate_compliance_reports = true

[reporting]
output_formats = html,pdf,json,xml
template_directory = templates/
report_directory = reports/

[exploitation]
enable_auto_exploit = false
max_exploit_threads = 5
safe_mode = true

[monitoring]
prometheus_enabled = false
grafana_enabled = false
elasticsearch_enabled = false

[backup]
auto_backup = true
backup_interval = 24
backup_retention = 30
EOF
        log "Configuration file created"
    else
        log "Configuration file already exists"
    fi
    
    # Create .env.example
    if [ ! -f ".env.example" ]; then
        cat > .env.example << 'EOF'
# HackGPT Enterprise Environment Variables

# Database Configuration
DATABASE_URL=postgresql://hackgpt:hackgpt123@localhost:5432/hackgpt
REDIS_URL=redis://localhost:6379/0

# AI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4
LOCAL_LLM_ENDPOINT=http://localhost:11434

# Security
SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here
ENCRYPTION_KEY=your_encryption_key_here

# LDAP Configuration
LDAP_SERVER=ldaps://your-ldap-server.com:636
LDAP_BIND_DN=cn=admin,dc=example,dc=com
LDAP_BIND_PASSWORD=your_ldap_password

# Cloud Services
DOCKER_HOST=unix:///var/run/docker.sock
KUBECONFIG=/path/to/kubeconfig
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AZURE_SUBSCRIPTION_ID=your_azure_subscription_id
GCP_PROJECT_ID=your_gcp_project_id

# Monitoring
PROMETHEUS_ENDPOINT=http://localhost:9090
GRAFANA_ENDPOINT=http://localhost:3000
ELASTICSEARCH_ENDPOINT=http://localhost:9200

# Third-party APIs
SHODAN_API_KEY=your_shodan_api_key
CENSYS_API_ID=your_censys_api_id
CENSYS_API_SECRET=your_censys_api_secret
VIRUSTOTAL_API_KEY=your_virustotal_api_key

# Notification Settings
SLACK_WEBHOOK_URL=your_slack_webhook_url
DISCORD_WEBHOOK_URL=your_discord_webhook_url
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_email_password

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
LOG_ROTATION=daily
EOF
        log "Environment template created"
    else
        log "Environment template already exists"
    fi
    
    # Create directories
    mkdir -p logs reports templates database/migrations
    mkdir -p ai_engine/models security/certificates
    mkdir -p exploitation/payloads reporting/templates
    mkdir -p cloud/deployments performance/cache
    
    log "Directory structure created"
}

# Setup database schema
setup_database_schema() {
    log "Setting up database schema..."
    
    if [[ "$VIRTUAL_ENV" != "" ]]; then
        # Create database tables
        python3 -c "
from database import create_tables
try:
    create_tables()
    print('Database schema created successfully')
except Exception as e:
    print(f'Database schema creation failed: {e}')
" 2>/dev/null || warn "Database schema setup failed - will be created on first run"
    fi
}

# Download additional resources
download_resources() {
    log "Downloading additional resources..."
    
    # Download wordlists
    mkdir -p wordlists
    cd wordlists
    
    if [ ! -f "rockyou.txt" ]; then
        warn "Downloading wordlists (this may take a while)..."
        # Download common wordlists
        wget -q https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt -O top-passwords.txt || warn "Failed to download password list"
        wget -q https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/common.txt -O common-dirs.txt || warn "Failed to download directory list"
    fi
    
    cd ..
    
    # Download AI models if needed
    if command -v ollama &> /dev/null; then
        log "Ollama detected, pulling AI models..."
        ollama pull llama2:7b 2>/dev/null || warn "Failed to pull AI model"
    fi
    
    log "Resource download completed"
}

# Final setup and testing
final_setup() {
    log "Performing final setup and testing..."
    
    # Make scripts executable
    chmod +x hackgpt.py hackgpt_v2.py install.sh usage_examples.sh
    
    # Test installation
    if [[ "$VIRTUAL_ENV" != "" ]]; then
        python3 test_installation.py || warn "Installation test failed"
    fi
    
    log "Final setup completed"
}

# Main installation process
main() {
    log "Starting HackGPT Enterprise installation..."
    
    # Check requirements
    check_python
    
    # Install system dependencies
    install_system_deps
    
    # Setup services
    setup_postgresql
    setup_redis
    setup_docker
    
    # Setup Python environment
    create_venv
    install_python_deps
    
    # Install additional tools
    install_pentest_tools
    setup_kubernetes
    
    # Create configuration
    create_config_files
    setup_database_schema
    
    # Download resources
    download_resources
    
    # Final setup
    final_setup
    
    log "Installation completed successfully!"
    echo
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                    INSTALLATION COMPLETE                     ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo
    echo -e "${CYAN}Next steps:${NC}"
    echo -e "  1. Copy ${YELLOW}.env.example${NC} to ${YELLOW}.env${NC} and configure your API keys"
    echo -e "  2. Edit ${YELLOW}config.ini${NC} to customize settings"
    echo -e "  3. Activate the virtual environment: ${YELLOW}source venv/bin/activate${NC}"
    echo -e "  4. Run HackGPT: ${YELLOW}python3 hackgpt_v2.py${NC}"
    echo -e "  5. Or use the original version: ${YELLOW}python3 hackgpt.py${NC}"
    echo
    echo -e "${BLUE}API Server:${NC} ${YELLOW}python3 hackgpt_v2.py --api${NC}"
    echo -e "${BLUE}Web Dashboard:${NC} ${YELLOW}python3 hackgpt_v2.py --web${NC}"
    echo -e "${BLUE}Direct Assessment:${NC} ${YELLOW}python3 hackgpt_v2.py --target <target> --scope <scope> --auth-key <key>${NC}"
    echo
    echo -e "${PURPLE}For enterprise features, ensure all services are running:${NC}"
    echo -e "  • PostgreSQL: ${YELLOW}sudo systemctl status postgresql${NC}"
    echo -e "  • Redis: ${YELLOW}sudo systemctl status redis${NC}"
    echo -e "  • Docker: ${YELLOW}sudo systemctl status docker${NC}"
    echo
    echo -e "${GREEN}Happy Hacking! 🚀${NC}"
}

# Run main installation
main "$@"

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
