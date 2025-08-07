# core/message.py
from dataclasses import dataclass
from typing import Any, Dict, Optional, List
import time, uuid

@dataclass
class Message:
    """
    Standard message with causal fields.
    """
    type: str
    payload: Any
    metadata: Optional[Dict[str, Any]] = None
    cid: Optional[str] = None          # causal id
    parent_cid: Optional[str] = None   # parent causal id
    ts: Optional[float] = None         # timestamp
    tags: Optional[List[str]] = None   # optional tags

def new_message(type: str, payload: Any, metadata: Optional[Dict[str, Any]] = None, parent_cid: Optional[str] = None) -> Message:
    return Message(
        type=type,
        payload=payload,
        metadata=metadata or {},
        cid=str(uuid.uuid4()),
        parent_cid=parent_cid,
        ts=time.time(),
        tags=[]
    )
