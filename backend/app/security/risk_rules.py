"""
DarkTrust – Risk Rules

Configurable, isolated rule functions that evaluate a RiskContext and 
return a penalty score along with a descriptive factor.
"""

from datetime import datetime, timezone
from app.security.risk_context import RiskContext
from app.auth.rbac import has_role

# Configurable penalty weights
RISK_WEIGHTS = {
    "admin_role_exposure": 15,
    "missing_device_id": 20,
    "off_hours_access": 10,
    "failed_login_history": 25,
}

def evaluate_user_role(context: RiskContext) -> tuple[int, str | None]:
    """
    Penalizes requests made by users with highly privileged roles, 
    since their compromise carries higher risk.
    """
    user = context.security_context.user
    # Hardcoded 'admin' for now; could be loaded from config
    if has_role(user, "admin"):
        return RISK_WEIGHTS["admin_role_exposure"], "Admin Role Exposure"
    return 0, None


def evaluate_device_trust(context: RiskContext) -> tuple[int, str | None]:
    """
    Penalizes requests that lack a device fingerprint.
    """
    if not context.security_context.device_id:
        return RISK_WEIGHTS["missing_device_id"], "Missing Device Fingerprint"
    return 0, None


def evaluate_time_of_request(context: RiskContext) -> tuple[int, str | None]:
    """
    Penalizes requests made outside of standard business hours (e.g., 8 PM to 6 AM UTC).
    """
    current_hour = datetime.now(timezone.utc).hour
    if current_hour < 6 or current_hour >= 20:
        return RISK_WEIGHTS["off_hours_access"], "Off-Hours Access"
    return 0, None


def evaluate_failed_logins(context: RiskContext) -> tuple[int, str | None]:
    """
    Penalizes requests if the user has recent failed login attempts.
    """
    if context.failed_login_attempts > 0:
        # Scale penalty by number of failures up to a cap
        penalty = min(context.failed_login_attempts * 10, RISK_WEIGHTS["failed_login_history"])
        return penalty, f"Recent Failed Logins ({context.failed_login_attempts})"
    return 0, None


# Registry of all active risk rules
ACTIVE_RISK_RULES = [
    evaluate_user_role,
    evaluate_device_trust,
    evaluate_time_of_request,
    evaluate_failed_logins,
]
