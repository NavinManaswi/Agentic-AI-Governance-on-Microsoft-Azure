// ============================================================================
// Bicep Template: Agentic AI Governance on Microsoft Azure
// ============================================================================

param environment string = 'dev'
param location string = 'eastus'
param notificationEmail string
param purviewAccountName string
param aiFoundryResourceGroup string

// ============================================================================
// Resource Group
// ============================================================================

resource aiGovernanceRG 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: 'rg-agentic-governance-${environment}'
  location: location
}

// ============================================================================
// Key Vault
// ============================================================================

resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: 'kv-agentic-governance-${uniqueString(resourceGroup().id)}'
  location: location
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: subscription().tenantId
    enableRbacAuthorization: true
  }
}

// ============================================================================
// Storage Account (for agent logs and audit data)
// ============================================================================

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: 'stagenticgov${uniqueString(resourceGroup().id)}'
  location: location
  kind: 'StorageV2'
  sku: {
    name: 'Standard_LRS'
  }
  properties: {
    allowBlobPublicAccess: false
    minimumTlsVersion: 'TLS1_2'
  }
}

// ============================================================================
// Log Analytics Workspace
// ============================================================================

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: 'law-agentic-governance-${environment}'
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 3650 // 10-year retention for compliance
  }
}

// ============================================================================
// Application Insights
// ============================================================================

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: 'appi-agentic-governance-${environment}'
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
  }
}

// ============================================================================
// Azure AI Foundry Hub
// ============================================================================

resource aiFoundryHub 'Microsoft.MachineLearningServices/workspaces@2024-10-01' = {
  name: 'aihub-agentic-governance-${environment}'
  location: location
  properties: {
    friendlyName: 'Agentic AI Governance Hub'
    description: 'Azure AI Foundry Hub for agentic AI governance'
    applicationInsights: appInsights.id
    keyVault: keyVault.id
    storageAccount: storageAccount.id
  }
}

// ============================================================================
// Azure AI Foundry Project
// ============================================================================

resource aiFoundryProject 'Microsoft.MachineLearningServices/workspaces@2024-10-01' = {
  name: 'aiproject-agentic-governance-${environment}'
  location: location
  properties: {
    friendlyName: 'Agentic AI Governance Project'
    description: 'Azure AI Foundry project for agentic AI governance'
    hubResourceId: aiFoundryHub.id
  }
}

// ============================================================================
// Microsoft Purview Account
// ============================================================================

resource purviewAccount 'Microsoft.Purview/accounts@2023-05-01-preview' = {
  name: purviewAccountName
  location: location
  properties: {
    publicNetworkAccess: 'Enabled'
  }
}

// ============================================================================
// Azure AI Content Safety
// ============================================================================

resource contentSafety 'Microsoft.CognitiveServices/accounts@2024-10-01' = {
  name: 'acs-agentic-governance-${environment}'
  location: location
  kind: 'ContentSafety'
  sku: {
    name: 'S0'
  }
  properties: {
    customSubDomainName: 'acs-agentic-governance-${environment}'
  }
}

// ============================================================================
// Azure Functions (PDP)
// ============================================================================

resource functionApp 'Microsoft.Web/sites@2024-04-01' = {
  name: 'func-agentic-pdp-${environment}'
  location: location
  kind: 'functionapp'
  properties: {
    serverFarmId: functionPlan.id
    siteConfig: {
      appSettings: [
        { name: 'FUNCTIONS_EXTENSION_VERSION', value: '~4' }
        { name: 'FUNCTIONS_WORKER_RUNTIME', value: 'python' }
        { name: 'PURVIEW_ACCOUNT_NAME', value: purviewAccountName }
        { name: 'KEY_VAULT_URI', value: keyVault.properties.vaultUri }
        { name: 'LOG_ANALYTICS_WORKSPACE_ID', value: logAnalytics.id }
        { name: 'APPLICATIONINSIGHTS_CONNECTION_STRING', value: appInsights.properties.ConnectionString }
      ]
    }
  }
}

resource functionPlan 'Microsoft.Web/serverfarms@2024-04-01' = {
  name: 'plan-agentic-governance-${environment}'
  location: location
  sku: {
    name: 'Y1'
    tier: 'Dynamic'
  }
}

// ============================================================================
// API Management (AI Gateway)
// ============================================================================

resource apiManagement 'Microsoft.ApiManagement/service@2024-05-01' = {
  name: 'apim-agentic-governance-${environment}'
  location: location
  sku: {
    name: 'Developer'
    capacity: 1
  }
  properties: {
    publisherName: 'NovaTech'
    publisherEmail: notificationEmail
  }
}

// ============================================================================
// Outputs
// ============================================================================

output aiFoundryHubId string = aiFoundryHub.id
output aiFoundryProjectId string = aiFoundryProject.id
output purviewAccountName string = purviewAccount.name
output contentSafetyEndpoint string = contentSafety.properties.endpoint
output functionAppName string = functionApp.name
output apiManagementGatewayUrl string = apiManagement.properties.gatewayUrl
