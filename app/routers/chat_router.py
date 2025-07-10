from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session

from app.models.pydantic.chat_payload import AdminPayload
from app.services.chat_service import ChatService


router = APIRouter(prefix="/chat", tags = ['AI_chat'])
 
@router.post('/')
async def ai_chat(question: AdminPayload, db: AsyncSession = Depends(get_async_session)):
    response = await ChatService(db).chat(chat_data=question)
    return {'response' : response}