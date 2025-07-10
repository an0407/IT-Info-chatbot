from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session

from app.models.pydantic.chat_payload import AdminPayload
from app.services.chat_service import ChatService
# from app.utils.json_to_txt import convert_json_to_txt

# scrape_top_30_chennai()



router = APIRouter(prefix="/chat", tags = ['AI_chat'])
 
@router.post('/')
async def ai_chat(question: AdminPayload, db: AsyncSession = Depends(get_async_session)):
    chroma = ChromaService()
    vectordb = chroma.build_vector_store()
    response = await ChatService(db).chat(chat_data=question, vectordb=vectordb)
    return {'response' : response}