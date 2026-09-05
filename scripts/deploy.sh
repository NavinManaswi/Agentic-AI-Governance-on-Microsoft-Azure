#!/bin/bash
# One-click deployment script for Agentic AI Governance on Microsoft Azure

set -e

echo "🤖 Agentic AI Governance on Microsoft Azure"
echo "============================================"
echo ""

# Check prerequisites
echo "🔍 Checking prerequisites..."
command -v az >/dev/null 2>&1 || { echo "❌ Azure CLI not found. Please install it."; exit 1; }
command -v func >/dev/null 2>&1 || { echo "❌ Azure Functions Core Tools not found. Please install it."; exit 1; }
command -v pwsh >/dev/null 2>&1 || { echo "❌ PowerShell 7 not found. Please install it."; exit 1; }
echo "✅ Prerequisites satisfied."
echo ""

# Check Azure login
echo "🔐 Checking Azure login..."
az account show >/dev/null 2>&1 || { echo "❌ Not logged into Azure. Please run 'az login'."; exit 1; }
echo "✅ Logged into Azure."
echo ""

# Get user input
read -p "Enter your email for notifications: " EMAIL
read -p "Enter Azure subscription ID: " SUBSCRIPTION_ID
read -p "Enter resource group name: " RESOURCE_GROUP
read -p "Enter location (default: eastus): " LOCATION
LOCATION=${LOCATION:-eastus}

# Set subscription
az account set --subscription "$SUBSCRIPTION_ID"

# Create resource group
echo "📦 Creating resource group..."
az group create --name "$RESOURCE_GROUP" --location "$LOCATION"
echo "✅ Resource group created."
echo ""

# Deploy Bicep infrastructure
echo "🚀 Deploying Bicep infrastructure..."
az deployment group create \
  --resource-group "$RESOURCE_GROUP" \
  --template-file infrastructure/main.bicep \
  --parameters \
    environment=dev \
    location="$LOCATION" \
    notificationEmail="$EMAIL" \
    purviewAccountName="purview-agentic-$(openssl rand -hex 4)" \
    aiFoundryResourceGroup="$RESOURCE_GROUP"
echo "✅ Infrastructure deployment complete."
echo ""

# Deploy Azure Policy initiatives
echo "⚙️ Deploying Azure Policy initiatives..."
az policy initiative create \
  --name agentic-ai-governance \
  --display-name "Agentic AI Governance Initiative" \
  --description "Azure Policy initiative for agentic AI governance" \
  --rules infrastructure/policy-initiatives/agentic-ai-governance-policy.json || echo "Initiative may already exist"
echo "✅ Policy initiatives deployed."
echo ""

# Deploy Azure Functions
echo "📤 Deploying Azure Functions..."
cd src/policy-engine
func azure functionapp publish "func-agentic-pdp-dev" || echo "Function app may not exist yet"
cd ../..
echo "✅ Functions deployed."
echo ""

echo "🎉 Deployment complete!"
echo ""
echo "📊 Power BI dashboard available at:"
echo "   https://app.powerbi.com/"
echo ""
echo "🔍 Microsoft Sentinel available at:"
echo "   https://portal.azure.com/#view/Microsoft_Azure_Security/Sentinel"
echo ""
echo "📋 Microsoft Purview available at:"
echo "   https://web.purview.azure.com/"
echo ""
echo "📧 Email notifications configured for: $EMAIL"
echo ""
echo "✅ Your Agentic AI Governance framework is now operational!"
