from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_community.vectorstores.faiss import FAISS


from app.services.memory_manager import MemoryManager
from app.services.chroma_service import ChromaService
from app.utils.Build_prompt import build_prompt
from app.utils.system_prompt import system_prompt
from app.models.pydantic.chat_payload import AdminPayload

load_dotenv()

class ChatService:
    def __init__(self, db: AsyncSession):
        self.llm = ChatOpenAI(model="gpt-4o-mini")
        self.memory_manager = MemoryManager(db)
        self.retriever = ChromaService()

    async def chat(self, chat_data : AdminPayload):
        try:
            docs = self.retriever.query_docs(chat_data.query)
            context = "\n\n".join(docs) if docs else "No related information found in the scraped data."

            print(f'\n\n{context}\n\n')
            
            chat_history = await self.memory_manager.get_history(chat_data.session_id)


            systems_prompt = system_prompt(context,chat_history)
            # systems_prompt = f"""You are a helpful Anush's Info provider chatbot
            # - you are supposed to answer the user's query related to a person called 'Anush' uding the context below.
            # - answer to queries only relating to Anush, else just politely inform the user
            # - also answer the query only using the info in the context, if not tel the user that you do not know the answer
            # - If there is nothing in context, then tell the user that you do not know the answer, do not create your own answers instead.
            
            # **context**:{context}"""

            full_prompt = build_prompt(chat_data.query,chat_history)

            
            response = self.llm.invoke([
                SystemMessage(content=systems_prompt),
                HumanMessage(content=full_prompt)
            ])

            await self.memory_manager.save_message(
                session_id= chat_data.session_id,
                user_input= chat_data.query,
                assistant_response= response.content
            )
            print(response.content)
            return response.content
        except Exception as e:
            return {"response": f"Sorry, I encountered an error: {str(e)}"}