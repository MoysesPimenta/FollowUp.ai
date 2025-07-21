"""Tests for the Message dataclass."""

import sys
from pathlib import Path
import uuid
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from backend.messaging_core.models import Message  # noqa: E402


def test_message_entity_dataclass() -> None:
    """Ensure the Message dataclass stores data correctly."""
    msg = Message(
        id=uuid.uuid4(),
        conversation_id=uuid.uuid4(),
        sender_id=uuid.uuid4(),
        content="Hello",
        created_at=datetime(2024, 1, 1, 12, 0, 0),
        status="sent",
    )
    assert msg.content == "Hello"
    assert msg.status == "sent"
