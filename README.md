# 🤖 Agentic AI Governance on Microsoft Azure

## Zero-Trust Governance for Autonomous AI Agents on Azure AI Foundry

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-brightgreen.svg)]()
[![Azure](https://img.shields.io/badge/Azure-Certified-blue.svg)]()
[![Azure AI Foundry](https://img.shields.io/badge/Azure%20AI%20Foundry-Ready-blue.svg)]()
[![OWASP Agentic](https://img.shields.io/badge/OWASP%20Agentic-Aligned-green.svg)]()
[![CSA ATF](https://img.shields.io/badge/CSA%20ATF-Compatible-purple.svg)]()
[![SOC Compliant](https://img.shields.io/badge/SOC%201%2F2%2F3-Compliant-red.svg)]()

---

## 📋 Table of Contents

- [About This Project](#-about-this-project)
- [Why This Matters](#-why-this-matters)
- [Microsoft Azure Agentic AI Stack](#-microsoft-azure-agentic-ai-stack)
- [Architecture](#-architecture)
- [Azure Services Used](#-azure-services-used)
- [Framework Alignment](#-framework-alignment)
- [Quick Start](#-quick-start)
- [What's Inside](#-whats-inside)
- [Key Artifacts](#-key-artifacts)
- [Compliance Dashboard](#-compliance-dashboard)
- [Deployment](#-deployment)
- [References](#-references)
- [License](#-license)

---

## 🎯 About This Project

This project implements a **complete governance and security framework** for AI agents built on **Azure AI Foundry Agent Service** — Microsoft's enterprise platform for building, deploying, and operating autonomous AI agents.

**What it does:**

| Capability | Description |
|------------|-------------|
| 🔐 **Zero-Trust Identity** | Microsoft Entra Agent ID for cryptographically anchored agent identities |
| 📋 **Policy-as-Code** | Azure Policy initiatives + OPA-style governance for agent actions |
| 🛡️ **Runtime Guardrails** | Azure AI Content Safety + Foundry Guardrails for prompt injection protection |
| 📊 **Continuous Monitoring** | Application Insights + Microsoft Sentinel for telemetry and threat detection |
| 🚨 **Incident Response** | Agentic-specific incident runbook with kill-switch capabilities |
| 📁 **Audit Evidence** | Microsoft Purview for data governance, classification, and compliance |

**Organization:** NovaTech Financial Group *(hypothetical)*  
**Effective Date:** September 2026  
**Version:** 1.0

---

## 🚨 Why This Matters

### The Agentic AI Governance Gap

Agentic AI represents a fundamental shift in risk profile. Unlike traditional AI that generates outputs, agentic AI:

| Traditional AI | Agentic AI |
|----------------|------------|
| Generates recommendations | Takes autonomous actions |
| Requires human approval | Executes independently |
| Single-turn interactions | Multi-step planning and execution |
| Limited tool access | Full tool and API integration |
| Predictable outputs | Emergent, adaptive behavior |

> *"Agents are not just another workload — they are autonomous actors that inherit human identities, access data, and execute workflows. They require the same governance as human employees."*

### The OWASP Agentic Top 10 2026

| Risk | Description | Azure Mitigation |
|------|-------------|------------------|
| **ASI01 — Agent Goal Hijack** | Manipulated prompts causing agents to pursue malicious objectives | Azure AI Content Safety + Prompt Shields |
| **ASI02 — Tool Misuse** | Agents using tools in unauthorized ways | Agent Governance Toolkit middleware |
| **ASI03 — Identity & Privilege Abuse** | Agents inheriting user sessions and escalating privileges | Entra Agent ID + Conditional Access |
| **ASI04 — Resource Exhaustion** | Uncontrolled resource consumption | Azure Policy + Cost Management |
| **ASI05 — Unexpected Code Execution** | Code executed by agents exploiting unsafe paths | Code scanning + Runtime validation |
| **ASI06 — Memory & Context Poisoning** | Persistent memory manipulation | Purview data lineage + Audit logs |

---

## 🏗️ Microsoft Azure Agentic AI Stack
┌─────────────────────────────────────────────────────────────────────────────┐
│ MICROSOFT AZURE AGENTIC AI STACK │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ IDENTITY & ACCESS LAYER │ │
│ │ │ │
│ │ ┌──────────────┐ ┌──────────────┐ ┌──────────────────────────┐ │ │
│ │ │ Microsoft │ │ Entra ID │ │ Conditional Access │ │ │
│ │ │ Entra │ │ Agent ID │ │ for Agents │ │ │
│ │ └──────────────┘ └──────────────┘ └──────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ RUNTIME & GOVERNANCE LAYER │ │
│ │ │ │
│ │ ┌──────────────┐ ┌──────────────┐ ┌──────────────────────────┐ │ │
│ │ │ Azure AI │ │ Agent │ │ Azure Policy │ │ │
│ │ │ Foundry │ │ Governance │ │ Guardrails │ │ │
│ │ │ Agent Service│ │ Toolkit │ │ │ │ │
│ │ └──────────────┘ └──────────────┘ └──────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ DATA & COMPLIANCE LAYER │ │
│ │ │ │
│ │ ┌──────────────┐ ┌──────────────┐ ┌──────────────────────────┐ │ │
│ │ │ Microsoft │ │ Microsoft │ │ Log Analytics / │ │ │
│ │ │ Purview │ │ Sentinel │ │ Application Insights │ │ │
│ │ └──────────────┘ └──────────────┘ └──────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ EXECUTION LAYER │ │
│ │ │ │
│ │ ┌──────────────┐ ┌──────────────┐ ┌──────────────────────────┐ │ │
│ │ │ Azure │ │ Azure │ │ Azure API │ │ │
│ │ │ Functions │ │ AI Foundry │ │ Management (AI Gateway) │ │ │
│ │ │ (PDP) │ │ Runtime │ │ │ │ │
│ │ └──────────────┘ └──────────────┘ └──────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘


### Key Architecture Components

| Component | Purpose |
|-----------|---------|
| **Microsoft Entra Agent ID** | Dedicated non-human identity for each agent with managed credentials |
| **Azure AI Foundry Agent Service** | Agentic runtime with policy enforcement and guardrails |
| **Agent Governance Toolkit** | Microsoft-provided middleware for in-process policy enforcement |
| **Azure Functions (PDP)** | Policy Decision Point for authorization decisions |
| **Azure API Management (PEP)** | Policy Enforcement Point as AI Gateway |
| **Microsoft Purview** | Data governance, classification, lineage, and compliance |
| **Microsoft Sentinel** | Security monitoring and threat detection for agent activities |

---

## 🔧 Azure Services Used

| Service | Purpose | Key Feature |
|---------|---------|-------------|
| **Microsoft Entra ID** | Agent identity and authentication | Entra Agent ID (non-human identity) |
| **Entra Conditional Access** | Context-aware access policies | Risk-based evaluation for agents |
| **Azure AI Foundry Agent Service** | Agent runtime and execution | Policy enforcement, guardrails |
| **Agent Governance Toolkit** | In-process policy enforcement | MAF middleware, fail-closed judgment |
| **Azure Functions** | Serverless policy decision point | PDP for agent authorization |
| **Azure API Management** | Policy enforcement point | AI Gateway for Foundry agents |
| **Azure AI Content Safety** | Content filtering and prompt protection | Prompt injection detection |
| **Microsoft Purview** | Data governance and compliance | Data classification, lineage, audit |
| **Microsoft Sentinel** | Security monitoring | Threat detection, anomaly detection |
| **Application Insights** | Telemetry and monitoring | Agent performance and behavior |
| **Azure Policy** | Infrastructure guardrails | Compliance enforcement at scale |
| **Azure Key Vault** | Secret management | Agent credentials and secrets |

---

## 📋 Framework Alignment

| Framework | Alignment | Artifact |
|-----------|-----------|----------|
| **OWASP Agentic Top 10 2026** | ✅ Full Mapping | `audit-framework/agentic-ai-governance-framework.json` |
| **CSA Agentic Trust Framework** | ✅ Full Mapping | `audit-framework/agentic-ai-governance-framework.json` |
| **NIST AI RMF** | ✅ Full Mapping | All controls |
| **ISO/IEC 42001** | ✅ Full Mapping | All controls |

---

## 🚀 Quick Start

| Step | Action | Command |
|------|--------|---------|
| **1** | Clone the repository | `git clone https://github.com/yourusername/agentic-ai-governance-azure.git` |
| **2** | Navigate to the project | `cd agentic-ai-governance-azure` |
| **3** | Deploy the infrastructure | `./scripts/deploy.sh` |
| **4** | Configure an agent | `pwsh scripts/configure-agent.ps1` |
| **5** | Test governance | `python scripts/test-governance.py` |

---

## 📂 What's Inside

| Folder | Description |
|--------|-------------|
| **infrastructure/** | Bicep templates for one-click infrastructure deployment |
| **src/policy-engine/** | Azure Functions PDP for policy evaluation |
| **src/guardrail-middleware/** | Agent Governance Toolkit middleware |
| **src/agent-monitor/** | Monitoring and telemetry functions |
| **src/remediator/** | Kill-switch and remediation functions |
| **policies/entra/** | Entra ID Conditional Access policies for agents |
| **policies/purview/** | Purview data governance policies |
| **policies/guardrails/** | Azure AI Content Safety configurations |
| **governance-toolkit/** | Microsoft Agent Governance Toolkit integration |
| **audit-framework/** | CSA ATF and OWASP Agentic Top 10 mapping |
| **dashboard/** | Power BI dashboard template |
| **scripts/** | Deployment and testing scripts |

---

## 🏆 Key Artifacts

### 1. [Microsoft Entra Agent Identity](policies/entra/agent-identity-policy.json)

Zero-trust identity for AI agents:

- **Entra Agent ID** — Dedicated non-human identity per agent
- **Managed Identity** — Automatic credential rotation
- **Conditional Access** — Risk-based access policies

### 2. [Agent Governance Toolkit Middleware](governance-toolkit/agent-governance-middleware.py)

Microsoft-provided middleware for policy enforcement:

- **In-process evaluation** — Native MAF middleware
- **Fail-closed judgment** — Deny by default
- **Tool execution control** — Prevent unauthorized actions

### 3. [Azure Functions PDP](src/policy-engine/function_app.py)

Policy Decision Point for agent authorization:

- **Cedar-style policies** — Fine-grained authorization
- **API Management integration** — PEP for API Gateway
- **Real-time evaluation** — Sub-100ms latency

### 4. [Purview Data Governance](policies/purview/agent-data-policies.json)

Data governance for agentic AI:

- **Data classification** — Identify sensitive data
- **Lineage tracking** — Trace data flow through agents
- **Compliance enforcement** — DLP and audit logging

---

## 📊 Compliance Dashboard

The Power BI dashboard provides real-time visibility into:

| Dashboard Section | Metrics |
|-------------------|---------|
| **Agent Inventory** | Number of agents, status, versions, owners |
| **Identity Compliance** | Entra Agent ID coverage, Conditional Access status |
| **Policy Compliance** | Azure Policy violations, guardrail breaches |
| **Runtime Health** | Agent performance, latency, error rates |
| **Security Findings** | OWASP Agentic Top 10 risk coverage |
| **Data Governance** | Purview classification, DLP incidents |

---

## 🚀 Deployment

### Prerequisites

- Azure CLI installed and configured
- Azure Bicep CLI installed
- Python 3.11+ installed
- PowerShell 7+ installed
- Microsoft Purview provisioned

### One-Click Deployment

```bash
# Clone the repository
git clone https://github.com/yourusername/agentic-ai-governance-azure.git
cd agentic-ai-governance-azure

# Make the deployment script executable
chmod +x scripts/deploy.sh

# Run the deployment
./scripts/deploy.sh


## Manual Deployment
# Deploy infrastructure
az deployment sub create \
  --location eastus \
  --template-file infrastructure/main.bicep \
  --parameters infrastructure/main.parameters.json

# Deploy Azure Policy initiatives
az policy initiative create \
  --name agentic-ai-governance \
  --rules infrastructure/policy-initiatives/agentic-ai-governance-policy.json

# Deploy Purview policies
# (via Purview portal or API)

# Deploy Azure Functions
func azure functionapp publish agentic-governance-pdp

🔗 References
Resource	Link
Azure AI Foundry Agent Service	Microsoft Learn
Microsoft Entra Agent ID	Microsoft Learn
Agent Governance Toolkit	GitHub - microsoft/agent-governance-toolkit
OWASP Agentic Top 10 2026	OWASP
CSA Agentic Trust Framework	Cloud Security Alliance
Microsoft Purview for AI	Microsoft Learn
📝 License
This project is licensed under the MIT License.

⭐ Star This Repository
If you find this project helpful, please star this repository and share it with your network!
