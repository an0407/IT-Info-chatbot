from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_community.vectorstores.faiss import FAISS


from app.services.memory_manager import MemoryManager
from app.services.chroma_service import ChromaService
from app.utils.Build_prompt import build_prompt
from app.utils.system_prompt import system_prompt
from app.models.pydantic.chat_payload import AdminPayload
from app.utils.prev_context_manager import get_prev_context
from app.models.db.memory_model import ChatHistory

load_dotenv()

class ChatService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.llm = ChatOpenAI(model="gpt-4o-mini")
        self.memory_manager = MemoryManager(db)
        self.retriever = ChromaService()

    async def chat(self, chat_data : AdminPayload):
        try:
            query = chat_data.query

            print(f"***QUERY****\n{query}")

            docs = self.retriever.query_docs(query)
            context = "\n\n".join(docs) if docs else "No related information found in the scraped data."

            print(f'\nlen(docs) : {len(docs)}\n')
            print(f'\n\n{context}\n\n')

            prev_contexts = get_prev_context(context)
            print(f'\n ****previous_contexts****\n {prev_contexts}\n')

            chat_history = await self.memory_manager.get_history(chat_data.session_id)

            # temp_response = self.llm.invoke(
            #     f"""The following is the chat history of past 10 user queries and agent replies ordered by latest first:
            # {chat_history}

            # The following is the user's current query:
            # {chat_data.query}

            # Analyze the chat history and the current query, and reply as if you are instructing another RAG chatbot on what to do with:
            # - The context
            # - The prev_contexts
            # - The same chat history

            # Be specific and clear in your instruction.""")


            systems_prompt = system_prompt(context= context,prev_contexts=prev_contexts,history= chat_history, query= query)

            # full_prompt = build_prompt(chat_data.query,chat_history)
            print(f"\n****SYSTEM PROMPT****\n {systems_prompt}\n")
            response = self.llm.invoke([
                SystemMessage(content=systems_prompt),
                HumanMessage(content=query)
            ])

            await self.memory_manager.save_message(
                session_id= chat_data.session_id,
                user_input= query,
                assistant_response= response.content
            )
            print(response.content)
            return response.content
        except Exception as e:
            return {"response": f"Sorry, I encountered an error: {str(e)}"}