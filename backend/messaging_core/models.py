"""Data models for the messaging core."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class Message:
    """Represent a single WhatsApp message."""

    id: UUID
    conversation_id: UUID
    sender_id: UUID
    content: str
    created_at: datetime
    status: str
