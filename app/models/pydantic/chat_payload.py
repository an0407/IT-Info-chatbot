from pydantic import BaseModel, Field

class AdminPayload(BaseModel):
    session_id : str = Field(..., examples=['abc@abc.com'])
    query : str = Field(...)