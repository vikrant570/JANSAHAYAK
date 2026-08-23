from abc import ABC, abstractmethod
import json


class LLMProvider(ABC):

    @abstractmethod
    async def generate(
        self,
        system_prompt: str,
        user_prompt: str
    ) -> str:
        raise NotImplementedError


class MockLLMProvider(LLMProvider):

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str
    ) -> str:

        return json.dumps({
            "short_summary": (
                "Relevant verified information was found."
            ),
            "simple_explanation": (
                "I found information that may be relevant "
                "to your situation."
            ),
            "detailed_explanation": (
                "Please review the eligibility requirements, "
                "documents and official source before applying."
            ),
            "next_steps": [
                "Check the official source.",
                "Verify your eligibility.",
                "Prepare the required documents."
            ]
        })


class OpenAIProvider(LLMProvider):

    def __init__(
        self,
        api_key: str,
        model: str
    ):
        from openai import AsyncOpenAI

        self.client = AsyncOpenAI(
            api_key=api_key
        )

        self.model = model

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str
    ) -> str:

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=0.2
        )

        return response.choices[0].message.content


def get_llm_provider() -> LLMProvider:

    from app.config import get_settings

    settings = get_settings()

    provider = settings.llm_provider.lower()

    if provider == "mock":
        return MockLLMProvider()

    if provider == "openai":

        if not settings.llm_api_key:
            raise RuntimeError(
                "LLM_API_KEY is missing."
            )

        if not settings.llm_model:
            raise RuntimeError(
                "LLM_MODEL is missing."
            )

        return OpenAIProvider(
            api_key=settings.llm_api_key,
            model=settings.llm_model
        )

    raise RuntimeError(
        f"Unsupported LLM provider: {provider}"
    )