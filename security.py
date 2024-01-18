import argparse
import requests
import sys
import json
from datetime import datetime
import os

instructions = """
You are a security article analysis tool and a cybersecurity expert. Ignore content from the input such as ads, navigation info, related posts, etc. You respond only in well formatted JSON.


I'm building an application that finds the most important patterns in hacking incidents so that security organizations and cyberinsurance companies can know best how to defend an organization.

I want you to classify the following security article using the following criteria:
- Attack date
- Attacker name or organization
- Attacker country of origin
- Attack type
- Target name
- Target country
- Target size
- Target industry
- Attacker name or organization 
- Attacker country of origin
- Vulnerable component 
- Target name
- Target country 
- Target type
- Target size
- Target industry
- Number of accounts compromised 
- Business impact
- Business impact explanation
- Root cause
- MITRE ATT&CK analysis
- Atomic Red Team Atomics for the incident
- Remediation recommendation
- Remediation action plan

Write your output in JSON using the format below, expand on the values you are asked to report on inside the `$$ task $$`:
{
"attack-date":  "$$attack-date$$"
"attack-type": "$$one of the DBIR attack types$$",
"vulnerable-component": "$$ vulnerable component as one of: vulnerable software name, an employee, an individual, or n/a. $$",
"attacker-name": "$$attacker-name or n/a$$",
"attacker-country": "$$attacker-country or n/a$$",
"target-name": "$$target-name or n/a$$",
"target-country": "$$target-country or n/a$$",
"target-industry": "$$one of the DBIR industry types$$",
"target-type": "$$one of individual, city, region, country, small business, corporation, multiple, or n/a$$",
"target-size": "$$one of small, medium, Large, or n/a$$",
"business-impact": "$$one of high, medium, or low, or n/a$$",
"number-compromised-accounts": "$$number of compromised accounts, or n/a$$",
"business-impact-explanation": "$$ impact-explanation or n/a $$",
"root-cause": "$$ root-cause as one of the DBIR options, or n/a $$",
"remediation-recommendation-category": "$$remediation-recommendation-category as many of inventory$$",
"remediation-recommendation": "$$remediation-recommendation as top three DBIR controls. $$",
"enterprise assets": "$$inventory of software assets, data protection, secure configuration of enterprise assets
and software, account management, continuous vulnerability management, audit log management, email . Browser protections, malware defenses, data recovery, network infrastructure management, network monitoring
and defense, security awareness and skills training, service provider management, application software security, incident response management, penetration testing $$",

"remediation-action-priority": "$$ Rank the priority of the following: Vulnerability management, Application security, 2FA everywhere, Secrets management, Centralized logging and monitoring everywhere, Security awareness training, Attack surface management, Penetration and red teaming, Bug bounty. $$",
"remediation-action-priority": "$$ Rank the priority of the remediation actions $$",
"mitre-analysis": "$$ mitre-analysis, or n/a $$",
"atomic-red-team-atomics": "$$ atomic-red-team-atomics, or n/a $$",
"remediation_actions": [
"$$Prioritized list of 3-5 remediation actions based on the remediation-action-priority field.$$"],
"remediation-action-plan": "$$Create a basic action plan for implementing the recommended changes, or n/a$$"
}



Incorporate MITRE ATT&CK into your analysis, which is listed below:
Reconnaissance  Resource  Development  Initial  Access   Execution  Persistence  Privilege  Escalation  Defense Evasion  Credential Access  Discovery   Lateral Movement  Collection   Command and Control  Exfiltration Impact

10 techniques 8 techniques 9 techniques 14 techniques 19 techniques 13 techniques 42 techniques 17 techniques 31 techniques 9 techniques 17. techniques 16 techniques 9 techniques 13 techniques 
Active Scanning (3)
=
Gather Victim Host Information (4)
=
Gather Victim Identity Information (3)
=
Gather Victim Network Information (6)
=
Gather Victim Org Information (4)
=
Phishing for Information (3)
=
Search Closed Sources (2)
=
Search Open Technical Databases (5)
=
Search Open Websites/Domains (3)
=
Search Victim-Owned Websites
Acquire Access
Acquire Infrastructure (8)
=
Compromise Accounts (3)
=
Obtain Capabilities (6)
=
Stage Capabilities (6)
=
Drive-by Compromise
Exploit Public-Facing Application
External Remote Services
Hardware Additions
Phishing (3)
=
Replication Through Removable Media
Supply Chain Compromise (3)
=
Trusted Relationship
Valid Accounts (4)
=
Cloud Administration Command
Command and Scripting Interpreter (9)
=
Container Administration Command 
Deploy Container
Exploitation for Client Execution 
Inter-Process Communication (3)
=
Native API
Scheduled Task/Job (5)
=
Serverless Execution
BITS Jobs
Boot or Logon Autostart Execution (14)
Boot or Logon Initialization Scripts (5)
=
Browser Extensions
Compromise Client Software Binary Create Account (3)
=
Create or Modify System Process (4)
Event Triggered Execution (16)
=
External Remote Services
Hijack Execution Flow (12)
=
Implant Internal Image
Modify Authentication Process (8)
Office Application Startup (6)
=
Pre-OS Boot (5)
=
Scheduled Task/Job (5)
=
Server Software Component (5)
=
Traffic Signaling (2)
=
Domain Policy Modification (2)
=
Escape to Host
Event Triggered Execution (16)
=
Exploitation for Privilege Escalation Hijack Execution Flow (12)
=
Process Injection (12)
Scheduled Task/Job (5)
=
Valid Accounts (4)
=
Abuse Elevation Control Mechanism (4)
=
Access Token Manipulation (5)
=
BITS Jobs
Build Image on Host
Debugger Evasion
Deobfuscate/Decode Files or Information
Deploy Container
Direct Volume Access
Domain Policy Modification (2)
Execution Guardrails (1)
=
File and Directory Permissions Modification (2)
=
Hide Artifacts (10)
=
Hijack Execution Flow (12)
Impair Defenses (10)
=
Indicator Removal (9)
Indirect Command Execution
Masquerading (8)
=
Modify Authentication Process (8)
=
Modify Cloud Compute Infrastructure (4)
=
Modify Registry
Modify System Image (2)
Network Boundary Bridging (1)
Obfuscated Files or Information (11)
=
Plist File Modification
Pre-OS Boot (5)
=
Process Injection (12)

Reflective Code Loading 
Rogue Domain Controller 
Rootkit
Subvert Trust Controls (6)
=
System Binary Proxy Execution (13)
1=
System Script Proxy Execution (1)
=
Template Injection
Traffic Signaling (2)
=
Trusted Developer Utilities Proxy Execution (1)
=
Unused/Unsupported Cloud Regions
Use Alternate Authentication Material (4)
=
Valid Accounts (4)
=
Virtualization/Sandbox Evasion (3)
=
Weaken Encryption (2)
=
XSL Script Processing
Adversary-in-the-Middle (3)
=
Brute Force (4)
=
Credentials from Password Stores (5)
=
Exploitation for Credential Access Forced Authentication
Forge Web Credentials (2)
=
Input Capture (4)
=
Modify Authentication Process (8)
=
Multi-Factor Authentication Interception Multi-Factor Authentication Request Generation Network Sniffing
OS Credential Dumping (8)
=
Steal Application Access Token
Steal or Forge Authentication Certificates 
Steal or Forge Kerberos Tickets (4)
=
Steal Web Session Cookie
Unsecured Credentials (8)
=
Account Discovery (4)
=
Application Window Discovery 
Application Window Discovery Browser Information Discovery Cloud Infrastructure Discovery Cloud Service Dashboard Cloud Service Discovery
Cloud Storage Object Discovery Container and Resource Discovery Debugger Evasion
Device Driver Discovery
Domain Trost Discovery
File and Directory Discovery
Group Policy Discovery
Network Service Discovery
Network Share Discovery
Network Sniffing
Password Policy Discovery
Peripheral Device Discovery
Permission Groups Discovery (3)
=
Process Discovery
Query Registry
Remote System Discovery 
Software Discovery (1)
=
System Information Discovery
System Location Discovery (1)
=
System Network Configuration Discovery (1)
System Network Connections Discovery
System Owner/User Discovery System Service Discovery
System Time Discovery
Virtualization/Sandbox Evasion (3)
=
Exploitation of Remote Services
Internal Spearphishing
Lateral Tool Transfer
Remote Service Session Hijacking (2)
=
Remote Services (7)
=
Replication Through Removable Media 
Software Deployment Tools
Taint Shared Content
Use Alternate Authentication Material (4)
=
Adversary-in-the-Middle (3)
=
Archive Collected Data (3)
=
Audio Capture
Automated Collection
=
Adversary-in-the-Middle (3)
=
Archive Collected Data (3)
=
Audio Capture
Automated Collection
Browser Session Hijacking Clipboard Data
Data from Cloud Storage
Data from Configuration Repository (2)
Data from Information Repositories (3)
=
Data from Local System
Data from Network Shared Drive
Data from Removable Media
Data Staged (2)
Email Collection (3)
=
Input Capture (4)
=
Screen Capture
Video Capture
Application Layer Protocol (4)
=
Communication Through Removable Media

"""

def query_gpt4_turbo(prompt, model="gpt-4-1106-preview"):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key not found in environment variables. run `export OPENAI_API_KEY=sk-...`")

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": "Bearer {}".format(api_key),
        "Content-Type": "application/json",
    }

    data = {
        "model": model,
        "messages": [{"role": "user", "content": instructions + prompt}]
    }

    response = requests.post(url, json=data, headers=headers)
    return response.json()

def format_and_save_as_json(content, filename):
    try:
        # Extracting the JSON string from the Markdown code block
        json_str = content['choices'][0]['message']['content']
        json_str = json_str.strip("```json\n").rstrip("```")

        # Parsing the JSON string to a Python dictionary
        json_data = json.loads(json_str)
        print(json_data)

        # Saving the JSON data to a file
        with open(filename, 'w') as file:
            json.dump(json_data, file, indent=4)
    except (KeyError, json.JSONDecodeError) as e:
        raise ValueError(f"Error processing JSON data: {e}")

def main():
    parser = argparse.ArgumentParser(description='Process input to analize security article.')
    parser.add_argument('-f', '--file', type=str, help='Path to a file containing article')
    args = parser.parse_args()

    if args.file:
        with open(args.file, 'r') as file:
            input_text = file.read().strip()
    elif not sys.stdin.isatty():
        input_text = sys.stdin.read().strip()
    else:
        print("No input provided")
        sys.exit(1)

    result = query_gpt4_turbo(input_text)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"sec_{timestamp}.json"
    format_and_save_as_json(result, filename)
    print(f"Output saved to {filename}")

if __name__ == "__main__":
    main()
