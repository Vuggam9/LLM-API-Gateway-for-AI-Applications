from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from app.core.config import get_settings


class LLMService:
    def __init__(self) -> None:
        self.settings = get_settings()

    def generate(self, prompt_text: str, model_name: str | None = None, temperature: float = 0.2) -> str:
        if not self.settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is missing. Add it to your .env file before running inference.")

        llm = ChatOpenAI(
            api_key=self.settings.openai_api_key,
            model=model_name or self.settings.openai_model,
            temperature=temperature,
        )
        response = llm.invoke([HumanMessage(content=prompt_text)])
        return str(response.content)
