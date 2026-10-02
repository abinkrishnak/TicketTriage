"""Local advisory guardrails; no inference, retrieval, transactions or messaging."""
from .engine import VERSION, assess
__all__ = ['VERSION', 'assess']
