"""
Azure Functions Remediator: Agent Kill-Switch and Remediation

This Azure Function implements kill-switch capabilities and automated remediation
for agentic AI governance violations.
"""

import json
import logging
import azure.functions as func
from datetime import datetime
import os
import requests

# ============================================================================
# Configuration
# ============================================================================

AZURE_AI_FOUNDRY_ENDPOINT = os.environ.get('AZURE_AI_FOUNDRY_ENDPOINT', '')
KEY_VAULT_URI = os.environ.get('KEY_VAULT_URI', '')

# ============================================================================
# Kill-Switch Actions
# ============================================================================

def activate_kill_switch(agent_id: str, reason: str, violation_type: str) -> dict:
    """
    Activate kill-switch for a rogue or compromised agent.
    """
    logging.warning(f"KILL-SWITCH ACTIVATED for agent: {agent_id}")
    logging.warning(f"Reason: {reason}")
    logging.warning(f"Violation Type: {violation_type}")
    
    try:
        # In production, this would call Azure AI Foundry API to disable agent
        # response = requests.post(
        #     f"{AZURE_AI_FOUNDRY_ENDPOINT}/agents/{agent_id}/disable",
        #     headers={"Authorization": f"Bearer {access_token}"}
        # )
        
        return {
            'status': 'kill-switch-activated',
            'agent_id': agent_id,
            'reason': reason,
            'violation_type': violation_type,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'status': 'kill-switch-failed',
            'agent_id': agent_id,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

def revoke_agent_credentials(agent_id: str, reason: str) -> dict:
    """
    Revoke agent credentials and access via Entra ID.
    """
    logging.info(f"Revoking credentials for agent: {agent_id}")
    
    try:
        # In production, this would call Microsoft Graph API to revoke tokens
        # response = requests.post(
        #     f"https://graph.microsoft.com/v1.0/identity/conditionalAccess/policies/{policy_id}/revoke",
        #     headers={"Authorization": f"Bearer {access_token}"}
        # )
        
        return {
            'status': 'credentials-revoked',
            'agent_id': agent_id,
            'reason': reason,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'status': 'revocation-failed',
            'agent_id': agent_id,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

def quarantine_agent(agent_id: str, reason: str) -> dict:
    """
    Quarantine an agent for investigation.
    """
    logging.info(f"Quarantining agent: {agent_id}")
    
    try:
        # In production, this would restrict agent access
        return {
            'status': 'agent-quarantined',
            'agent_id': agent_id,
            'reason': reason,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'status': 'quarantine-failed',
            'agent_id': agent_id,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

# ============================================================================
# Violation Classification
# ============================================================================

def classify_violation(violation_type: str) -> dict:
    """
    Classify violation type and determine appropriate action.
    Based on OWASP Agentic Top 10 2026
    """
    severity_map = {
        'GOAL_HIJACK': {'severity': 'critical', 'action': 'kill-switch'},
        'TOOL_MISUSE': {'severity': 'critical', 'action': 'kill-switch'},
        'PRIVILEGE_ABUSE': {'severity': 'critical', 'action': 'kill-switch'},
        'RESOURCE_EXHAUSTION': {'severity': 'high', 'action': 'quarantine'},
        'IDENTITY_CONFUSION': {'severity': 'critical', 'action': 'revoke-credentials'},
        'MEMORY_POISONING': {'severity': 'high', 'action': 'quarantine'},
        'COST_RUNAWAY': {'severity': 'high', 'action': 'quarantine'},
        'MINOR_ANOMALY': {'severity': 'low', 'action': 'log-only'}
    }
    
    return severity_map.get(violation_type, {'severity': 'medium', 'action': 'quarantine'})

# ============================================================================
# HTTP Trigger
# ============================================================================

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    HTTP-triggered Azure Function for remediation.
    """
    logging.info('Remediator function processed a request.')
    
    try:
        req_body = req.get_json()
        agent_id = req_body.get('agentId', 'unknown')
        violation_type = req_body.get('violationType', 'UNKNOWN')
        reason = req_body.get('reason', 'No reason provided')
        
        logging.info(f"Processing violation for agent: {agent_id}")
        logging.info(f"Violation Type: {violation_type}")
        
        # Classify violation
        classification = classify_violation(violation_type)
        severity = classification.get('severity', 'medium')
        action = classification.get('action', 'quarantine')
        
        # Execute appropriate action
        result = None
        
        if action == 'kill-switch':
            result = activate_kill_switch(agent_id, reason, violation_type)
        elif action == 'revoke-credentials':
            result = revoke_agent_credentials(agent_id, reason)
        elif action == 'quarantine':
            result = quarantine_agent(agent_id, reason)
        else:
            result = {
                'status': 'logged-only',
                'agent_id': agent_id,
                'reason': reason,
                'violation_type': violation_type,
                'timestamp': datetime.now().isoformat()
            }
        
        return func.HttpResponse(
            json.dumps({
                'agentId': agent_id,
                'violationType': violation_type,
                'severity': severity,
                'action': action,
                'result': result,
                'timestamp': datetime.now().isoformat()
            }),
            status_code=200,
            mimetype='application/json'
        )
    
    except Exception as e:
        logging.error(f"Error in remediation: {str(e)}")
        return func.HttpResponse(
            json.dumps({'error': str(e)}),
            status_code=500,
            mimetype='application/json'
        )
