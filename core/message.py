# core/message.py
from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class Message:
    """
    Standardized envelope for bus messages.
    """
    type: str
    payload: Any
    metadata: Dict[str, Any] = None
