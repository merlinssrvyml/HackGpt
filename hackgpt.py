#!/usr/bin/env python3
"""
HackGPT - AI-Powered Penetration Testing Automation Tool
Author: HackGPT Team
Version: 1.0.0
Description: Production-ready pentesting automation tool for Kali Linux
"""

import os
import sys
import json
import time
import subprocess
import argparse
import logging
from datetime import datetime
from pathlib import Path
import threading
import queue
import hashlib

# Required imports
try:
    import requests
    import openai
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.prompt import Prompt, Confirm
    from rich.markdown import Markdown
    import speech_recognition as sr
    import pyttsx3
    import pypandoc
    import cvsslib
    from flask import Flask, render_template, request, jsonify
    import threading
except ImportError as e:
    print(f"Missing required package: {e}")
    print("Installing required packages...")
    subprocess.run([sys.executable, "-m", "pip", "install", 
                   "requests", "openai", "rich", "speechrecognition", 
                   "pyttsx3", "pypandoc", "cvss", "flask"], check=True)
    # Retry imports
    import requests
    import openai
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.prompt import Prompt, Confirm
    from rich.markdown import Markdown
    import speech_recognition as sr
    import pyttsx3
    import pypandoc
    import cvsslib
    from flask import Flask, render_template, request, jsonify

# Initialize Rich Console
console = Console()

# ASCII Banner
BANNER = """
[bold red]
    ██╗  ██╗ █████╗  ██████╗██╗  ██╗ ██████╗ ██████╗ ████████╗
    ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝ ██╔══██╗╚══██╔══╝
    ███████║███████║██║     █████╔╝ ██║  ███╗██████╔╝   ██║   
    ██╔══██║██╔══██║██║     ██╔═██╗ ██║   ██║██╔═══╝    ██║   
    ██║  ██║██║  ██║╚██████╗██║  ██╗╚██████╔╝██║        ██║   
    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝        ╚═╝   
[/bold red]
[bold cyan]           AI-Powered Penetration Testing Automation Tool[/bold cyan]
[dim]                      Running on Kali Linux[/dim]
"""

class AIEngine:
    """AI Engine for decision making and analysis"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.local_mode = not bool(self.api_key)
        self.console = Console()
        
        if self.local_mode:
            self.console.print("[yellow]No OpenAI API key found. Running in local mode.[/yellow]")
            self.setup_local_llm()
        else:
            openai.api_key = self.api_key
            
    def setup_local_llm(self):
        """Setup local LLM using ollama"""
        try:
            result = subprocess.run(['which', 'ollama'], capture_output=True, text=True)
            if result.returncode != 0:
                self.console.print("[yellow]Installing ollama for local AI...[/yellow]")
                subprocess.run(['curl', '-fsSL', 'https://ollama.ai/install.sh', '|', 'sh'], shell=True)
            
            # Pull a lightweight model
            subprocess.run(['ollama', 'pull', 'llama2:7b'], check=True)
            self.console.print("[green]Local LLM setup complete[/green]")
        except Exception as e:
            self.console.print(f"[red]Error setting up local LLM: {e}[/red]")
    
    def analyze(self, context, data, phase="general"):
        """Analyze data using AI"""
        prompt = self._create_prompt(context, data, phase)
        
        if self.local_mode:
            return self._query_local_llm(prompt)
        else:
            return self._query_openai(prompt)
    
    def _create_prompt(self, context, data, phase):
        """Create appropriate prompt based on phase"""
        base_prompt = f"""
        You are HackGPT, an expert penetration testing AI assistant. 
        
        Context: {context}
        Phase: {phase}
        Data to analyze: {data}
        
        Please provide:
        1. Summary of findings
        2. Risk assessment
        3. Recommended next actions
        4. Specific commands or techniques to try
        
        Keep responses concise and actionable.
        """
        return base_prompt
    
    def _query_openai(self, prompt):
        """Query OpenAI API"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"AI Error: {str(e)}"
    
    def _query_local_llm(self, prompt):
        """Query local LLM using ollama"""
        try:
            result = subprocess.run(
                ['ollama', 'run', 'llama2:7b', prompt],
                capture_output=True, text=True, timeout=60
            )
            return result.stdout if result.returncode == 0 else f"Local AI Error: {result.stderr}"
        except Exception as e:
            return f"Local AI Error: {str(e)}"

class ToolManager:
    """Manages pentesting tools installation and execution"""
    
    TOOL_COMMANDS = {
        'nmap': 'sudo apt install -y nmap',
        'masscan': 'sudo apt install -y masscan',
        'nikto': 'sudo apt install -y nikto',
        'gobuster': 'sudo apt install -y gobuster',
        'sqlmap': 'sudo apt install -y sqlmap',
        'hydra': 'sudo apt install -y hydra',
        'theharvester': 'sudo apt install -y theharvester',
        'enum4linux': 'sudo apt install -y enum4linux',
        'whatweb': 'sudo apt install -y whatweb',
        'wpscan': 'sudo apt install -y wpscan',
        'dnsenum': 'sudo apt install -y dnsenum',
        'whois': 'sudo apt install -y whois',
        'searchsploit': 'sudo apt install -y exploitdb',
        'metasploit-framework': 'sudo apt install -y metasploit-framework',
        'netcat': 'sudo apt install -y netcat-traditional',
        'curl': 'sudo apt install -y curl',
        'wget': 'sudo apt install -y wget',
    }
    
    GITHUB_TOOLS = {
        'linpeas': {
            'url': 'https://github.com/carlospolop/PEASS-ng.git',
            'path': '/opt/PEASS-ng',
            'executable': '/opt/PEASS-ng/linPEAS/linpeas.sh'
        },
        'winpeas': {
            'url': 'https://github.com/carlospolop/PEASS-ng.git',
            'path': '/opt/PEASS-ng',
            'executable': '/opt/PEASS-ng/winPEAS/winPEAS.exe'
        }
    }
    
    def __init__(self):
        self.console = Console()
        self.installed_tools = set()
        
    def check_tool(self, tool_name):
        """Check if tool is installed"""
        result = subprocess.run(['which', tool_name], capture_output=True, text=True)
        return result.returncode == 0
    
    def install_tool(self, tool_name):
        """Install a specific tool"""
        if tool_name in self.installed_tools:
            return True
            
        self.console.print(f"[yellow]Installing {tool_name}...[/yellow]")
        
        try:
            if tool_name in self.TOOL_COMMANDS:
                cmd = self.TOOL_COMMANDS[tool_name]
                result = subprocess.run(cmd.split(), check=True, capture_output=True, text=True)
                self.installed_tools.add(tool_name)
                self.console.print(f"[green]✓ {tool_name} installed successfully[/green]")
                return True
                
            elif tool_name in self.GITHUB_TOOLS:
                tool_info = self.GITHUB_TOOLS[tool_name]
                if not os.path.exists(tool_info['path']):
                    subprocess.run(['git', 'clone', tool_info['url'], tool_info['path']], check=True)
                    subprocess.run(['chmod', '+x', '-R', tool_info['path']], check=True)
                self.installed_tools.add(tool_name)
                self.console.print(f"[green]✓ {tool_name} installed successfully[/green]")
                return True
                
        except subprocess.CalledProcessError as e:
            self.console.print(f"[red]✗ Failed to install {tool_name}: {e}[/red]")
            return False
        
        return False
    
    def ensure_tools(self, tools):
        """Ensure all required tools are installed"""
        missing_tools = []
        
        for tool in tools:
            if not self.check_tool(tool) and tool not in self.installed_tools:
                missing_tools.append(tool)
        
        if missing_tools:
            self.console.print(f"[yellow]Missing tools: {', '.join(missing_tools)}[/yellow]")
            for tool in missing_tools:
                self.install_tool(tool)
        
        return len(missing_tools) == 0
    
    def run_command(self, command, timeout=300):
        """Execute a system command safely"""
        try:
            self.console.print(f"[cyan]Executing: {command}[/cyan]")
            result = subprocess.run(
                command.split() if isinstance(command, str) else command,
                capture_output=True, text=True, timeout=timeout
            )
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'command': command
            }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'stdout': '',
                'stderr': f'Command timed out after {timeout} seconds',
                'command': command
            }
        except Exception as e:
            return {
                'success': False,
                'stdout': '',
                'stderr': str(e),
                'command': command
            }

class PentestingPhases:
    """Implementation of the 6 pentesting phases"""
    
    def __init__(self, ai_engine, tool_manager, target, scope, auth_key):
        self.ai = ai_engine
        self.tools = tool_manager
        self.target = target
        self.scope = scope
        self.auth_key = auth_key
        self.console = Console()
        self.results = {}
        
        # Setup reports directory
        self.report_dir = Path(f"/reports/{target}")
        self.report_dir.mkdir(parents=True, exist_ok=True)
        
    def phase1_reconnaissance(self):
        """Phase 1: Planning & Reconnaissance"""
        self.console.print(Panel("[bold blue]Phase 1: Planning & Reconnaissance[/bold blue]"))
        
        # Ensure required tools
        recon_tools = ['theharvester', 'whois', 'dnsenum', 'nmap', 'masscan']
        self.tools.ensure_tools(recon_tools)
        
        results = {}
        
        # Passive Reconnaissance
        self.console.print("[yellow]Starting passive reconnaissance...[/yellow]")
        
        # theHarvester
        harvester_cmd = f"theharvester -d {self.target} -b all -f {self.report_dir}/harvester.json"
        harvester_result = self.tools.run_command(harvester_cmd)
        results['harvester'] = harvester_result
        
        # WHOIS lookup
        whois_cmd = f"whois {self.target}"
        whois_result = self.tools.run_command(whois_cmd)
        results['whois'] = whois_result
        
        # DNS enumeration
        dns_cmd = f"dnsenum {self.target}"
        dns_result = self.tools.run_command(dns_cmd)
        results['dns'] = dns_result
        
        # Active Reconnaissance
        self.console.print("[yellow]Starting active reconnaissance...[/yellow]")
        
        # Nmap service detection
        nmap_cmd = f"nmap -sV -Pn {self.target} -oN {self.report_dir}/nmap_services.txt"
        nmap_result = self.tools.run_command(nmap_cmd)
        results['nmap'] = nmap_result
        
        # Masscan for fast port scanning
        masscan_cmd = f"masscan -p1-65535 {self.target} --rate=1000"
        masscan_result = self.tools.run_command(masscan_cmd)
        results['masscan'] = masscan_result
        
        # AI Analysis
        combined_output = "\n".join([f"{k}: {v['stdout']}" for k, v in results.items()])
        ai_analysis = self.ai.analyze(
            f"Reconnaissance phase for target {self.target}",
            combined_output,
            "reconnaissance"
        )
        
        results['ai_analysis'] = ai_analysis
        self.results['phase1'] = results
        
        self.console.print(Panel(ai_analysis, title="[green]AI Analysis[/green]"))
        
        # Save results
        self._save_phase_results("phase1_reconnaissance", results)
        
        return results
    
    def phase2_scanning_enumeration(self):
        """Phase 2: Scanning & Enumeration"""
        self.console.print(Panel("[bold blue]Phase 2: Scanning & Enumeration[/bold blue]"))
        
        # Ensure required tools
        scan_tools = ['nmap', 'nikto', 'gobuster', 'whatweb', 'enum4linux']
        self.tools.ensure_tools(scan_tools)
        
        results = {}
        
        # Vulnerability scanning
        self.console.print("[yellow]Starting vulnerability scanning...[/yellow]")
        
        # Nmap vulnerability scripts
        nmap_vuln_cmd = f"nmap --script vuln {self.target} -oN {self.report_dir}/nmap_vulns.txt"
        nmap_vuln_result = self.tools.run_command(nmap_vuln_cmd)
        results['nmap_vulns'] = nmap_vuln_result
        
        # Web application scanning
        self.console.print("[yellow]Starting web application scanning...[/yellow]")
        
        # Nikto web vulnerability scanner
        nikto_cmd = f"nikto -h {self.target} -output {self.report_dir}/nikto.txt"
        nikto_result = self.tools.run_command(nikto_cmd)
        results['nikto'] = nikto_result
        
        # Directory brute forcing with gobuster
        gobuster_cmd = f"gobuster dir -u http://{self.target} -w /usr/share/wordlists/dirb/common.txt -o {self.report_dir}/gobuster.txt"
        gobuster_result = self.tools.run_command(gobuster_cmd)
        results['gobuster'] = gobuster_result
        
        # Technology stack detection
        whatweb_cmd = f"whatweb {self.target}"
        whatweb_result = self.tools.run_command(whatweb_cmd)
        results['whatweb'] = whatweb_result
        
        # SMB/NetBIOS enumeration
        enum4linux_cmd = f"enum4linux {self.target}"
        enum4linux_result = self.tools.run_command(enum4linux_cmd)
        results['enum4linux'] = enum4linux_result
        
        # AI Analysis
        combined_output = "\n".join([f"{k}: {v['stdout']}" for k, v in results.items()])
        ai_analysis = self.ai.analyze(
            f"Scanning and enumeration phase for target {self.target}",
            combined_output,
            "scanning"
        )
        
        results['ai_analysis'] = ai_analysis
        self.results['phase2'] = results
        
        self.console.print(Panel(ai_analysis, title="[green]AI Analysis[/green]"))
        
        # Save results
        self._save_phase_results("phase2_scanning_enumeration", results)
        
        return results
    
    def phase3_exploitation(self, confirm=True):
        """Phase 3: Exploitation"""
        self.console.print(Panel("[bold red]Phase 3: Exploitation[/bold red]"))
        
        if confirm and not Confirm.ask("[red]This phase will attempt to exploit vulnerabilities. Continue?[/red]"):
            self.console.print("[yellow]Exploitation phase skipped by user.[/yellow]")
            return {}
        
        # Ensure required tools
        exploit_tools = ['searchsploit', 'sqlmap', 'hydra', 'metasploit-framework']
        self.tools.ensure_tools(exploit_tools)
        
        results = {}
        
        # Search for exploits
        self.console.print("[yellow]Searching for available exploits...[/yellow]")
        
        # Use AI to identify potential vulnerabilities from previous phases
        if 'phase2' in self.results:
            vuln_data = str(self.results['phase2'])
            exploit_suggestions = self.ai.analyze(
                f"Suggest exploits for target {self.target}",
                vuln_data,
                "exploitation_planning"
            )
            results['exploit_suggestions'] = exploit_suggestions
            self.console.print(Panel(exploit_suggestions, title="[yellow]Exploit Suggestions[/yellow]"))
        
        # SQL injection testing
        sqlmap_cmd = f"sqlmap -u http://{self.target} --batch --crawl=2"
        sqlmap_result = self.tools.run_command(sqlmap_cmd)
        results['sqlmap'] = sqlmap_result
        
        # Brute force common services (with rate limiting)
        hydra_cmd = f"hydra -L /usr/share/wordlists/metasploit/unix_users.txt -P /usr/share/wordlists/metasploit/unix_passwords.txt -t 4 {self.target} ssh"
        hydra_result = self.tools.run_command(hydra_cmd)
        results['hydra'] = hydra_result
        
        # AI Analysis
        combined_output = "\n".join([f"{k}: {str(v)}" for k, v in results.items()])
        ai_analysis = self.ai.analyze(
            f"Exploitation phase for target {self.target}",
            combined_output,
            "exploitation"
        )
        
        results['ai_analysis'] = ai_analysis
        self.results['phase3'] = results
        
        self.console.print(Panel(ai_analysis, title="[green]AI Analysis[/green]"))
        
        # Save results
        self._save_phase_results("phase3_exploitation", results)
        
        return results
    
    def phase4_post_exploitation(self):
        """Phase 4: Post-Exploitation"""
        self.console.print(Panel("[bold blue]Phase 4: Post-Exploitation[/bold blue]"))
        
        # This phase would only run if exploitation was successful
        # For demo purposes, we'll show what would happen
        
        results = {}
        
        self.console.print("[yellow]Post-exploitation activities (simulated):[/yellow]")
        self.console.print("• Privilege escalation enumeration")
        self.console.print("• Credential harvesting")  
        self.console.print("• Lateral movement assessment")
        self.console.print("• Data exfiltration simulation")
        
        # AI provides post-exploitation guidance
        ai_analysis = self.ai.analyze(
            f"Post-exploitation guidance for {self.target}",
            "Simulated successful exploitation",
            "post_exploitation"
        )
        
        results['ai_analysis'] = ai_analysis
        self.results['phase4'] = results
        
        self.console.print(Panel(ai_analysis, title="[green]AI Analysis[/green]"))
        
        # Save results
        self._save_phase_results("phase4_post_exploitation", results)
        
        return results
    
    def phase5_reporting(self):
        """Phase 5: Reporting"""
        self.console.print(Panel("[bold blue]Phase 5: Reporting[/bold blue]"))
        
        results = {}
        
        # Generate comprehensive report
        report_data = {
            'target': self.target,
            'scope': self.scope,
            'timestamp': datetime.now().isoformat(),
            'phases': self.results
        }
        
        # AI-generated executive summary
        all_findings = json.dumps(self.results, indent=2)
        executive_summary = self.ai.analyze(
            f"Generate executive summary for pentest of {self.target}",
            all_findings,
            "executive_summary"
        )
        
        # Technical report
        technical_report = self.ai.analyze(
            f"Generate technical report for pentest of {self.target}",
            all_findings,
            "technical_report"
        )
        
        # Create reports
        self._create_markdown_report(report_data, executive_summary, technical_report)
        self._create_json_report(report_data)
        
        results['executive_summary'] = executive_summary
        results['technical_report'] = technical_report
        self.results['phase5'] = results
        
        self.console.print("[green]Reports generated successfully![/green]")
        self.console.print(f"[cyan]Report location: {self.report_dir}[/cyan]")
        
        return results
    
    def phase6_retesting(self):
        """Phase 6: Retesting"""
        self.console.print(Panel("[bold blue]Phase 6: Retesting[/bold blue]"))
        
        results = {}
        
        # AI guidance on retesting
        ai_analysis = self.ai.analyze(
            f"Retesting strategy for {self.target}",
            "After remediation efforts",
            "retesting"
        )
        
        results['ai_analysis'] = ai_analysis
        results['retest_plan'] = "Focused retesting on identified vulnerabilities"
        
        self.console.print(Panel(ai_analysis, title="[green]Retesting Plan[/green]"))
        
        # Save results
        self._save_phase_results("phase6_retesting", results)
        
        return results
    
    def _save_phase_results(self, phase_name, results):
        """Save phase results to file"""
        with open(self.report_dir / f"{phase_name}.json", 'w') as f:
            json.dump(results, f, indent=2, default=str)
    
    def _create_markdown_report(self, report_data, executive_summary, technical_report):
        """Create markdown report"""
        markdown_content = f"""
# Penetration Testing Report

## Executive Summary
{executive_summary}

## Technical Report
{technical_report}

## Test Details
- **Target:** {report_data['target']}
- **Scope:** {report_data['scope']}
- **Date:** {report_data['timestamp']}

## Detailed Findings
"""
        
        for phase, data in report_data['phases'].items():
            markdown_content += f"\n### {phase.replace('_', ' ').title()}\n"
            if 'ai_analysis' in data:
                markdown_content += f"{data['ai_analysis']}\n"
        
        # Save markdown
        with open(self.report_dir / "report.md", 'w') as f:
            f.write(markdown_content)
        
        # Convert to PDF if possible
        try:
            pypandoc.convert_file(
                str(self.report_dir / "report.md"),
                'pdf',
                outputfile=str(self.report_dir / "report.pdf")
            )
        except Exception as e:
            self.console.print(f"[yellow]Could not generate PDF: {e}[/yellow]")
    
    def _create_json_report(self, report_data):
        """Create JSON report"""
        with open(self.report_dir / "report.json", 'w') as f:
            json.dump(report_data, f, indent=2, default=str)

class VoiceInterface:
    """Voice command interface"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        self.console = Console()
        
    def listen_for_command(self):
        """Listen for voice commands"""
        try:
            with self.microphone as source:
                self.console.print("[cyan]Listening for voice command...[/cyan]")
                audio = self.recognizer.listen(source, timeout=5)
            
            command = self.recognizer.recognize_google(audio)
            self.console.print(f"[green]Heard: {command}[/green]")
            return command.lower()
            
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            self.console.print("[red]Voice recognition service unavailable[/red]")
            return None
        except sr.WaitTimeoutError:
            return None
    
    def speak(self, text):
        """Text-to-speech output"""
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

class WebDashboard:
    """Flask web dashboard"""
    
    def __init__(self, hackgpt_instance):
        self.app = Flask(__name__)
        self.hackgpt = hackgpt_instance
        self.setup_routes()
    
    def setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def index():
            return render_template('dashboard.html')
        
        @self.app.route('/api/status')
        def status():
            return jsonify({'status': 'running'})
        
        @self.app.route('/api/run_pentest', methods=['POST'])
        def run_pentest():
            data = request.json
            # Run pentest in background thread
            thread = threading.Thread(
                target=self.hackgpt.run_full_pentest,
                args=(data['target'], data['scope'], data['auth_key'])
            )
            thread.start()
            return jsonify({'status': 'started'})
    
    def run(self, host='0.0.0.0', port=5000):
        """Run the web dashboard"""
        self.app.run(host=host, port=port, debug=False)

class HackGPT:
    """Main HackGPT application"""
    
    def __init__(self):
        self.ai_engine = AIEngine()
        self.tool_manager = ToolManager()
        self.voice_interface = VoiceInterface()
        self.console = Console()
        self.web_dashboard = None
        
    def show_banner(self):
        """Display the HackGPT banner"""
        self.console.print(BANNER)
        
    def show_menu(self):
        """Display main menu"""
        table = Table(title="HackGPT Main Menu")
        table.add_column("Option", style="cyan")
        table.add_column("Description", style="magenta")
        
        table.add_row("1", "Full Pentest (All 6 Phases)")
        table.add_row("2", "Run Specific Phase")
        table.add_row("3", "View Reports")
        table.add_row("4", "Configure AI Mode")
        table.add_row("5", "Start Web Dashboard")
        table.add_row("6", "Voice Command Mode")
        table.add_row("0", "Exit")
        
        self.console.print(table)
    
    def get_target_info(self):
        """Get target information from user"""
        target = Prompt.ask("[cyan]Enter target (IP/domain)[/cyan]")
        scope = Prompt.ask("[cyan]Enter scope description[/cyan]")
        auth_key = Prompt.ask("[cyan]Enter authorization key[/cyan]", password=True)
        
        if not all([target, scope, auth_key]):
            self.console.print("[red]All fields are required![/red]")
            return None, None, None
            
        return target, scope, auth_key
    
    def run_full_pentest(self, target=None, scope=None, auth_key=None):
        """Run complete penetration test"""
        if not all([target, scope, auth_key]):
            target, scope, auth_key = self.get_target_info()
            if not target:
                return
        
        self.console.print(f"[green]Starting full pentest against {target}[/green]")
        
        # Initialize pentesting phases
        phases = PentestingPhases(self.ai_engine, self.tool_manager, target, scope, auth_key)
        
        try:
            # Run all phases
            phases.phase1_reconnaissance()
            phases.phase2_scanning_enumeration()
            phases.phase3_exploitation()
            phases.phase4_post_exploitation()
            phases.phase5_reporting()
            phases.phase6_retesting()
            
            self.console.print("[bold green]Full pentest completed![/bold green]")
            
        except KeyboardInterrupt:
            self.console.print("[yellow]Pentest interrupted by user[/yellow]")
        except Exception as e:
            self.console.print(f"[red]Error during pentest: {e}[/red]")
    
    def run_specific_phase(self):
        """Run a specific phase"""
        target, scope, auth_key = self.get_target_info()
        if not target:
            return
            
        phases_menu = Table(title="Select Phase")
        phases_menu.add_column("Phase", style="cyan")
        phases_menu.add_column("Description", style="magenta")
        
        phases_menu.add_row("1", "Planning & Reconnaissance")
        phases_menu.add_row("2", "Scanning & Enumeration")
        phases_menu.add_row("3", "Exploitation")
        phases_menu.add_row("4", "Post-Exploitation")
        phases_menu.add_row("5", "Reporting")
        phases_menu.add_row("6", "Retesting")
        
        self.console.print(phases_menu)
        
        choice = Prompt.ask("[cyan]Select phase[/cyan]", choices=["1", "2", "3", "4", "5", "6"])
        
        phases = PentestingPhases(self.ai_engine, self.tool_manager, target, scope, auth_key)
        
        phase_methods = {
            "1": phases.phase1_reconnaissance,
            "2": phases.phase2_scanning_enumeration,
            "3": phases.phase3_exploitation,
            "4": phases.phase4_post_exploitation,
            "5": phases.phase5_reporting,
            "6": phases.phase6_retesting
        }
        
        phase_methods[choice]()
    
    def view_reports(self):
        """View existing reports"""
        reports_dir = Path("/reports")
        if not reports_dir.exists():
            self.console.print("[yellow]No reports directory found[/yellow]")
            return
        
        targets = [d.name for d in reports_dir.iterdir() if d.is_dir()]
        
        if not targets:
            self.console.print("[yellow]No reports found[/yellow]")
            return
        
        table = Table(title="Available Reports")
        table.add_column("Target", style="cyan")
        table.add_column("Reports", style="magenta")
        
        for target in targets:
            target_dir = reports_dir / target
            reports = [f.name for f in target_dir.iterdir() if f.is_file()]
            table.add_row(target, ", ".join(reports))
        
        self.console.print(table)
    
    def configure_ai_mode(self):
        """Configure AI mode"""
        current_mode = "Local LLM" if self.ai_engine.local_mode else "OpenAI API"
        self.console.print(f"[cyan]Current AI mode: {current_mode}[/cyan]")
        
        if Confirm.ask("Switch AI mode?"):
            if self.ai_engine.local_mode:
                api_key = Prompt.ask("Enter OpenAI API key", password=True)
                if api_key:
                    os.environ['OPENAI_API_KEY'] = api_key
                    self.ai_engine = AIEngine()
                    self.console.print("[green]Switched to OpenAI API mode[/green]")
            else:
                if 'OPENAI_API_KEY' in os.environ:
                    del os.environ['OPENAI_API_KEY']
                self.ai_engine = AIEngine()
                self.console.print("[green]Switched to Local LLM mode[/green]")
    
    def start_web_dashboard(self):
        """Start web dashboard"""
        self.web_dashboard = WebDashboard(self)
        self.console.print("[cyan]Starting web dashboard on http://0.0.0.0:5000[/cyan]")
        
        # Create dashboard template
        self.create_dashboard_template()
        
        try:
            self.web_dashboard.run()
        except Exception as e:
            self.console.print(f"[red]Error starting web dashboard: {e}[/red]")
    
    def create_dashboard_template(self):
        """Create HTML template for dashboard"""
        template_dir = Path("templates")
        template_dir.mkdir(exist_ok=True)
        
        dashboard_html = """
<!DOCTYPE html>
<html>
<head>
    <title>HackGPT Dashboard</title>
    <style>
        body { background: #000; color: #0f0; font-family: monospace; }
        .container { margin: 20px; }
        .panel { border: 1px solid #0f0; padding: 20px; margin: 10px 0; }
        button { background: #333; color: #0f0; border: 1px solid #0f0; padding: 10px; }
        input { background: #333; color: #0f0; border: 1px solid #0f0; padding: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>HackGPT - AI-Powered Penetration Testing</h1>
        
        <div class="panel">
            <h2>Start Pentest</h2>
            <input type="text" id="target" placeholder="Target IP/Domain">
            <input type="text" id="scope" placeholder="Scope">
            <input type="password" id="auth" placeholder="Authorization Key">
            <button onclick="startPentest()">Start Full Pentest</button>
        </div>
        
        <div class="panel">
            <h2>Status</h2>
            <div id="status">Ready</div>
        </div>
    </div>
    
    <script>
        function startPentest() {
            const target = document.getElementById('target').value;
            const scope = document.getElementById('scope').value;
            const auth = document.getElementById('auth').value;
            
            fetch('/api/run_pentest', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ target, scope, auth_key: auth })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('status').innerText = 'Pentest Started';
            });
        }
    </script>
</body>
</html>
        """
        
        with open(template_dir / "dashboard.html", "w") as f:
            f.write(dashboard_html)
    
    def voice_command_mode(self):
        """Voice command interface"""
        self.console.print("[cyan]Voice command mode activated. Say 'exit' to quit.[/cyan]")
        self.voice_interface.speak("Voice command mode activated")
        
        while True:
            command = self.voice_interface.listen_for_command()
            
            if command:
                if 'exit' in command or 'quit' in command:
                    self.voice_interface.speak("Exiting voice mode")
                    break
                elif 'full pentest' in command or 'start pentest' in command:
                    self.voice_interface.speak("Starting full pentest. Please provide target information.")
                    self.run_full_pentest()
                elif 'help' in command:
                    help_text = "Available commands: full pentest, view reports, configure AI, exit"
                    self.console.print(f"[green]{help_text}[/green]")
                    self.voice_interface.speak(help_text)
                else:
                    self.voice_interface.speak("Command not recognized")
    
    def run(self):
        """Main application loop"""
        self.show_banner()
        
        while True:
            try:
                self.show_menu()
                choice = Prompt.ask("[cyan]Select option[/cyan]", 
                                  choices=["0", "1", "2", "3", "4", "5", "6"])
                
                if choice == "0":
                    self.console.print("[green]Goodbye![/green]")
                    break
                elif choice == "1":
                    self.run_full_pentest()
                elif choice == "2":
                    self.run_specific_phase()
                elif choice == "3":
                    self.view_reports()
                elif choice == "4":
                    self.configure_ai_mode()
                elif choice == "5":
                    self.start_web_dashboard()
                elif choice == "6":
                    self.voice_command_mode()
                    
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Use option 0 to exit properly[/yellow]")
            except Exception as e:
                self.console.print(f"[red]Error: {e}[/red]")

def main():
    """Entry point"""
    parser = argparse.ArgumentParser(description="HackGPT - AI-Powered Penetration Testing Tool")
    parser.add_argument('--target', help='Target IP or domain')
    parser.add_argument('--scope', help='Scope description')
    parser.add_argument('--auth-key', help='Authorization key')
    parser.add_argument('--confirm', action='store_true', help='Skip confirmation prompts')
    parser.add_argument('--web', action='store_true', help='Start web dashboard only')
    parser.add_argument('--voice', action='store_true', help='Start in voice mode')
    
    args = parser.parse_args()
    
    hackgpt = HackGPT()
    
    if args.web:
        hackgpt.start_web_dashboard()
    elif args.voice:
        hackgpt.show_banner()
        hackgpt.voice_command_mode()
    elif args.target and args.scope and args.auth_key:
        hackgpt.show_banner()
        hackgpt.run_full_pentest(args.target, args.scope, args.auth_key)
    else:
        hackgpt.run()

if __name__ == "__main__":
    main()
