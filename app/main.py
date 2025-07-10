import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models.pydantic.chat_payload import AdminPayload
from app.services.chat_service import ChatService
from app.database import Base, engine
from app.models.db.memory_model import ChatHistory
from app.routers import chat_router

# 1. Template renderer
templates = Jinja2Templates(directory="app/templates") 

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as create:
        await create.run_sync(Base.metadata.create_all)  
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def message():
    return {"message" : "   add '/docs' after this page's url to open the swagger interface or '/chatbot' to open the 'IT Info Chatbot'   "}

# @app.post('/')
# async def ai_chat(question: AdminPayload, db: AsyncSession = Depends(get_async_session)):
#     response = await ChatService(db).chat(chat_data=question, vectordb=vectordb)
#     return {'response' : response}

# 2. Include API router
app.include_router(chat_router.router)

# 3. Serve the chatbot UI
@app.get("/chatbot", response_class=HTMLResponse)
async def chatbot_ui(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)