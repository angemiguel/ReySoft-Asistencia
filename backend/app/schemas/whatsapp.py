from pydantic import BaseModel


class WhatsAppLinkResponse(BaseModel):
    url: str
