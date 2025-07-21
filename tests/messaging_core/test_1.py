import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import uuid
from datetime import datetime

from backend.messaging_core.models import Message


def test_message_entity_dataclass() -> None:
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
