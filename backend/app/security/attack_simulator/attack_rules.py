"""
DarkTrust – Attack Rules

Defines regex patterns and logic sets representing malicious intent 
for the educational Attack Simulator.
"""

import re
from app.security.attack_simulator.simulation_models import AttackType, AttackSeverity

# Basic heuristic signatures for demonstration purposes
ATTACK_SIGNATURES = {
    AttackType.SQL_INJECTION: {
        "patterns": [
            re.compile(r"(?i)\bOR\b\s+1\s*=\s*1", re.IGNORECASE),
            re.compile(r"(?i)(UNION\s+SELECT|DROP\s+TABLE|--)", re.IGNORECASE)
        ],
        "severity": AttackSeverity.CRITICAL,
        "description": "SQL Injection payload detected"
    },
    AttackType.XSS: {
        "patterns": [
            re.compile(r"(?i)<script.*?>.*?</script>", re.IGNORECASE),
            re.compile(r"(?i)javascript:.*", re.IGNORECASE),
            re.compile(r"(?i)onerror\s*=", re.IGNORECASE)
        ],
        "severity": AttackSeverity.HIGH,
        "description": "Cross-Site Scripting (XSS) payload detected"
    },
    AttackType.PATH_TRAVERSAL: {
        "patterns": [
            re.compile(r"(?i)(\.\./|\.\.\\)", re.IGNORECASE),
            re.compile(r"(?i)/etc/passwd", re.IGNORECASE)
        ],
        "severity": AttackSeverity.HIGH,
        "description": "Path Traversal sequence detected"
    }
}
