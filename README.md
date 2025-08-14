# 🔥 HackGPT - AI-Powered Penetration Testing Automation Tool

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/Platform-Kali%20Linux-orange.svg" alt="Kali Linux">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/AI-GPT%20%7C%20Local%20LLM-purple.svg" alt="AI Powered">
</p>

HackGPT is a production-ready AI-powered penetration testing automation tool designed specifically for Kali Linux. It follows the standard 6-phase penetration testing methodology while leveraging AI for intelligent decision-making, tool selection, and report generation.

## ✨ Features

### 🤖 AI-Powered Intelligence
- **Dual AI Mode**: OpenAI API (online) or Local LLM with Ollama (offline)
- **Smart Tool Selection**: AI recommends optimal tools and commands
- **Intelligent Analysis**: Automated vulnerability assessment and risk scoring
- **Context-Aware Decisions**: AI learns from previous phases to guide next steps

### 🛡️ Complete Penetration Testing Framework
- **Phase 1**: Planning & Reconnaissance (Passive/Active OSINT)
- **Phase 2**: Scanning & Enumeration (Network/Web/Service Discovery)
- **Phase 3**: Exploitation (Safe, Confirmed Exploitation)
- **Phase 4**: Post-Exploitation (Privilege Escalation, Lateral Movement)
- **Phase 5**: Reporting (Technical & Executive Reports)
- **Phase 6**: Retesting (Validation After Remediation)

### 🔧 Automated Tool Management
- **Auto-Installation**: Missing tools are installed automatically
- **Tool Integration**: 20+ integrated pentesting tools
- **Custom Scripts**: Downloads and configures specialized tools from GitHub

### 🎯 Multiple Interfaces
- **CLI Mode**: Terminal-based dark hacker interface
- **Web Dashboard**: Flask-based web interface
- **Voice Commands**: Speech recognition and text-to-speech
- **Batch Mode**: Command-line arguments for automation

### 📊 Advanced Reporting
- **AI-Generated Reports**: Technical and executive summaries
- **Multiple Formats**: Markdown, JSON, PDF export
- **CVSS Scoring**: Automated vulnerability scoring
- **Timestamped Results**: All results saved with timestamps

## 🚀 Quick Start

### Prerequisites
- Kali Linux (Desktop, VM, or Termux + NetHunter)
- Python 3.8+
- Internet connection (for tool updates and online AI mode)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/HackGPT.git
cd HackGPT

# Run the installation script
chmod +x install.sh
./install.sh

# Optional: Set OpenAI API key for online AI mode
export OPENAI_API_KEY='your-api-key-here'
```

### Basic Usage

```bash
# Interactive mode (recommended for beginners)
./hackgpt.py

# Full automated pentest
./hackgpt.py --target example.com --scope "Web application" --auth-key "AUTH123"

# Web dashboard
./hackgpt.py --web

# Voice command mode
./hackgpt.py --voice
```

## 🔧 Configuration

### AI Configuration
HackGPT supports two AI modes:

1. **Online Mode (OpenAI API)**:
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

2. **Offline Mode (Local LLM)**:
   - Automatically installs Ollama
   - Downloads Llama2 7B model
   - Works without internet connection

### Tool Configuration
HackGPT automatically manages the following tools:

**Network Tools**: nmap, masscan, netcat
**Web Tools**: nikto, gobuster, whatweb, wpscan
**Exploitation**: metasploit, sqlmap, hydra, searchsploit
**Reconnaissance**: theharvester, enum4linux, dnsenum
**Post-Exploitation**: linpeas, winpeas (auto-downloaded)

## 🎯 Usage Examples

### Full Penetration Test
```bash
./hackgpt.py
# Follow interactive prompts:
# 1. Enter target: example.com
# 2. Enter scope: Web application and infrastructure
# 3. Enter authorization key: PENTEST-2024-AUTH
# 4. Select "Full Pentest (All 6 Phases)"
```

### Specific Phase Testing
```bash
./hackgpt.py
# Select "Run Specific Phase"
# Choose phase 1-6 based on your needs
```

### Web Dashboard
```bash
./hackgpt.py --web
# Open browser to http://localhost:5000
```

### Voice Commands
```bash
./hackgpt.py --voice
# Say: "Start full pentest"
# Say: "View reports" 
# Say: "Exit"
```

## 📋 Penetration Testing Phases

### Phase 1: Planning & Reconnaissance
**Tools Used**: theHarvester, whois, dnsenum, nmap, masscan
- Passive OSINT collection
- Domain and subdomain enumeration
- Service discovery and version detection
- **AI Analysis**: Attack surface identification, priority targeting

### Phase 2: Scanning & Enumeration
**Tools Used**: nmap (vuln scripts), nikto, gobuster, whatweb, enum4linux
- Vulnerability scanning
- Web application enumeration
- SMB/NetBIOS enumeration
- **AI Analysis**: CVE correlation, exploit recommendations

### Phase 3: Exploitation
**Tools Used**: searchsploit, sqlmap, hydra, metasploit
- Safe exploitation attempts
- SQL injection testing
- Brute force attacks (rate-limited)
- **AI Analysis**: Risk-based exploit selection, impact assessment

### Phase 4: Post-Exploitation
**Tools Used**: linpeas, winpeas, netcat
- Privilege escalation enumeration
- Credential harvesting
- Lateral movement assessment
- **AI Analysis**: Business impact analysis, persistence strategies

### Phase 5: Reporting
- AI-generated executive summary
- Technical vulnerability details
- CVSS scoring and remediation
- **Output Formats**: Markdown, JSON, PDF

### Phase 6: Retesting
- Focused re-testing of remediated vulnerabilities
- Validation of security fixes
- **AI Analysis**: Remediation verification, residual risk assessment

## 🛡️ Security Features

### Authorization Controls
- Mandatory authorization key before active testing
- Confirmation prompts for high-impact operations
- No automatic exploitation without user approval

### Data Protection
- Authorization keys stored in memory only
- No sensitive data in logs
- Results saved locally with proper permissions

### Rate Limiting
- Built-in delays for brute force attacks
- Respectful scanning speeds
- Timeout controls for all operations

## 📊 Report Examples

### Executive Summary
```
High-Risk Vulnerabilities Found: 3
Medium-Risk Vulnerabilities Found: 7
Recommended Priority Actions:
1. Patch SQL injection in login form
2. Update outdated web server
3. Implement input validation
```

### Technical Report
```
CVE-2023-1234: SQL Injection
CVSS Score: 9.1 (Critical)
Location: /login.php parameter 'username'
Proof: ' UNION SELECT user,pass FROM admin--
Recommendation: Use parameterized queries
```

## 🚧 Development

### Project Structure
```
HackGPT/
├── hackgpt.py          # Main application
├── install.sh          # Installation script
├── requirements.txt    # Python dependencies
├── templates/          # Web dashboard templates
├── reports/           # Generated reports
└── README.md          # This file
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Test on Kali Linux
4. Submit a pull request

### Testing
```bash
# Test CLI mode
./hackgpt.py --target testphp.vulnweb.com --scope "Test site" --auth-key "TEST"

# Test web dashboard
./hackgpt.py --web

# Test voice commands
./hackgpt.py --voice
```

## 📚 Advanced Usage

### Custom Tool Integration
Add new tools to the `TOOL_COMMANDS` dictionary:
```python
TOOL_COMMANDS = {
    'your-tool': 'sudo apt install -y your-tool',
    # ... existing tools
}
```

### Custom AI Prompts
Modify AI prompts in the `_create_prompt` method for specialized analysis.

### Web Dashboard Customization
Modify `templates/dashboard.html` for custom web interface.

## ⚠️ Legal Disclaimer

**IMPORTANT**: HackGPT is designed for authorized penetration testing only. 

- Only use against systems you own or have explicit written permission to test
- Obtain proper authorization before conducting any security tests
- Follow responsible disclosure practices
- Comply with all applicable laws and regulations

The developers are not responsible for any misuse of this tool.

## 🐛 Troubleshooting

### Common Issues

**Issue**: "Tool not found"
**Solution**: Run `./install.sh` again or manually install missing tools

**Issue**: "AI not responding"
**Solution**: Check internet connection or verify API key

**Issue**: "Permission denied"
**Solution**: Run with proper sudo privileges or check file permissions

**Issue**: "Ollama model not found"
**Solution**: Run `ollama pull llama2:7b` manually

### Debug Mode
Enable verbose output:
```bash
export PYTHONPATH=$PWD
python3 -m pdb hackgpt.py
```

## 🔄 Version History

- **v1.0.0**: Initial release with full 6-phase pentesting
- **v1.1.0**: Added web dashboard and voice commands
- **v1.2.0**: Enhanced AI analysis and reporting

## 📞 Support

- **Issues**: Open a GitHub issue
- **Discussions**: GitHub Discussions
- **Security**: Email security@hackgpt.dev

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for GPT API
- Ollama team for local LLM support
- Kali Linux team for the platform
- Security community for tools and techniques

---

<p align="center">
  <strong>Made with ❤️ for the ethical hacking community</strong>
</p>