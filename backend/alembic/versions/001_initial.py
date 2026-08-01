"""Initial migration

Revision ID: 001_initial
Revises: 
Create Date: 2026-08-01 13:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # --- Enums ---
    user_status_enum = postgresql.ENUM('ACTIVE', 'INACTIVE', 'SUSPENDED', 'PENDING', name='user_status_enum')
    user_status_enum.create(op.get_bind())

    policy_effect_enum = postgresql.ENUM('ALLOW', 'DENY', name='policy_effect_enum')
    policy_effect_enum.create(op.get_bind())

    risk_level_enum = postgresql.ENUM('CRITICAL', 'LOW', 'MEDIUM', 'HIGH', 'VERIFIED', name='risk_level_enum')
    risk_level_enum.create(op.get_bind())

    audit_event_type_enum = postgresql.ENUM(
        'LOGIN_SUCCESS', 'LOGIN_FAILURE', 'LOGOUT', 'TOKEN_REFRESH', 'TOKEN_REVOKED',
        'ACCESS_GRANTED', 'ACCESS_DENIED', 'POLICY_VIOLATION',
        'USER_CREATED', 'USER_UPDATED', 'USER_DELETED', 'USER_SUSPENDED',
        'ROLE_ASSIGNED', 'ROLE_REVOKED', 'PERMISSION_GRANTED', 'PERMISSION_REVOKED',
        'POLICY_CREATED', 'POLICY_UPDATED', 'POLICY_DELETED',
        'SUSPICIOUS_ACTIVITY', 'RATE_LIMIT_EXCEEDED', 'ATTACK_DETECTED',
        'SYSTEM_STARTUP', 'SYSTEM_SHUTDOWN', 'CONFIG_CHANGED',
        name='audit_event_type_enum'
    )
    audit_event_type_enum.create(op.get_bind())

    audit_status_enum = postgresql.ENUM('SUCCESS', 'FAILURE', 'DENIED', 'ERROR', name='audit_status_enum')
    audit_status_enum.create(op.get_bind())

    # --- Tables ---
    # users
    op.create_table('users',
        sa.Column('id', sa.UUID(), nullable=False, comment='Unique user identifier (UUIDv4)'),
        sa.Column('username', sa.String(length=100), nullable=False, comment='Unique login username'),
        sa.Column('email', sa.String(length=255), nullable=False, comment='Unique email address'),
        sa.Column('hashed_password', sa.String(length=255), nullable=False, comment='Bcrypt-hashed password — never plaintext'),
        sa.Column('full_name', sa.String(length=255), nullable=True, comment='Optional display name'),
        sa.Column('is_active', sa.Boolean(), nullable=False, comment='Whether the account may authenticate'),
        sa.Column('is_superuser', sa.Boolean(), nullable=False, comment='Superuser flag — bypasses all policy checks'),
        sa.Column('status', postgresql.ENUM(name='user_status_enum', create_type=False), nullable=False, comment='Current account lifecycle state'),
        sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True, comment='Timestamp of last successful authentication'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='Record creation timestamp (UTC)'),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True, comment='Record last update timestamp (UTC)'),
        sa.PrimaryKeyConstraint('id'),
        comment='Platform user accounts'
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_index('ix_users_email_active', 'users', ['email', 'is_active'], unique=False)

    # roles
    op.create_table('roles',
        sa.Column('id', sa.UUID(), nullable=False, comment='Unique role identifier (UUIDv4)'),
        sa.Column('name', sa.String(length=100), nullable=False, comment='Unique machine-readable role name (e.g. admin, analyst)'),
        sa.Column('description', sa.String(length=500), nullable=True, comment='Human-readable description of role purpose'),
        sa.Column('is_active', sa.Boolean(), nullable=False, comment='Inactive roles deny all access without deletion'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='Record creation timestamp (UTC)'),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True, comment='Record last update timestamp (UTC)'),
        sa.PrimaryKeyConstraint('id'),
        comment='Named access-control roles'
    )
    op.create_index(op.f('ix_roles_name'), 'roles', ['name'], unique=True)

    # permissions
    op.create_table('permissions',
        sa.Column('id', sa.UUID(), nullable=False, comment='Unique permission identifier (UUIDv4)'),
        sa.Column('name', sa.String(length=150), nullable=False, comment='Unique human-readable identifier (e.g. policies:read)'),
        sa.Column('resource', sa.String(length=100), nullable=False, comment='Target resource (e.g. users, policies, audit_logs, *)'),
        sa.Column('action', sa.String(length=50), nullable=False, comment='Allowed action (e.g. read, write, delete, *)'),
        sa.Column('description', sa.String(length=500), nullable=True, comment='Human-readable explanation of this permission'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='Record creation timestamp (UTC)'),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True, comment='Record last update timestamp (UTC)'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('resource', 'action', name='uq_permission_resource_action'),
        comment='Granular resource-action access rights'
    )
    op.create_index(op.f('ix_permissions_name'), 'permissions', ['name'], unique=True)

    # user_roles
    op.create_table('user_roles',
        sa.Column('user_id', sa.UUID(), nullable=False, comment='FK → users.id'),
        sa.Column('role_id', sa.UUID(), nullable=False, comment='FK → roles.id'),
        sa.Column('assigned_by', sa.UUID(), nullable=True, comment='User who performed this role assignment'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='Timestamp when the role was assigned (UTC)'),
        sa.ForeignKeyConstraint(['assigned_by'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id', 'role_id'),
        comment='User-to-role assignments'
    )

    # role_permissions
    op.create_table('role_permissions',
        sa.Column('role_id', sa.UUID(), nullable=False, comment='FK → roles.id'),
        sa.Column('permission_id', sa.UUID(), nullable=False, comment='FK → permissions.id'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='Timestamp when the permission was granted (UTC)'),
        sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('role_id', 'permission_id'),
        comment='Role-to-permission grants'
    )

    # policies
    op.create_table('policies',
        sa.Column('id', sa.UUID(), nullable=False, comment='Unique policy identifier (UUIDv4)'),
        sa.Column('name', sa.String(length=200), nullable=False, comment='Unique policy name'),
        sa.Column('description', sa.Text(), nullable=True, comment='Human-readable description of what this policy does'),
        sa.Column('resource', sa.String(length=100), nullable=False, comment='Target resource path or wildcard (e.g. users, policies, *)'),
        sa.Column('action', sa.String(length=50), nullable=False, comment='Target action or wildcard (e.g. read, write, delete, *)'),
        sa.Column('effect', postgresql.ENUM(name='policy_effect_enum', create_type=False), nullable=False, comment='Whether this policy grants or denies access'),
        sa.Column('conditions', postgresql.JSONB(astext_type=sa.Text()), nullable=True, comment='Optional JSONB conditions evaluated by the Policy Engine'),
        sa.Column('priority', sa.Integer(), nullable=False, comment='Evaluation priority — higher value = evaluated first'),
        sa.Column('is_active', sa.Boolean(), nullable=False, comment='Inactive policies are skipped during evaluation'),
        sa.Column('created_by', sa.UUID(), nullable=True, comment='User who created this policy'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='Record creation timestamp (UTC)'),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True, comment='Record last update timestamp (UTC)'),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        comment='Zero Trust ABAC access control policies'
    )
    op.create_index(op.f('ix_policies_name'), 'policies', ['name'], unique=True)
    op.create_index(op.f('ix_policies_priority'), 'policies', ['priority'], unique=False)
    op.create_index(op.f('ix_policies_resource'), 'policies', ['resource'], unique=False)

    # trust_contexts
    op.create_table('trust_contexts',
        sa.Column('id', sa.UUID(), nullable=False, comment='Unique trust context identifier (UUIDv4)'),
        sa.Column('user_id', sa.UUID(), nullable=True, comment='Authenticated user — NULL for unauthenticated requests'),
        sa.Column('request_id', sa.String(length=100), nullable=False, comment='X-Request-ID header value for distributed tracing'),
        sa.Column('session_id', sa.String(length=255), nullable=True, comment='Session identifier if a session exists'),
        sa.Column('ip_address', sa.String(length=45), nullable=False, comment='Client IP address (IPv4 or IPv6)'),
        sa.Column('user_agent', sa.Text(), nullable=True, comment='Raw User-Agent header'),
        sa.Column('device_id', sa.String(length=255), nullable=True, comment='Device fingerprint (set by the client SDK)'),
        sa.Column('trust_score', sa.Float(), nullable=False, comment='Computed trust score 0.0 (no trust) – 100.0 (fully verified)'),
        sa.Column('risk_level', postgresql.ENUM(name='risk_level_enum', create_type=False), nullable=False, comment='Tier derived from trust_score'),
        sa.Column('is_allowed', sa.Boolean(), nullable=False, comment='Final access decision for this request'),
        sa.Column('denial_reason', sa.String(length=500), nullable=True, comment='Machine-readable reason for denial (populated when is_allowed=False)'),
        sa.Column('evaluated_policies', postgresql.JSONB(astext_type=sa.Text()), nullable=True, comment='Snapshot of policy IDs evaluated and their outcomes'),
        sa.Column('extra_metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True, comment='Additional context (geo-IP, anomaly flags, etc.)'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='Timestamp of trust evaluation (UTC)'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        comment='Immutable per-request Zero Trust evaluation snapshots'
    )
    op.create_index(op.f('ix_trust_contexts_ip_address'), 'trust_contexts', ['ip_address'], unique=False)
    op.create_index(op.f('ix_trust_contexts_request_id'), 'trust_contexts', ['request_id'], unique=False)
    op.create_index(op.f('ix_trust_contexts_user_id'), 'trust_contexts', ['user_id'], unique=False)

    # audit_logs
    op.create_table('audit_logs',
        sa.Column('id', sa.UUID(), nullable=False, comment='Unique audit log entry identifier (UUIDv4)'),
        sa.Column('user_id', sa.UUID(), nullable=True, comment='User who triggered the event — NULL for system events'),
        sa.Column('request_id', sa.String(length=100), nullable=True, comment='X-Request-ID for cross-service tracing'),
        sa.Column('trust_context_id', sa.UUID(), nullable=True, comment='Associated trust evaluation snapshot'),
        sa.Column('event_type', postgresql.ENUM(name='audit_event_type_enum', create_type=False), nullable=False, comment='Classification of the audited event'),
        sa.Column('resource', sa.String(length=100), nullable=False, comment='Resource type affected (e.g. users, policies)'),
        sa.Column('resource_id', sa.String(length=255), nullable=True, comment='Specific resource instance identifier'),
        sa.Column('action', sa.String(length=50), nullable=False, comment='Action attempted (e.g. read, write, delete)'),
        sa.Column('status', postgresql.ENUM(name='audit_status_enum', create_type=False), nullable=False, comment='Outcome of the action'),
        sa.Column('ip_address', sa.String(length=45), nullable=True, comment='Client IP address at time of event'),
        sa.Column('user_agent', sa.Text(), nullable=True, comment='Client User-Agent at time of event'),
        sa.Column('old_values', postgresql.JSONB(astext_type=sa.Text()), nullable=True, comment='State of the resource BEFORE the action (mutations only)'),
        sa.Column('new_values', postgresql.JSONB(astext_type=sa.Text()), nullable=True, comment='State of the resource AFTER the action (mutations only)'),
        sa.Column('error_message', sa.Text(), nullable=True, comment='Error message if the action resulted in FAILURE or ERROR'),
        sa.Column('extra_metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True, comment='Additional structured context (geo, threat flags, etc.)'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='Event timestamp (UTC) — immutable after insert'),
        sa.ForeignKeyConstraint(['trust_context_id'], ['trust_contexts.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        comment='Immutable security-event audit trail'
    )
    op.create_index(op.f('ix_audit_logs_created_at'), 'audit_logs', ['created_at'], unique=False)
    op.create_index(op.f('ix_audit_logs_event_type'), 'audit_logs', ['event_type'], unique=False)
    op.create_index(op.f('ix_audit_logs_request_id'), 'audit_logs', ['request_id'], unique=False)
    op.create_index(op.f('ix_audit_logs_resource'), 'audit_logs', ['resource'], unique=False)
    op.create_index(op.f('ix_audit_logs_status'), 'audit_logs', ['status'], unique=False)
    op.create_index(op.f('ix_audit_logs_user_id'), 'audit_logs', ['user_id'], unique=False)


def downgrade() -> None:
    op.drop_table('audit_logs')
    op.drop_table('trust_contexts')
    op.drop_table('policies')
    op.drop_table('role_permissions')
    op.drop_table('user_roles')
    op.drop_table('permissions')
    op.drop_table('roles')
    op.drop_table('users')

    postgresql.ENUM(name='audit_status_enum').drop(op.get_bind())
    postgresql.ENUM(name='audit_event_type_enum').drop(op.get_bind())
    postgresql.ENUM(name='risk_level_enum').drop(op.get_bind())
    postgresql.ENUM(name='policy_effect_enum').drop(op.get_bind())
    postgresql.ENUM(name='user_status_enum').drop(op.get_bind())
