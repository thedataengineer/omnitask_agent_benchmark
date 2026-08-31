import dataclasses
from typing import Optional, List, Dict, Any
from datetime import datetime

@dataclasses.dataclass
class User:
    id: str
    email: str
    password_hash: str
    role: str = 'developer'
    created_at: float = dataclasses.field(default_factory=lambda: datetime.utcnow().timestamp())

@dataclasses.dataclass
class TaskJob:
    id: str
    user_id: str
    payload: Dict[str, Any]
    status: str = 'pending'
    retry_count: int = 0
    created_at: float = dataclasses.field(default_factory=lambda: datetime.utcnow().timestamp())

@dataclasses.dataclass
class Invoice:
    id: str
    user_id: str
    amount_cents: int
    currency: str = 'USD'
    paid: bool = False
    created_at: float = dataclasses.field(default_factory=lambda: datetime.utcnow().timestamp())

    # Shared model enhancement
