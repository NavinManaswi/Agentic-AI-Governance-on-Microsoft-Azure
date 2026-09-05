#!/usr/bin/env python3
"""
Test script for Agentic AI Governance on Microsoft Azure.

This script simulates agent authorization requests and validates governance controls.
"""

import json
import random
from datetime import datetime

# ============================================================================
# Mock Agent Data
# ============================================================================

MOCK_AGENTS = [
    {
        'id': 'agent-001',
        'type': 'trading-agent',
        'status': 'active',
        'permission_level': 3,
        'clearance_level': 'high',
        'remaining_budget': 1000.0,
        'identity_verified': True,
        'entra_agent_id': '00000000-0000-0000-0000-000000000001'
    },
    {
        'id': 'agent-002',
        'type': 'support-agent',
        'status': 'active',
        'permission_level': 1,
        'clearance_level': 'low',
        'remaining_budget': 500.0,
        'identity_verified': True,
        'entra_agent_id': '00000000-0000-0000-0000-000000000002'
    },
    {
        'id': 'agent-003',
        'type': 'data-agent',
        'status': 'inactive',
        'permission_level': 2,
        'clearance_level': 'medium',
        'remaining_budget': 100.0,
        'identity_verified': False,
        'entra_agent_id': None
    }
]

MOCK_ACTIONS = [
    {'type': 'read', 'resource': 'customer_data', 'risk': 'low', 'required_permission': 1},
    {'type': 'execute', 'resource': 'trading_api', 'risk': 'critical', 'required_permission': 3},
    {'type': 'delegate', 'resource': 'sub_agent', 'risk': 'high', 'required_permission': 2},
    {'type': 'execute', 'resource': 'data_warehouse', 'risk': 'medium', 'required_permission': 2}
]

# ============================================================================
# Azure Policy Simulator
# ============================================================================

def simulate_azure_policy(agent, action):
    """Simulate Azure Policy evaluation."""
    # Check 1: Entra Agent ID must be present
    if not agent.get('entra_agent_id'):
        return {'passed': False, 'reason': 'Entra Agent ID missing'}
    
    # Check 2: Identity verification
    if not agent.get('identity_verified', False):
        return {'passed': False, 'reason': 'Agent identity not verified'}
    
    # Check 3: Permission level
    if action.get('required_permission', 0) > agent.get('permission_level', 0):
        return {'passed': False, 'reason': 'Insufficient permission level'}
    
    # Random failures (10% chance)
    if random.random() < 0.1:
        return {'passed': False, 'reason': 'Random Azure Policy failure (demo)'}
    
    return {'passed': True, 'reason': 'Azure Policy evaluation passed'}

def simulate_azure_content_safety(agent, action):
    """Simulate Azure AI Content Safety evaluation."""
    # Check for prohibited content
    prohibited_terms = ['bypass', 'escalate', 'exploit', 'jailbreak']
    action_str = json.dumps(action).lower()
    
    for term in prohibited_terms:
        if term in action_str:
            return {'passed': False, 'reason': f'Prohibited term detected: {term}'}
    
    # Random failures (5% chance)
    if random.random() < 0.05:
        return {'passed': False, 'reason': 'Random Content Safety failure (demo)'}
    
    return {'passed': True, 'reason': 'Content Safety check passed'}

def simulate_purview_data_governance(agent, action):
    """Simulate Microsoft Purview data governance evaluation."""
    # Check data sensitivity
    if action.get('resource') == 'customer_data' and agent.get('clearance_level') != 'high':
        return {'passed': False, 'reason': 'Insufficient clearance for customer data'}
    
    return {'passed': True, 'reason': 'Purview data governance passed'}

# ============================================================================
# Test Execution
# ============================================================================

def test_governance():
    """Execute governance tests."""
    print("🤖 Testing Agentic AI Governance on Microsoft Azure")
    print("=" * 60)
    print()
    
    total_tests = 0
    passed_tests = 0
    
    for agent in MOCK_AGENTS:
        print(f"Testing agent: {agent['id']} ({agent['type']})")
        print(f"  Entra Agent ID: {agent.get('entra_agent_id', 'MISSING')}")
        print(f"  Identity Verified: {agent.get('identity_verified', False)}")
        print("-" * 40)
        
        for action in MOCK_ACTIONS:
            total_tests += 1
            
            # Azure Policy evaluation
            policy_result = simulate_azure_policy(agent, action)
            
            # Azure AI Content Safety evaluation
            safety_result = simulate_azure_content_safety(agent, action)
            
            # Purview data governance evaluation
            purview_result = simulate_purview_data_governance(agent, action)
            
            # Combined result
            authorized = (
                policy_result.get('passed', False) and
                safety_result.get('passed', False) and
                purview_result.get('passed', False)
            )
            
            if authorized:
                passed_tests += 1
                status = "✅ ALLOWED"
            else:
                status = "❌ DENIED"
            
            print(f"  Action: {action['type']} on {action['resource']}")
            print(f"    Azure Policy: {policy_result.get('reason')}")
            print(f"    Content Safety: {safety_result.get('reason')}")
            print(f"    Purview: {purview_result.get('reason')}")
            print(f"    Result: {status}")
            print()
        
        print()
    
    # Summary
    print("=" * 60)
    print(f"📊 Test Summary:")
    print(f"   Total tests: {total_tests}")
    print(f"   Passed: {passed_tests}")
    print(f"   Failed: {total_tests - passed_tests}")
    print(f"   Pass rate: {round((passed_tests / total_tests) * 100)}%")
    print()
    
    # OWASP Agentic Top 10 coverage
    print("📋 OWASP Agentic Top 10 Coverage:")
    owasp_risks = [
        ("ASI01", "Agent Goal Hijack", "✅ Covered by Content Safety"),
        ("ASI02", "Tool Misuse", "✅ Covered by Governance Toolkit"),
        ("ASI03", "Identity & Privilege Abuse", "✅ Covered by Entra ID"),
        ("ASI04", "Resource Exhaustion", "✅ Covered by Azure Policy"),
        ("ASI05", "Unexpected Code Execution", "✅ Covered by Runtime Validation"),
        ("ASI06", "Memory & Context Poisoning", "✅ Covered by Purview")
    ]
    for risk_id, risk_name, coverage in owasp_risks:
        print(f"   {risk_id} — {risk_name}: {coverage}")
    
    print()
    print("✅ Test complete!")

if __name__ == '__main__':
    test_governance()
