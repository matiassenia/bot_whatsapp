from pydantic import BaseModel
from typing import Optional


class InboundMessage(BaseModel):
    phone: str
    message_id: str
    text: Optional[str]
    timestamp: Optional[str]
    profile_name: Optional[str]