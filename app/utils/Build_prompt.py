def build_prompt(query: str,history:str="") -> str:
    return f"""

History:
-Carefully check history and understand what user has spoken and user chats and response.
{history}

Question: {query}

Answer:"""
