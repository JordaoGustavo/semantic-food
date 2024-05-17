import os
from sentence_transformers import SentenceTransformer
from langchain_community.chat_models import ChatOpenAI


class LLMService:
    def generate_embedding(self, text: str):
        model = SentenceTransformer('all-MiniLM-L6-v2')
        embedding = model.encode(text)
        return embedding.tolist()
    
    def ask_question(self, prompt):
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        chat = ChatOpenAI(
            openai_api_key=OPENAI_API_KEY, streaming=True, temperature=0
        )   

        answer = ""
        for chunk in chat.stream(prompt):
            answer += chunk.content

        return answer

