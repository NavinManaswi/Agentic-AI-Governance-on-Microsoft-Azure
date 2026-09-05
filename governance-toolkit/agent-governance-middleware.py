"""
Microsoft Agent Governance Toolkit Middleware

This module provides middleware for in-process policy enforcement
for Azure AI Foundry Agent Service agents using the Microsoft Agent
Governance Toolkit (MAF).
"""

import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime

# ============================================================================
# Microsoft Agent Framework (MAF) Middleware
# ============================================================================

class AgentGovernanceMiddleware:
    """
    Agent middleware that enforces governance policies on agent actions.
    Uses the Microsoft Agent Governance Toolkit for in-process enforcement.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.policy_engine = PolicyEngine(config.get('policy_endpoint'))
        self.guardrail_evaluator = GuardrailEvaluator(config.get('guardrail_config'))
        self.purview_client = PurviewClient(config.get('purview_config'))
    
    async def before_tool_call(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Middleware hook executed before an agent tool call.
        Evaluates policies and guardrails before allowing the action.
        """
        self.logger.info(f"Evaluating tool call: {context.get('tool_name')}")
        
        # 1. Evaluate policy
        policy_result = await self.policy_engine.evaluate(
            agent_id=context.get('agent_id'),
            action=context.get('tool_name'),
            resource=context.get('tool_resource'),
            context=context
        )
        
        if not policy_result.get('allowed', False):
            self.logger.warning(f"Policy denied: {policy_result.get('reason')}")
            return {
                'allowed': False,
                'blocked': True,
                'reason': policy_result.get('reason'),
                'timestamp': datetime.now().isoformat()
            }
        
        # 2. Evaluate guardrails
        guardrail_result = await self.guardrail_evaluator.evaluate(
            agent_id=context.get('agent_id'),
            tool_name=context.get('tool_name'),
            tool_input=context.get('tool_input'),
            context=context
        )
        
        if not guardrail_result.get('passed', False):
            self.logger.warning(f"Guardrails failed: {guardrail_result.get('reason')}")
            return {
                'allowed': False,
                'blocked': True,
                'reason': guardrail_result.get('reason'),
                'timestamp': datetime.now().isoformat()
            }
        
        # 3. Log to Purview
        await self.purview_client.log_agent_interaction(
            agent_id=context.get('agent_id'),
            action=context.get('tool_name'),
            result='approved',
            timestamp=datetime.now()
        )
        
        return {
            'allowed': True,
            'blocked': False,
            'timestamp': datetime.now().isoformat()
        }
    
    async def after_tool_call(self, context: Dict[str, Any], result: Any) -> Dict[str, Any]:
        """
        Middleware hook executed after an agent tool call.
        Logs the outcome and checks for anomalies.
        """
        self.logger.info(f"Tool call completed: {context.get('tool_name')}")
        
        # Check for anomalous behavior
        anomaly_detected = await self.detect_anomalies(context, result)
        
        if anomaly_detected:
            self.logger.warning(f"Anomaly detected in tool call: {context.get('tool_name')}")
            return {
                'anomaly_detected': True,
                'timestamp': datetime.now().isoformat()
            }
        
        # Log to Purview
        await self.purview_client.log_agent_interaction(
            agent_id=context.get('agent_id'),
            action=context.get('tool_name'),
            result='completed',
            outcome=result,
            timestamp=datetime.now()
        )
        
        return {
            'anomaly_detected': False,
            'timestamp': datetime.now().isoformat()
        }
    
    async def detect_anomalies(self, context: Dict[str, Any], result: Any) -> bool:
        """
        Detect anomalous agent behavior using pattern analysis.
        """
        # In production, this would use Azure Sentinel or custom ML models
        anomalies = []
        
        # Check for unexpected tool usage patterns
        if result and isinstance(result, dict):
            if result.get('error') or result.get('status') == 'failed':
                anomalies.append('tool_failure')
            
            if result.get('data_volume', 0) > 1_000_000:  # >1MB data access
                anomalies.append('large_data_access')
        
        # Check for rate anomalies
        if context.get('request_count', 0) > context.get('rate_limit', 100):
            anomalies.append('rate_limit_exceeded')
        
        return len(anomalies) > 0


class PolicyEngine:
    """Policy Decision Point (PDP) for agent authorization."""
    
    def __init__(self, endpoint: Optional[str] = None):
        self.endpoint = endpoint or 'https://func-agentic-pdp-dev.azurewebsites.net'
    
    async def evaluate(self, agent_id: str, action: str, resource: str, context: Dict) -> Dict:
        """
        Evaluate policy for the given agent action.
        Delegates to Azure Functions PDP.
        """
        # In production, this would call the Azure Functions PDP
        # For demo, implement simple policy evaluation
        return {
            'allowed': True,
            'reason': 'Policy evaluation passed',
            'timestamp': datetime.now().isoformat()
        }


class GuardrailEvaluator:
    """Azure AI Content Safety evaluator for agent actions."""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
    
    async def evaluate(self, agent_id: str, tool_name: str, tool_input: Dict, context: Dict) -> Dict:
        """
        Evaluate guardrails for the agent action.
        Uses Azure AI Content Safety.
        """
        # In production, this would call Azure AI Content Safety API
        # For demo, implement simple guardrail evaluation
        return {
            'passed': True,
            'reason': 'Guardrails check passed',
            'timestamp': datetime.now().isoformat()
        }


class PurviewClient:
    """Microsoft Purview client for data governance."""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
    
    async def log_agent_interaction(self, agent_id: str, action: str, result: str, **kwargs):
        """
        Log agent interaction to Microsoft Purview for audit and compliance.
        """
        # In production, this would call Purview APIs
        print(f"Purview log: agent={agent_id}, action={action}, result={result}")
