"""
Azure Functions PDP (Policy Decision Point) for Agentic AI Governance

This Azure Function serves as the Policy Decision Point for agent authorization,
evaluating Cedar-style policies and integrating with Microsoft Purview.
"""

import json
import logging
import azure.functions as func
from datetime import datetime
import os

# ============================================================================
# Configuration
# ============================================================================

PURVIEW_ACCOUNT_NAME = os.environ.get('PURVIEW_ACCOUNT_NAME', '')
KEY_VAULT_URI = os.environ.get('KEY_VAULT_URI', '')
LOG_ANALYTICS_WORKSPACE_ID = os.environ.get('LOG_ANALYTICS_WORKSPACE_ID', '')

# ============================================================================
# Policy Evaluation
# ============================================================================

def evaluate_policy(agent_id: str, action: dict, resource: dict, context: dict) -> dict:
    """
    Evaluate policy for the given agent action.
    Implements Cedar-style policy evaluation.
    """
    # In production, this would evaluate actual Cedar policies
    # For demo, implement simple policy evaluation logic
    
    violations = []
    
    # Check 1: Agent identity must be verified
    if not context.get('identity_verified', False):
        violations.append({
            'control': 'IDENTITY-001',
            'message': 'Agent identity not verified'
        })
    
    # Check 2: Agent must have required permissions
    if resource.get('required_permission'):
        if context.get('permission_level', 0) < resource.get('required_permission'):
            violations.append({
                'control': 'AUTHZ-001',
                'message': 'Insufficient permission for action'
            })
    
    # Check 3: High-risk actions require approval
    if resource.get('risk_level') == 'critical' and not context.get('approval_granted', False):
        violations.append({
            'control': 'ESCALATION-001',
            'message': 'High-risk action requires human approval'
        })
    
    # Check 4: Cost limits
    if context.get('remaining_budget', 0) <= 0:
        violations.append({
            'control': 'COST-001',
            'message': 'Insufficient budget for action'
        })
    
    return {
        'allowed': len(violations) == 0,
        'violations': violations,
        'timestamp': datetime.now().isoformat()
    }

# ============================================================================
# HTTP Trigger
# ============================================================================

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    HTTP-triggered Azure Function for policy evaluation.
    """
    logging.info('Policy Engine function processed a request.')
    
    try:
        # Parse request body
        req_body = req.get_json()
        agent_id = req_body.get('agentId', 'unknown')
        action = req_body.get('action', {})
        resource = req_body.get('resource', {})
        context = req_body.get('context', {})
        
        # Evaluate policy
        result = evaluate_policy(agent_id, action, resource, context)
        
        # Log to Application Insights
        logging.info(f"Policy evaluation result for agent {agent_id}: {result['allowed']}")
        
        return func.HttpResponse(
            json.dumps({
                'agentId': agent_id,
                'timestamp': datetime.now().isoformat(),
                'allowed': result['allowed'],
                'violations': result['violations'],
                'reason': 'Policy evaluation completed'
            }),
            status_code=200,
            mimetype='application/json'
        )
    
    except Exception as e:
        logging.error(f"Error in policy evaluation: {str(e)}")
        return func.HttpResponse(
            json.dumps({
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }),
            status_code=500,
            mimetype='application/json'
        )
