"""
DarkTrust – Models module.

This module will contain all SQLAlchemy ORM models, including:
  - User:         Platform users with roles and attributes
  - Policy:       Zero Trust access control policies
  - AuditLog:     Security event audit records
  - TrustContext: Per-request trust evaluation snapshots

Import all models here to ensure they are registered in Base.metadata
for Alembic autogenerate to detect table changes.

No models are implemented at this foundation stage.
"""
